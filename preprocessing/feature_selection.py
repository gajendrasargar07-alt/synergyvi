import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config
from sklearn.decomposition import PCA
import numpy as np
import joblib
from typing import Dict, Any

def fit_pca(X_train: np.ndarray, n_components: int) -> PCA:
    """
    Fits PCA on the scaled training data.
    """
    pca = PCA(n_components=n_components)
    pca.fit(X_train)
    return pca

def transform_pca(pca: PCA, X: np.ndarray) -> np.ndarray:
    """
    Transforms the data using the fitted PCA.
    """
    return pca.transform(X)

def prepare_quantum_features(X: np.ndarray, n_quantum_features: int) -> np.ndarray:
    """
    Selects the top n_quantum_features components from the PCA-transformed data.
    """
    if X.shape[1] < n_quantum_features:
        raise ValueError(f"Input features {X.shape[1]} are less than n_quantum_features {n_quantum_features}")
    return X[:, :n_quantum_features]

def save_pca(pca: PCA) -> None:
    """
    Saves the fitted PCA object to config.PCA_FILE.
    """
    try:
        os.makedirs(os.path.dirname(config.PCA_FILE), exist_ok=True)
        joblib.dump(pca, config.PCA_FILE)
        print(f"PCA saved to {config.PCA_FILE}")
    except Exception as e:
        print(f"Error saving PCA: {e}")
        raise

def load_pca() -> PCA:
    """
    Loads the fitted PCA object from config.PCA_FILE.
    """
    try:
        pca = joblib.load(config.PCA_FILE)
        return pca
    except Exception as e:
        print(f"Error loading PCA: {e}")
        raise

def get_pca_info(pca: PCA) -> Dict[str, Any]:
    """
    Returns information about the fitted PCA.
    """
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(explained_variance)
    
    return {
        "explained_variance_ratio": explained_variance.tolist(),
        "n_components": pca.n_components_,
        "cumulative_variance": cumulative_variance.tolist()
    }
