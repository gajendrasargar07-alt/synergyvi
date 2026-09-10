"""
SHAP Analysis
=============
Classical model explainability using SHAP (SHapley Additive exPlanations).
Provides global feature importance and individual prediction explanations.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


def compute_shap_values(model, X_background, X_explain=None, model_name: str = ""):
    """Compute SHAP values for a classical model.

    Args:
        model: Trained scikit-learn or XGBoost model.
        X_background: Background dataset for SHAP (subset of training data).
        X_explain: Samples to explain. If None, uses X_background.
        model_name: Name of the model for choosing explainer type.

    Returns:
        SHAP Explanation object.
    """
    import shap

    if X_explain is None:
        X_explain = X_background

    # Limit background samples for performance
    n_bg = min(config.SHAP_BACKGROUND_SAMPLES, len(X_background))
    bg = X_background[:n_bg]

    try:
        # Use TreeExplainer for tree-based models
        if model_name in ("Random Forest", "XGBoost"):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_explain)
            # TreeExplainer may return list for multi-class; take class 1
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
            return shap_values, explainer.expected_value
        else:
            # KernelExplainer for linear/SVM models
            explainer = shap.KernelExplainer(model.predict_proba, bg)
            shap_values = explainer.shap_values(X_explain, nsamples=100)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
            return shap_values, explainer.expected_value
    except Exception as e:
        # Fallback: use KernelExplainer with predict
        try:
            explainer = shap.KernelExplainer(model.predict, bg)
            shap_values = explainer.shap_values(X_explain, nsamples=100)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
            return shap_values, explainer.expected_value
        except Exception as e2:
            raise RuntimeError(f"SHAP computation failed: {e2}")


def get_feature_importance(shap_values, feature_names=None) -> dict:
    """Compute mean absolute SHAP values for global feature importance.

    Args:
        shap_values: SHAP values array (n_samples, n_features).
        feature_names: Optional list of feature names.

    Returns:
        Dictionary with feature names and their importance scores, sorted descending.
    """
    mean_abs = np.mean(np.abs(shap_values), axis=0)

    if feature_names is None:
        feature_names = [f"Feature {i}" for i in range(len(mean_abs))]

    # Sort by importance
    indices = np.argsort(mean_abs)[::-1]
    importance = {
        "features": [str(feature_names[i]) for i in indices],
        "importance": [float(mean_abs[i]) for i in indices],
    }
    return importance


def explain_single_prediction(
    model, sample, X_background, model_name: str = "", feature_names=None
) -> dict:
    """Explain a single prediction using SHAP.

    Args:
        model: Trained model.
        sample: Single sample array (1, n_features).
        X_background: Background dataset.
        model_name: Model name for explainer selection.
        feature_names: Optional feature names.

    Returns:
        Dictionary with SHAP values, base value, and feature contributions.
    """
    sample = np.atleast_2d(sample)
    shap_values, base_value = compute_shap_values(
        model, X_background, sample, model_name
    )

    if isinstance(base_value, (list, np.ndarray)):
        base_value = float(base_value[1]) if len(base_value) > 1 else float(base_value[0])

    sv = shap_values[0] if shap_values.ndim > 1 else shap_values

    if feature_names is None:
        feature_names = [f"Feature {i}" for i in range(len(sv))]

    contributions = []
    for i, (name, val) in enumerate(zip(feature_names, sv)):
        contributions.append(
            {
                "feature": str(name),
                "shap_value": float(val),
                "feature_value": float(sample[0, i]) if i < sample.shape[1] else None,
            }
        )

    # Sort by absolute contribution
    contributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)

    return {
        "base_value": float(base_value),
        "shap_values": sv.tolist(),
        "contributions": contributions,
    }


def plot_shap_summary(shap_values, X, feature_names=None):
    """Generate SHAP summary plot data for display.

    Args:
        shap_values: SHAP values array.
        X: Feature matrix.
        feature_names: Feature names.

    Returns:
        Plotly figure object.
    """
    import plotly.graph_objects as go

    importance = get_feature_importance(shap_values, feature_names)
    top_n = min(15, len(importance["features"]))

    fig = go.Figure(
        go.Bar(
            x=importance["importance"][:top_n][::-1],
            y=importance["features"][:top_n][::-1],
            orientation="h",
            marker_color="#6366f1",
        )
    )
    fig.update_layout(
        title="SHAP Feature Importance",
        xaxis_title="Mean |SHAP value|",
        yaxis_title="Feature",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400 + top_n * 20,
    )
    return fig


def plot_single_explanation(explanation: dict, top_n: int = 10):
    """Generate a waterfall-like plot for a single prediction explanation.

    Args:
        explanation: Output from explain_single_prediction().
        top_n: Number of top features to show.

    Returns:
        Plotly figure object.
    """
    import plotly.graph_objects as go

    contribs = explanation["contributions"][:top_n]
    features = [c["feature"] for c in contribs][::-1]
    values = [c["shap_value"] for c in contribs][::-1]
    colors = ["#22c55e" if v > 0 else "#ef4444" for v in values]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=features,
            orientation="h",
            marker_color=colors,
        )
    )
    fig.update_layout(
        title="Feature Contributions to Prediction",
        xaxis_title="SHAP Value (impact on prediction)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300 + top_n * 25,
    )
    return fig
