import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config
import joblib
import json
from quantum.quantum_model import QuantumClassifier
from quantum.evaluate import evaluate_quantum, save_quantum_metrics

def main():
    print("Loading processed data...")
    if not os.path.exists(config.PROCESSED_DATA_FILE):
        raise FileNotFoundError("Processed data not found. Please run preprocessing first.")
    
    data = joblib.load(config.PROCESSED_DATA_FILE)
    X_train = data['X_train_quantum']
    y_train = data['y_train']
    X_test = data['X_test_quantum']
    y_test = data['y_test']
    
    print(f"Training Quantum Classifier on {X_train.shape[0]} samples...")
    model = QuantumClassifier()
    model.fit(X_train, y_train, verbose=True)
    
    print("Saving model parameters...")
    model.save_params()
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = evaluate_quantum(y_test, y_pred, y_proba)
    save_quantum_metrics(metrics)
    
    print("Training Complete. Metrics:")
    print(json.dumps(metrics, indent=4))

if __name__ == "__main__":
    main()
