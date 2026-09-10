"""
Preprocessing Tests
===================
Tests for dataset loading, preprocessing, and feature selection.
"""

import sys
import os
import pytest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


class TestDataLoading:
    """Test dataset loading functionality."""

    def test_load_dataset(self):
        from preprocessing.load_data import load_dataset

        X, y, meta = load_dataset()
        assert X.shape[0] == 569, "Expected 569 samples"
        assert X.shape[1] == 30, "Expected 30 features"
        assert len(y) == 569, "Target length must match samples"
        assert set(y.unique()) == {0, 1}, "Expected binary classification"

    def test_get_dataset_info(self):
        from preprocessing.load_data import get_dataset_info

        info = get_dataset_info()
        assert info["n_samples"] == 569
        assert info["n_features"] == 30
        assert len(info["feature_names"]) == 30
        assert len(info["target_names"]) == 2
        assert "class_distribution" in info


class TestPreprocessing:
    """Test preprocessing functionality."""

    def test_split_dataset(self):
        from preprocessing.load_data import load_dataset
        from preprocessing.preprocess import split_dataset

        X, y, _ = load_dataset()
        X_train, X_test, y_train, y_test = split_dataset(
            X, y, config.TEST_SIZE, config.RANDOM_SEED
        )

        total = len(X_train) + len(X_test)
        assert total == 569, "Split must preserve all samples"
        assert len(X_test) == pytest.approx(569 * config.TEST_SIZE, abs=2)

    def test_stratified_split(self):
        from preprocessing.load_data import load_dataset
        from preprocessing.preprocess import split_dataset

        X, y, _ = load_dataset()
        _, _, y_train, y_test = split_dataset(X, y, config.TEST_SIZE, config.RANDOM_SEED)

        # Check approximate stratification
        train_ratio = y_train.mean()
        test_ratio = y_test.mean()
        assert abs(train_ratio - test_ratio) < 0.05, "Split should be approximately stratified"

    def test_scaler_fit_transform(self):
        from preprocessing.load_data import load_dataset
        from preprocessing.preprocess import split_dataset, fit_scaler, transform_data

        X, y, _ = load_dataset()
        X_train, X_test, _, _ = split_dataset(X, y, config.TEST_SIZE, config.RANDOM_SEED)

        scaler = fit_scaler(X_train)
        X_train_scaled = transform_data(scaler, X_train)
        X_test_scaled = transform_data(scaler, X_test)

        # Training data should be approximately standardized
        assert np.abs(X_train_scaled.mean()) < 0.1
        assert X_train_scaled.shape == X_train.shape
        assert X_test_scaled.shape == X_test.shape


class TestFeatureSelection:
    """Test PCA and quantum feature preparation."""

    def test_pca_fit_transform(self):
        from preprocessing.load_data import load_dataset
        from preprocessing.preprocess import split_dataset, fit_scaler, transform_data
        from preprocessing.feature_selection import fit_pca, transform_pca

        X, y, _ = load_dataset()
        X_train, _, _, _ = split_dataset(X, y, config.TEST_SIZE, config.RANDOM_SEED)
        scaler = fit_scaler(X_train)
        X_train_scaled = transform_data(scaler, X_train)

        pca = fit_pca(X_train_scaled, config.N_PCA_COMPONENTS)
        X_pca = transform_pca(pca, X_train_scaled)

        assert X_pca.shape[1] == config.N_PCA_COMPONENTS

    def test_quantum_features(self):
        from preprocessing.load_data import load_dataset
        from preprocessing.preprocess import split_dataset, fit_scaler, transform_data
        from preprocessing.feature_selection import (
            fit_pca, transform_pca, prepare_quantum_features,
        )

        X, y, _ = load_dataset()
        X_train, _, _, _ = split_dataset(X, y, config.TEST_SIZE, config.RANDOM_SEED)
        scaler = fit_scaler(X_train)
        X_train_scaled = transform_data(scaler, X_train)

        pca = fit_pca(X_train_scaled, config.N_PCA_COMPONENTS)
        X_pca = transform_pca(pca, X_train_scaled)
        X_quantum = prepare_quantum_features(X_pca, config.N_QUANTUM_FEATURES)

        assert X_quantum.shape[1] == config.N_QUANTUM_FEATURES
        assert X_quantum.shape[1] == config.N_QUBITS


class TestPipeline:
    """Test end-to-end preprocessing pipeline."""

    def test_run_pipeline(self):
        from preprocessing.pipeline import run_preprocessing_pipeline

        data = run_preprocessing_pipeline()

        assert "X_train" in data
        assert "X_test" in data
        assert "y_train" in data
        assert "y_test" in data
        assert "X_train_quantum" in data
        assert "X_test_quantum" in data

        assert data["X_train_quantum"].shape[1] == config.N_QUANTUM_FEATURES
        assert data["X_test_quantum"].shape[1] == config.N_QUANTUM_FEATURES
