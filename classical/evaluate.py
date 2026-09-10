import sys, os
import json
import joblib
import numpy as np
from typing import Dict, Any, Optional

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config
from predict import predict, predict_proba

def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, y_proba: Optional[np.ndarray] = None) -> Dict[str, Optional[float]]:
    """Evaluate model predictions returning common metrics."""
    metrics = {
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'precision': float(precision_score(y_true, y_pred, zero_division=0)),
        'recall': float(recall_score(y_true, y_pred, zero_division=0)),
        'f1': float(f1_score(y_true, y_pred, zero_division=0)),
        'roc_auc': None
    }
    
    if y_proba is not None:
        try:
            # Assuming binary classification with positive class at index 1
            if len(y_proba.shape) > 1 and y_proba.shape[1] > 1:
                prob_pos = y_proba[:, 1]
            else:
                prob_pos = y_proba
            metrics['roc_auc'] = float(roc_auc_score(y_true, prob_pos))
        except Exception as e:
            print(f"Warning: ROC AUC calculation failed: {e}")
            metrics['roc_auc'] = None
            
    return metrics

def generate_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Generate confusion matrix."""
    return confusion_matrix(y_true, y_pred)

def generate_roc_data(y_true: np.ndarray, y_proba: np.ndarray) -> Dict[str, Any]:
    """Generate data needed for ROC curve plotting."""
    if len(y_proba.shape) > 1 and y_proba.shape[1] > 1:
        prob_pos = y_proba[:, 1]
    else:
        prob_pos = y_proba
    fpr, tpr, thresholds = roc_curve(y_true, prob_pos)
    return {
        'fpr': fpr.tolist(),
        'tpr': tpr.tolist(),
        'thresholds': thresholds.tolist()
    }

def evaluate_all_classical(X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Dict[str, Optional[float]]]:
    """Load all classical models, evaluate them, and return a dictionary of metrics."""
    all_metrics = {}
    
    for name in config.CLASSICAL_MODEL_NAMES:
        try:
            filepath = os.path.join(config.CLASSICAL_MODELS_DIR, config.CLASSICAL_MODEL_FILES[name])
            if not os.path.exists(filepath):
                print(f"Skipping {name}: file not found.")
                continue
                
            model = joblib.load(filepath)
            
            y_pred = predict(model, X_test)
            y_proba = predict_proba(model, X_test)
            
            metrics = evaluate_model(y_test, y_pred, y_proba)
            all_metrics[name] = metrics
        except Exception as e:
            print(f"Error evaluating {name}: {e}")
            
    return all_metrics

def save_classical_metrics(metrics_dict: Dict[str, Dict[str, Optional[float]]]) -> None:
    """Save metrics dictionary to the configured JSON file."""
    config.ensure_dirs()
    with open(config.CLASSICAL_METRICS_FILE, 'w') as f:
        json.dump(metrics_dict, f, indent=4)

def load_classical_metrics() -> Dict[str, Dict[str, Optional[float]]]:
    """Load metrics dictionary from the configured JSON file."""
    if not os.path.exists(config.CLASSICAL_METRICS_FILE):
        raise FileNotFoundError(f"Metrics file not found at {config.CLASSICAL_METRICS_FILE}")
    with open(config.CLASSICAL_METRICS_FILE, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    try:
        if not os.path.exists(config.PROCESSED_DATA_FILE):
            print(f"Preprocessed data not found at {config.PROCESSED_DATA_FILE}. Cannot evaluate.")
            sys.exit(1)
            
        data = joblib.load(config.PROCESSED_DATA_FILE)
        X_test = data['X_test']
        y_test = data['y_test']
        
        print(f"Loaded test data: {X_test.shape[0]} samples")
        
        metrics = evaluate_all_classical(X_test, y_test)
        save_classical_metrics(metrics)
        
        print("Evaluation completed. Metrics saved.")
        for name, m in metrics.items():
            print(f"{name}:")
            for k, v in m.items():
                print(f"  {k}: {v:.4f}" if v is not None else f"  {k}: None")
    except Exception as e:
        print(f"Error during evaluation: {e}")
