import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import joblib
from typing import Tuple, Union

def split_dataset(X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray], 
                  test_size: float, random_seed: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Performs a stratified train/test split.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_seed, stratify=y
    )
    return X_train, X_test, y_train, y_test

def fit_scaler(X_train: Union[pd.DataFrame, np.ndarray]) -> StandardScaler:
    """
    Fits a StandardScaler on the training data.
    To prevent data leakage, this must ONLY be fitted on training data.
    """
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler

def transform_data(scaler: StandardScaler, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
    """
    Transforms the provided features using the fitted scaler.
    """
    return scaler.transform(X)

def save_scaler(scaler: StandardScaler) -> None:
    """
    Saves the fitted scaler to the config.SCALER_FILE.
    """
    try:
        os.makedirs(os.path.dirname(config.SCALER_FILE), exist_ok=True)
        joblib.dump(scaler, config.SCALER_FILE)
        print(f"Scaler saved to {config.SCALER_FILE}")
    except Exception as e:
        print(f"Error saving scaler: {e}")
        raise

def load_scaler() -> StandardScaler:
    """
    Loads the fitted scaler from config.SCALER_FILE.
    """
    try:
        scaler = joblib.load(config.SCALER_FILE)
        return scaler
    except Exception as e:
        print(f"Error loading scaler: {e}")
        raise
