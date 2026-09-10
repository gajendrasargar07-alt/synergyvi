import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config
from quantum.quantum_model import QuantumClassifier

def load_quantum_model():
    """Creates QuantumClassifier, loads saved params, returns model"""
    model = QuantumClassifier()
    model.load_params()
    return model

def quantum_predict(X):
    """Loads model, returns predictions"""
    model = load_quantum_model()
    return model.predict(X)

def quantum_predict_proba(X):
    """Loads model, returns probabilities"""
    model = load_quantum_model()
    return model.predict_proba(X)

def is_quantum_model_trained():
    """Checks if params file exists"""
    model = QuantumClassifier()
    return model.is_trained()
