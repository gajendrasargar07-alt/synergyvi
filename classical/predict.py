import sys, os
import joblib
import numpy as np
from typing import Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config

def predict(model: Any, X: np.ndarray) -> np.ndarray:
    """Predict class labels for X."""
    return model.predict(X)

def predict_proba(model: Any, X: np.ndarray) -> np.ndarray:
    """Predict class probabilities for X."""
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)
    else:
        # Fallback if predict_proba is not available
        preds = model.predict(X)
        probs = np.zeros((len(preds), 2))
        for i, p in enumerate(preds):
            probs[i, int(p)] = 1.0
        return probs

def predict_with_model_name(name: str, X: np.ndarray) -> np.ndarray:
    """Load model by name and predict class labels."""
    if name not in config.CLASSICAL_MODEL_FILES:
        raise ValueError(f"Model name {name} not found in config.")
    filepath = os.path.join(config.CLASSICAL_MODELS_DIR, config.CLASSICAL_MODEL_FILES[name])
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found at {filepath}")
    model = joblib.load(filepath)
    return predict(model, X)

def predict_all(X: np.ndarray) -> Dict[str, np.ndarray]:
    """Load all classical models and return a dictionary of predictions."""
    predictions = {}
    for name in config.CLASSICAL_MODEL_NAMES:
        try:
            predictions[name] = predict_with_model_name(name, X)
        except Exception as e:
            print(f"Error predicting with {name}: {e}")
    return predictions
