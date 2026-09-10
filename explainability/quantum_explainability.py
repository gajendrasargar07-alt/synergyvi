"""
Quantum Feature Sensitivity
============================
Explainability for quantum models using feature perturbation analysis.
This is NOT SHAP — it measures how sensitive the quantum model's prediction
is to changes in each input feature.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


def quantum_feature_sensitivity(
    quantum_model, sample, feature_names=None, delta: float = None
) -> dict:
    """Compute feature sensitivity for a quantum model prediction.

    Method:
        1. Obtain the original prediction probability.
        2. For each feature, perturb it by ±delta.
        3. Measure the change in prediction probability.
        4. Sensitivity = mean of |change| across both perturbation directions.
        5. Rank features by sensitivity.

    This is labeled as 'Quantum Feature Sensitivity', NOT as SHAP.

    Args:
        quantum_model: Trained QuantumClassifier with predict_proba().
        sample: Single sample array (n_quantum_features,).
        feature_names: Optional names for the quantum features.
        delta: Perturbation magnitude. Defaults to config.PERTURBATION_DELTA.

    Returns:
        Dictionary with sensitivity scores, ranking, and raw perturbation results.
    """
    if delta is None:
        delta = config.PERTURBATION_DELTA

    sample = np.atleast_2d(sample).astype(np.float64)
    n_features = sample.shape[1]

    if feature_names is None:
        feature_names = [f"QF{i + 1}" for i in range(n_features)]

    # Original prediction
    original_proba = float(quantum_model.predict_proba(sample)[0])
    original_pred = int(quantum_model.predict(sample)[0])

    sensitivities = []
    perturbation_details = []

    for i in range(n_features):
        # Positive perturbation
        sample_pos = sample.copy()
        sample_pos[0, i] += delta
        proba_pos = float(quantum_model.predict_proba(sample_pos)[0])

        # Negative perturbation
        sample_neg = sample.copy()
        sample_neg[0, i] -= delta
        proba_neg = float(quantum_model.predict_proba(sample_neg)[0])

        # Sensitivity = mean absolute change
        change_pos = abs(proba_pos - original_proba)
        change_neg = abs(proba_neg - original_proba)
        sensitivity = (change_pos + change_neg) / 2.0

        sensitivities.append(sensitivity)
        perturbation_details.append(
            {
                "feature": str(feature_names[i]),
                "original_value": float(sample[0, i]),
                "sensitivity": float(sensitivity),
                "proba_positive_perturb": float(proba_pos),
                "proba_negative_perturb": float(proba_neg),
                "change_positive": float(change_pos),
                "change_negative": float(change_neg),
            }
        )

    # Rank by sensitivity (descending)
    ranking_indices = np.argsort(sensitivities)[::-1]
    ranking = [
        {
            "rank": rank + 1,
            "feature": str(feature_names[idx]),
            "sensitivity": float(sensitivities[idx]),
        }
        for rank, idx in enumerate(ranking_indices)
    ]

    return {
        "method": "Quantum Feature Sensitivity (Perturbation Analysis)",
        "original_prediction": original_pred,
        "original_probability": original_proba,
        "delta": delta,
        "sensitivities": {
            str(feature_names[i]): float(sensitivities[i]) for i in range(n_features)
        },
        "ranking": ranking,
        "details": perturbation_details,
    }


def plot_quantum_sensitivity(sensitivity_result: dict):
    """Generate a bar chart of quantum feature sensitivity.

    Args:
        sensitivity_result: Output from quantum_feature_sensitivity().

    Returns:
        Plotly figure object.
    """
    import plotly.graph_objects as go

    ranking = sensitivity_result["ranking"]
    features = [r["feature"] for r in ranking][::-1]
    values = [r["sensitivity"] for r in ranking][::-1]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=features,
            orientation="h",
            marker_color="#8b5cf6",
        )
    )
    fig.update_layout(
        title="Quantum Feature Sensitivity",
        xaxis_title="Sensitivity Score",
        yaxis_title="Feature",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=250 + len(features) * 40,
    )
    return fig


def plot_perturbation_details(sensitivity_result: dict):
    """Generate a detailed perturbation chart showing positive/negative changes.

    Args:
        sensitivity_result: Output from quantum_feature_sensitivity().

    Returns:
        Plotly figure object.
    """
    import plotly.graph_objects as go

    details = sensitivity_result["details"]
    features = [d["feature"] for d in details]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="+δ perturbation",
            x=features,
            y=[d["change_positive"] for d in details],
            marker_color="#6366f1",
        )
    )
    fig.add_trace(
        go.Bar(
            name="−δ perturbation",
            x=features,
            y=[d["change_negative"] for d in details],
            marker_color="#a78bfa",
        )
    )
    fig.update_layout(
        title="Perturbation Impact by Direction",
        xaxis_title="Feature",
        yaxis_title="|Δ Probability|",
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
    )
    return fig
