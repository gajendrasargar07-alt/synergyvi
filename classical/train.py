import sys, os
import time
import joblib
import numpy as np
from typing import Tuple, Dict, Any

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config

def train_logistic_regression(X_train: np.ndarray, y_train: np.ndarray) -> Tuple[Any, float]:
    """Train a Logistic Regression model."""
    start_time = time.time()
    model = LogisticRegression(max_iter=1000, random_state=config.RANDOM_SEED)
    model.fit(X_train, y_train)
    return model, time.time() - start_time

def train_svm(X_train: np.ndarray, y_train: np.ndarray) -> Tuple[Any, float]:
    """Train a Support Vector Machine model."""
    start_time = time.time()
    model = SVC(kernel='rbf', probability=True, random_state=config.RANDOM_SEED)
    model.fit(X_train, y_train)
    return model, time.time() - start_time

def train_random_forest(X_train: np.ndarray, y_train: np.ndarray) -> Tuple[Any, float]:
    """Train a Random Forest model."""
    start_time = time.time()
    model = RandomForestClassifier(n_estimators=100, random_state=config.RANDOM_SEED)
    model.fit(X_train, y_train)
    return model, time.time() - start_time

def train_xgboost(X_train: np.ndarray, y_train: np.ndarray) -> Tuple[Any, float]:
    """Train an XGBoost model."""
    start_time = time.time()
    model = XGBClassifier(
        n_estimators=100, 
        eval_metric='logloss', 
        random_state=config.RANDOM_SEED, 
        use_label_encoder=False
    )
    model.fit(X_train, y_train)
    return model, time.time() - start_time

def save_model(model: Any, name: str) -> None:
    """Save the model to disk using config paths."""
    config.ensure_dirs()
    if name not in config.CLASSICAL_MODEL_FILES:
        raise ValueError(f"Model name {name} not found in config.")
    filepath = os.path.join(config.CLASSICAL_MODELS_DIR, config.CLASSICAL_MODEL_FILES[name])
    joblib.dump(model, filepath)

def load_model(name: str) -> Any:
    """Load the model from disk using config paths."""
    if name not in config.CLASSICAL_MODEL_FILES:
        raise ValueError(f"Model name {name} not found in config.")
    filepath = os.path.join(config.CLASSICAL_MODELS_DIR, config.CLASSICAL_MODEL_FILES[name])
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found at {filepath}")
    return joblib.load(filepath)

def train_all_classical(X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, Tuple[Any, float]]:
    """Train all classical models and save them."""
    results = {}
    
    print("Training Logistic Regression...")
    lr_model, lr_time = train_logistic_regression(X_train, y_train)
    save_model(lr_model, "Logistic Regression")
    results["Logistic Regression"] = (lr_model, lr_time)
    
    print("Training SVM...")
    svm_model, svm_time = train_svm(X_train, y_train)
    save_model(svm_model, "SVM")
    results["SVM"] = (svm_model, svm_time)
    
    print("Training Random Forest...")
    rf_model, rf_time = train_random_forest(X_train, y_train)
    save_model(rf_model, "Random Forest")
    results["Random Forest"] = (rf_model, rf_time)
    
    print("Training XGBoost...")
    xgb_model, xgb_time = train_xgboost(X_train, y_train)
    save_model(xgb_model, "XGBoost")
    results["XGBoost"] = (xgb_model, xgb_time)
    
    return results

if __name__ == '__main__':
    try:
        if not os.path.exists(config.PROCESSED_DATA_FILE):
            print(f"Preprocessed data not found at {config.PROCESSED_DATA_FILE}. Cannot train.")
            sys.exit(1)
            
        data = joblib.load(config.PROCESSED_DATA_FILE)
        X_train = data['X_train']
        y_train = data['y_train']
        print(f"Loaded training data: {X_train.shape[0]} samples")
        
        results = train_all_classical(X_train, y_train)
        print("Training completed successfully.")
        for name, (_, t) in results.items():
            print(f" - {name}: {t:.4f}s")
    except Exception as e:
        print(f"Error during training: {e}")
