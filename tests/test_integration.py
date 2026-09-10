"""
Integration Tests
=================
Tests for the full pipeline, benchmarking, and IBM Quantum fallback.
"""

import sys
import os
import pytest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


class TestIntegration:
    """Test integration pipeline."""

    def test_inference_with_no_models(self):
        """Inference should handle missing models gracefully."""
        from integration.pipeline import run_inference

        # Use a dummy feature vector
        features = np.random.randn(30)
        result = run_inference(features, use_quantum=False)

        # Should not crash even if models aren't trained
        assert isinstance(result, dict)

    def test_benchmark_loading(self):
        """Benchmark loading should return dict even if no results."""
        from integration.pipeline import load_benchmark_results

        results = load_benchmark_results()
        assert isinstance(results, dict)


class TestIBMQuantum:
    """Test IBM Quantum integration without credentials."""

    def test_check_credentials_without_env(self):
        """Should report unavailable without crashing."""
        from integration.quantum_hardware import check_ibm_credentials

        # Remove env vars if set (save and restore)
        old_token = os.environ.pop(config.IBM_QUANTUM_TOKEN_ENV, None)
        try:
            creds = check_ibm_credentials()
            assert creds["available"] is False
        finally:
            if old_token:
                os.environ[config.IBM_QUANTUM_TOKEN_ENV] = old_token

    def test_backend_info_without_credentials(self):
        """Should return info dict without crashing."""
        from integration.quantum_hardware import get_backend_info

        old_token = os.environ.pop(config.IBM_QUANTUM_TOKEN_ENV, None)
        try:
            info = get_backend_info()
            assert "local_simulator" in info
            assert info["local_simulator"]["status"] == "Available"
            assert info["ibm_quantum"]["status"] == "Not Configured"
        finally:
            if old_token:
                os.environ[config.IBM_QUANTUM_TOKEN_ENV] = old_token

    def test_get_ibm_backend_without_credentials(self):
        """Should raise RuntimeError without credentials."""
        from integration.quantum_hardware import get_ibm_backend

        old_token = os.environ.pop(config.IBM_QUANTUM_TOKEN_ENV, None)
        try:
            with pytest.raises(RuntimeError):
                get_ibm_backend()
        finally:
            if old_token:
                os.environ[config.IBM_QUANTUM_TOKEN_ENV] = old_token
