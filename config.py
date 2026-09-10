"""
Q-Dx Configuration
==================
Central configuration for the Hybrid Quantum ML Platform.
All constants used across modules are defined here.
"""

import os

# ── Project Paths ──────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DATA_RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
CLASSICAL_MODELS_DIR = os.path.join(PROJECT_ROOT, "classical", "models")
QUANTUM_DIR = os.path.join(PROJECT_ROOT, "quantum")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

# ── Random Seed ────────────────────────────────────────────────────────────────
RANDOM_SEED = 42

# ── Dataset ────────────────────────────────────────────────────────────────────
DATASET_NAME = "Wisconsin Breast Cancer"
TEST_SIZE = 0.2

# ── Feature Selection / PCA ───────────────────────────────────────────────────
N_PCA_COMPONENTS = 10  # For classical models
N_QUANTUM_FEATURES = 4  # For quantum model (top PCA components)

# ── Classical Models ───────────────────────────────────────────────────────────
CLASSICAL_MODEL_NAMES = [
    "Logistic Regression",
    "SVM",
    "Random Forest",
    "XGBoost",
]

CLASSICAL_MODEL_FILES = {
    "Logistic Regression": "logistic_regression.joblib",
    "SVM": "svm.joblib",
    "Random Forest": "random_forest.joblib",
    "XGBoost": "xgboost.joblib",
}

# ── Quantum Model ──────────────────────────────────────────────────────────────
N_QUBITS = 4
N_QUANTUM_LAYERS = 2
QUANTUM_LEARNING_RATE = 0.01
QUANTUM_EPOCHS = 60
QUANTUM_BATCH_SIZE = 32
QUANTUM_PARAMS_FILE = os.path.join(RESULTS_DIR, "quantum_params.npy")

# ── Preprocessing Artifacts ────────────────────────────────────────────────────
SCALER_FILE = os.path.join(DATA_PROCESSED_DIR, "scaler.joblib")
PCA_FILE = os.path.join(DATA_PROCESSED_DIR, "pca.joblib")
PROCESSED_DATA_FILE = os.path.join(DATA_PROCESSED_DIR, "processed_data.joblib")

# ── Results Files ──────────────────────────────────────────────────────────────
CLASSICAL_METRICS_FILE = os.path.join(RESULTS_DIR, "classical_metrics.json")
QUANTUM_METRICS_FILE = os.path.join(RESULTS_DIR, "quantum_metrics.json")
BENCHMARK_FILE = os.path.join(RESULTS_DIR, "benchmark.json")

# ── IBM Quantum ────────────────────────────────────────────────────────────────
IBM_QUANTUM_TOKEN_ENV = "IBM_QUANTUM_TOKEN"
IBM_QUANTUM_INSTANCE_ENV = "IBM_QUANTUM_INSTANCE"

# ── Explainability ─────────────────────────────────────────────────────────────
SHAP_BACKGROUND_SAMPLES = 50
PERTURBATION_DELTA = 0.1

# ── Dashboard ──────────────────────────────────────────────────────────────────
APP_NAME = "Q-Dx"
APP_SUBTITLE = "Hybrid Quantum Intelligence for Early Disease Detection"
APP_TAGLINE = "Early detection, reimagined through hybrid intelligence."
DISCLAIMER = (
    "Research prototype. This prediction is not a medical diagnosis. "
    "Q-Dx is an experimental research platform and must not be used "
    "for clinical decision-making."
)


def ensure_dirs():
    """Create all required directories if they don't exist."""
    for d in [
        DATA_RAW_DIR,
        DATA_PROCESSED_DIR,
        CLASSICAL_MODELS_DIR,
        RESULTS_DIR,
    ]:
        os.makedirs(d, exist_ok=True)
