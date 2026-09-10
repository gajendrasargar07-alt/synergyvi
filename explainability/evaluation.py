"""
Explainability Evaluation
=========================
Combined explainability report generation for classical and quantum models.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


def generate_explainability_report(
    classical_model,
    quantum_model,
    sample,
    X_background,
    X_quantum_sample,
    model_name: str = "Random Forest",
    feature_names=None,
    quantum_feature_names=None,
) -> dict:
    """Generate a combined explainability report for both classical and quantum models.

    Args:
        classical_model: Trained classical model.
        quantum_model: Trained QuantumClassifier.
        sample: Single sample for classical model (PCA features).
        X_background: Background dataset for SHAP.
        X_quantum_sample: Single sample for quantum model (quantum features).
        model_name: Name of the classical model.
        feature_names: Feature names for classical model.
        quantum_feature_names: Feature names for quantum model.

    Returns:
        Dictionary with both classical and quantum explanations.
    """
    report = {"classical": None, "quantum": None}

    # Classical SHAP explanation
    try:
        from explainability.shap_analysis import explain_single_prediction

        report["classical"] = explain_single_prediction(
            classical_model, sample, X_background, model_name, feature_names
        )
        report["classical"]["method"] = "SHAP (SHapley Additive exPlanations)"
    except Exception as e:
        report["classical"] = {"error": str(e)}

    # Quantum sensitivity explanation
    try:
        from explainability.quantum_explainability import quantum_feature_sensitivity

        report["quantum"] = quantum_feature_sensitivity(
            quantum_model, X_quantum_sample, quantum_feature_names
        )
    except Exception as e:
        report["quantum"] = {"error": str(e)}

    return report


def save_explainability_report(report: dict, filepath: str = None):
    """Save explainability report to JSON.

    Args:
        report: Report dictionary.
        filepath: Output path. Defaults to results/explainability_report.json.
    """
    if filepath is None:
        filepath = os.path.join(config.RESULTS_DIR, "explainability_report.json")

    config.ensure_dirs()

    # Convert numpy types for JSON serialization
    def convert(obj):
        import numpy as np

        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    with open(filepath, "w") as f:
        json.dump(report, f, indent=2, default=convert)


def load_explainability_report(filepath: str = None) -> dict:
    """Load explainability report from JSON.

    Args:
        filepath: Input path. Defaults to results/explainability_report.json.

    Returns:
        Report dictionary, or empty dict if not found.
    """
    if filepath is None:
        filepath = os.path.join(config.RESULTS_DIR, "explainability_report.json")

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
