"""
Integration Pipeline
====================
Unified pipeline connecting preprocessing, classical, and quantum modules.
Provides end-to-end training, inference, and benchmarking functionality.
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


def run_full_pipeline(skip_quantum: bool = False, verbose: bool = True) -> dict:
    """Run the complete training pipeline: preprocessing → classical → quantum → benchmark.

    Args:
        skip_quantum: If True, skip quantum model training.
        verbose: Print progress messages.

    Returns:
        Dictionary with all results.
    """
    from preprocessing.pipeline import run_preprocessing_pipeline
    from classical.train import train_all_classical
    from classical.evaluate import evaluate_all_classical, save_classical_metrics
    from quantum.evaluate import save_quantum_metrics

    config.ensure_dirs()
    results = {}

    # Step 1: Preprocessing
    if verbose:
        print("=" * 60)
        print("PHASE 1: Preprocessing")
        print("=" * 60)
    data = run_preprocessing_pipeline()
    results["dataset_info"] = data["dataset_info"]

    # Step 2: Classical Training
    if verbose:
        print("\n" + "=" * 60)
        print("PHASE 2: Classical Model Training")
        print("=" * 60)
    classical_models = train_all_classical(data["X_train"], data["y_train"])
    results["classical_training"] = {
        name: {"training_time": t} for name, (_, t) in classical_models.items()
    }

    # Step 3: Classical Evaluation
    if verbose:
        print("\n" + "=" * 60)
        print("PHASE 3: Classical Model Evaluation")
        print("=" * 60)
    classical_metrics = evaluate_all_classical(data["X_test"], data["y_test"])
    save_classical_metrics(classical_metrics)

    # Merge training times into metrics
    for name in classical_metrics:
        if name in results["classical_training"]:
            classical_metrics[name]["training_time"] = results["classical_training"][
                name
            ]["training_time"]
    save_classical_metrics(classical_metrics)
    results["classical_metrics"] = classical_metrics

    # Step 4: Quantum Training (optional)
    if not skip_quantum:
        if verbose:
            print("\n" + "=" * 60)
            print("PHASE 4: Quantum Model Training")
            print("=" * 60)
        try:
            from quantum.quantum_model import QuantumClassifier
            from quantum.evaluate import evaluate_quantum

            qc = QuantumClassifier()
            start_time = time.time()
            qc.fit(
                data["X_train_quantum"],
                data["y_train"],
                X_val=data["X_test_quantum"],
                y_val=data["y_test"],
                verbose=verbose,
            )
            q_train_time = time.time() - start_time
            qc.save_params()

            y_pred_q = qc.predict(data["X_test_quantum"])
            y_proba_q = qc.predict_proba(data["X_test_quantum"])
            q_metrics = evaluate_quantum(data["y_test"], y_pred_q, y_proba_q)
            q_metrics["training_time"] = q_train_time
            save_quantum_metrics(q_metrics)
            results["quantum_metrics"] = q_metrics
        except Exception as e:
            if verbose:
                print(f"  [WARNING] Quantum training failed: {e}")
            results["quantum_metrics"] = None
    else:
        if verbose:
            print("\n  Skipping quantum model training.")
        results["quantum_metrics"] = None

    # Step 5: Benchmark
    if verbose:
        print("\n" + "=" * 60)
        print("PHASE 5: Generating Benchmark")
        print("=" * 60)
    benchmark = generate_benchmark_report()
    results["benchmark"] = benchmark

    if verbose:
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)

    return results


def run_inference(features, use_quantum: bool = True) -> dict:
    """Run inference on a single sample or batch using all available models.

    Args:
        features: Raw feature array (n_features,) or (n_samples, n_features).
        use_quantum: Whether to include quantum model predictions.

    Returns:
        Dictionary with predictions from each model.
    """
    import numpy as np
    from preprocessing.pipeline import load_processed_data
    from preprocessing.preprocess import load_scaler
    from preprocessing.feature_selection import load_pca

    features = np.atleast_2d(features)
    results = {"classical": {}, "quantum": None, "backend": "Local Simulator"}

    # Preprocess the input
    try:
        scaler = load_scaler()
        pca = load_pca()
        features_scaled = scaler.transform(features)
        features_pca = pca.transform(features_scaled)
        features_quantum = features_pca[:, : config.N_QUANTUM_FEATURES]
    except Exception as e:
        return {"error": f"Preprocessing failed: {e}"}

    # Classical predictions
    from classical.predict import predict, predict_proba
    from classical.train import load_model

    for name in config.CLASSICAL_MODEL_NAMES:
        try:
            model = load_model(name)
            pred = predict(model, features_pca)
            try:
                proba = predict_proba(model, features_pca)
            except Exception:
                proba = None
            results["classical"][name] = {
                "prediction": int(pred[0]),
                "label": "Malignant" if pred[0] == 0 else "Benign",
                "probability": float(proba[0][1]) if proba is not None else None,
            }
        except FileNotFoundError:
            results["classical"][name] = {"error": "Model not trained"}

    # Quantum prediction
    if use_quantum:
        try:
            from quantum.predict import load_quantum_model, is_quantum_model_trained

            if is_quantum_model_trained():
                qm = load_quantum_model()
                q_pred = qm.predict(features_quantum)
                q_proba = qm.predict_proba(features_quantum)
                results["quantum"] = {
                    "prediction": int(q_pred[0]),
                    "label": "Malignant" if q_pred[0] == 0 else "Benign",
                    # QuantumClassifier follows the scikit-learn convention:
                    # columns are class 0 then class 1 probabilities.
                    "probability": float(q_proba[0, 1]),
                    "backend": "Local Simulator",
                }
            else:
                results["quantum"] = {
                    "error": "Quantum model not trained. Run the training pipeline first."
                }
        except Exception as e:
            results["quantum"] = {"error": f"Quantum inference failed: {e}"}

    return results


def generate_benchmark_report() -> dict:
    """Generate a unified benchmark report comparing all models.

    Returns:
        Dictionary with benchmark data and saves to config.BENCHMARK_FILE.
    """
    benchmark = {"models": {}, "generated_at": None}

    # Load classical metrics
    try:
        from classical.evaluate import load_classical_metrics

        classical = load_classical_metrics()
        for name, metrics in classical.items():
            benchmark["models"][name] = {
                "type": "classical",
                **metrics,
            }
    except Exception:
        pass

    # Load quantum metrics
    try:
        from quantum.evaluate import load_quantum_metrics

        quantum = load_quantum_metrics()
        if quantum:
            benchmark["models"]["Variational Quantum Classifier"] = {
                "type": "quantum",
                **quantum,
            }
    except Exception:
        pass

    # Add timestamp
    from datetime import datetime

    benchmark["generated_at"] = datetime.now().isoformat()

    # Save
    config.ensure_dirs()
    with open(config.BENCHMARK_FILE, "w") as f:
        json.dump(benchmark, f, indent=2, default=str)
    print(f"  Benchmark saved to {config.BENCHMARK_FILE}")

    return benchmark


def load_benchmark_results() -> dict:
    """Load benchmark results from disk.

    Returns:
        Benchmark dictionary, or empty dict if not found.
    """
    try:
        with open(config.BENCHMARK_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Q-Dx Full Pipeline")
    parser.add_argument(
        "--skip-quantum", action="store_true", help="Skip quantum model training"
    )
    args = parser.parse_args()
    run_full_pipeline(skip_quantum=args.skip_quantum)
