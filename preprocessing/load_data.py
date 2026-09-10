import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config
from sklearn.datasets import load_breast_cancer
import pandas as pd
from typing import Tuple, Dict, Any

def load_dataset() -> Tuple[pd.DataFrame, pd.Series, Dict[str, Any]]:
    """
    Loads the breast cancer dataset.
    Returns:
        Tuple containing feature DataFrame, target Series, and metadata dictionary.
    """
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="target")
    metadata = {
        "dataset_name": config.DATASET_NAME,
        "feature_names": data.feature_names.tolist(),
        "target_names": data.target_names.tolist(),
        "DESCR": data.DESCR,
    }
    return X, y, metadata

def get_dataset_info() -> Dict[str, Any]:
    """
    Returns information about the dataset.
    """
    data = load_breast_cancer()
    y = pd.Series(data.target)
    class_dist = y.value_counts().to_dict()
    # Map index to target names for class distribution
    class_distribution = {data.target_names[k]: v for k, v in class_dist.items()}
    
    info = {
        "dataset_name": config.DATASET_NAME,
        "n_samples": data.data.shape[0],
        "n_features": data.data.shape[1],
        "feature_names": data.feature_names.tolist(),
        "target_names": data.target_names.tolist(),
        "class_distribution": class_distribution,
    }
    return info

def save_raw_data(df: pd.DataFrame, target: pd.Series, path: str) -> None:
    """
    Saves the features and targets to a CSV file in the specified path.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        combined_df = df.copy()
        combined_df['target'] = target
        combined_df.to_csv(path, index=False)
        print(f"Raw data saved successfully to {path}")
    except Exception as e:
        print(f"Error saving raw data: {e}")
        raise
