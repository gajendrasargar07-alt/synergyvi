import sys
import os
import json
from typing import Dict, Any, Optional
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

try:
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
except ImportError:
    pass

def evaluate_quantum(y_true, y_pred, y_proba: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """Same metrics as classical: accuracy, precision, recall, f1, roc_auc"""
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0))
    }
    
    if y_proba is not None:
        try:
            # If 2D (n_samples, 2), take the positive class column
            prob_scores = y_proba[:, 1] if getattr(y_proba, "ndim", 1) == 2 else y_proba
            metrics["roc_auc"] = float(roc_auc_score(y_true, prob_scores))
        except Exception:
            metrics["roc_auc"] = None
    else:
        metrics["roc_auc"] = None
        
    return metrics

def save_quantum_metrics(metrics_dict: Dict[str, Any]):
    """Save to config.QUANTUM_METRICS_FILE"""
    os.makedirs(os.path.dirname(config.QUANTUM_METRICS_FILE), exist_ok=True)
    with open(config.QUANTUM_METRICS_FILE, 'w') as f:
        json.dump(metrics_dict, f, indent=4)

def load_quantum_metrics() -> Dict[str, Any]:
    """Load from config.QUANTUM_METRICS_FILE"""
    if not os.path.exists(config.QUANTUM_METRICS_FILE):
        raise FileNotFoundError("Quantum metrics file not found.")
    with open(config.QUANTUM_METRICS_FILE, 'r') as f:
        return json.load(f)
