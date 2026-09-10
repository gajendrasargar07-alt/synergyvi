"""
Classical ML Tests
==================
Tests for classical model training, prediction, and evaluation.
"""

import sys
import os
import pytest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


@pytest.fixture(scope="module")
def processed_data():
    """Load preprocessed data for testing."""
    from preprocessing.pipeline import run_preprocessing_pipeline
    return run_preprocessing_pipeline()


class TestClassicalTraining:
    """Test classical model training."""

    def test_train_logistic_regression(self, processed_data):
        from classical.train import train_logistic_regression

        model, train_time = train_logistic_regression(
            processed_data["X_train"], processed_data["y_train"]
        )
        assert model is not None
        assert train_time >= 0

    def test_train_svm(self, processed_data):
        from classical.train import train_svm

        model, train_time = train_svm(
            processed_data["X_train"], processed_data["y_train"]
        )
        assert model is not None
        assert train_time >= 0

    def test_train_random_forest(self, processed_data):
        from classical.train import train_random_forest

        model, train_time = train_random_forest(
            processed_data["X_train"], processed_data["y_train"]
        )
        assert model is not None
        assert train_time >= 0

    def test_train_xgboost(self, processed_data):
        from classical.train import train_xgboost

        model, train_time = train_xgboost(
            processed_data["X_train"], processed_data["y_train"]
        )
        assert model is not None
        assert train_time >= 0


class TestClassicalPredictions:
    """Test classical model predictions."""

    def test_predictions_format(self, processed_data):
        from classical.train import train_logistic_regression
        from classical.predict import predict, predict_proba

        model, _ = train_logistic_regression(
            processed_data["X_train"], processed_data["y_train"]
        )
        X_test = processed_data["X_test"]

        preds = predict(model, X_test)
        assert preds.shape == (len(X_test),)
        assert set(np.unique(preds)).issubset({0, 1})

        probas = predict_proba(model, X_test)
        assert probas.shape[0] == len(X_test)
        assert np.all(probas >= 0) and np.all(probas <= 1)


class TestClassicalEvaluation:
    """Test classical model evaluation."""

    def test_evaluate_model(self, processed_data):
        from classical.train import train_logistic_regression
        from classical.predict import predict, predict_proba
        from classical.evaluate import evaluate_model

        model, _ = train_logistic_regression(
            processed_data["X_train"], processed_data["y_train"]
        )
        X_test = processed_data["X_test"]
        y_test = processed_data["y_test"]

        preds = predict(model, X_test)
        probas = predict_proba(model, X_test)

        metrics = evaluate_model(y_test, preds, probas[:, 1] if probas.ndim > 1 else probas)

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["f1"] <= 1
