"""
Quantum ML Tests
================
Tests for quantum circuit, model, and predictions.
"""

import sys
import os
import pytest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


class TestQuantumCircuit:
    """Test quantum circuit definition."""

    def test_circuit_creation(self):
        from quantum.circuit import get_circuit_info

        info = get_circuit_info()
        assert info["n_qubits"] == config.N_QUBITS
        assert info["n_layers"] == config.N_QUANTUM_LAYERS
        assert "encoding_method" in info

    def test_draw_circuit(self):
        from quantum.circuit import draw_circuit

        diagram = draw_circuit(config.N_QUBITS, config.N_QUANTUM_LAYERS)
        assert isinstance(diagram, str)
        assert len(diagram) > 0


class TestQuantumModel:
    """Test quantum model creation and basic operations."""

    def test_model_creation(self):
        from quantum.quantum_model import QuantumClassifier

        model = QuantumClassifier(
            n_qubits=config.N_QUBITS,
            n_layers=config.N_QUANTUM_LAYERS,
        )
        # Prediction requires fitted or restored variational parameters.
        model.params = model._initialize_params()
        assert model is not None

    def test_prediction_format(self):
        from quantum.quantum_model import QuantumClassifier

        model = QuantumClassifier(
            n_qubits=config.N_QUBITS,
            n_layers=config.N_QUANTUM_LAYERS,
        )
        # Random test input
        X = np.random.randn(5, config.N_QUANTUM_FEATURES)

        preds = model.predict(X)
        assert preds.shape == (5,)
        assert set(np.unique(preds)).issubset({0, 1})

        probas = model.predict_proba(X)
        assert probas.shape == (5, 2)
        assert np.all(probas >= 0) and np.all(probas <= 1)
        assert np.allclose(probas.sum(axis=1), 1.0)


class TestQuantumEvaluation:
    """Test quantum evaluation metrics."""

    def test_evaluate_quantum(self):
        from quantum.evaluate import evaluate_quantum

        y_true = np.array([0, 1, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 0, 1])
        y_proba = np.array([0.2, 0.8, 0.4, 0.3, 0.9])

        metrics = evaluate_quantum(y_true, y_pred, y_proba)

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert "roc_auc" in metrics
        assert 0 <= metrics["accuracy"] <= 1
