import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config
from preprocessing.load_data import load_dataset, get_dataset_info, save_raw_data
from preprocessing.preprocess import split_dataset, fit_scaler, transform_data, save_scaler
from preprocessing.feature_selection import fit_pca, transform_pca, prepare_quantum_features, save_pca
import joblib
from typing import Dict, Any

def run_preprocessing_pipeline() -> Dict[str, Any]:
    """
    Executes the end-to-end preprocessing pipeline:
    1. Load dataset
    2. Split (stratified)
    3. Fit scaler on train, transform both
    4. Fit PCA on train, transform both
    5. Prepare quantum features (top 4 PCA components)
    6. Save all artifacts (scaler, pca, processed data)
    7. Return dictionary with processed artifacts
    """
    # 1. Load dataset
    X, y, metadata = load_dataset()
    dataset_info = get_dataset_info()
    
    # Save raw data for reference
    raw_data_path = os.path.join(config.DATA_RAW_DIR, "raw_data.csv")
    save_raw_data(X, y, raw_data_path)
    
    # 2. Split dataset
    X_train, X_test, y_train, y_test = split_dataset(
        X, y, test_size=config.TEST_SIZE, random_seed=config.RANDOM_SEED
    )
    
    # 3. Fit scaler on train, transform both
    scaler = fit_scaler(X_train)
    X_train_scaled = transform_data(scaler, X_train)
    X_test_scaled = transform_data(scaler, X_test)
    
    # 4. Fit PCA on train, transform both
    pca = fit_pca(X_train_scaled, n_components=config.N_PCA_COMPONENTS)
    X_train_pca = transform_pca(pca, X_train_scaled)
    X_test_pca = transform_pca(pca, X_test_scaled)
    
    # 5. Prepare quantum features
    X_train_quantum = prepare_quantum_features(X_train_pca, config.N_QUANTUM_FEATURES)
    X_test_quantum = prepare_quantum_features(X_test_pca, config.N_QUANTUM_FEATURES)
    
    # Prepare result dictionary
    processed_data = {
        "X_train": X_train_pca,
        "X_test": X_test_pca,
        "y_train": y_train,
        "y_test": y_test,
        "X_train_quantum": X_train_quantum,
        "X_test_quantum": X_test_quantum,
        "feature_names": metadata["feature_names"],
        "dataset_info": dataset_info
    }
    
    # 6. Save all artifacts
    config.ensure_dirs()
    save_scaler(scaler)
    save_pca(pca)
    
    try:
        joblib.dump(processed_data, config.PROCESSED_DATA_FILE)
        print(f"Processed data saved to {config.PROCESSED_DATA_FILE}")
    except Exception as e:
        print(f"Error saving processed data: {e}")
        raise
        
    return processed_data

def load_processed_data() -> Dict[str, Any]:
    """
    Loads saved processed data from config.PROCESSED_DATA_FILE.
    """
    try:
        data = joblib.load(config.PROCESSED_DATA_FILE)
        return data
    except Exception as e:
        print(f"Error loading processed data: {e}")
        raise

if __name__ == '__main__':
    run_preprocessing_pipeline()
