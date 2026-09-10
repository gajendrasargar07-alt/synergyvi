import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

import pennylane as qml
from pennylane import numpy as pnp
import numpy as np
from quantum.circuit import get_qnode

class QuantumClassifier:
    def __init__(self, n_qubits=None, n_layers=None, learning_rate=None, epochs=None, batch_size=None):
        self.n_qubits = n_qubits if n_qubits is not None else config.N_QUBITS
        self.n_layers = n_layers if n_layers is not None else config.N_QUANTUM_LAYERS
        self.learning_rate = learning_rate if learning_rate is not None else config.QUANTUM_LEARNING_RATE
        self.epochs = epochs if epochs is not None else config.QUANTUM_EPOCHS
        self.batch_size = batch_size if batch_size is not None else config.QUANTUM_BATCH_SIZE
        self.qnode = get_qnode(self.n_qubits, self.n_layers)
        self.params = None
        
    def _initialize_params(self):
        """Random initial parameters with shape (n_layers, n_qubits, 2)"""
        return pnp.random.uniform(0, pnp.pi, (self.n_layers, self.n_qubits, 2), requires_grad=True)

    def _cost(self, params, X, y):
        """Binary cross-entropy-like cost function using circuit output"""
        predictions = [self.qnode(params, x) for x in X]
        # output is in [-1, 1]. Map to probability: p = (1 - output) / 2
        probs = [(1.0 - pred) / 2.0 for pred in predictions]
        eps = 1e-10
        cost = 0.0
        for i in range(len(y)):
            p = pnp.clip(probs[i], eps, 1.0 - eps)
            cost -= y[i] * pnp.log(p) + (1 - y[i]) * pnp.log(1 - p)
        return cost / len(y)

    def fit(self, X_train, y_train, X_val=None, y_val=None, verbose=True):
        """Train with NesterovMomentumOptimizer. Track loss history. Return self."""
        X_train = np.asarray(X_train)
        y_train = np.asarray(y_train)
        if X_val is not None:
            X_val = np.asarray(X_val)
        if y_val is not None:
            y_val = np.asarray(y_val)

        opt = qml.NesterovMomentumOptimizer(stepsize=self.learning_rate)
        self.params = self._initialize_params()
        
        loss_history = []
        n_samples = len(X_train)
        
        for epoch in range(self.epochs):
            indices = np.random.permutation(n_samples)
            X_shuffle = X_train[indices]
            y_shuffle = y_train[indices]
            
            for i in range(0, n_samples, self.batch_size):
                X_batch = X_shuffle[i:i + self.batch_size]
                y_batch = y_shuffle[i:i + self.batch_size]
                
                self.params, cost = opt.step_and_cost(
                    lambda p: self._cost(p, X_batch, y_batch), 
                    self.params
                )
            
            loss = self._cost(self.params, X_train, y_train)
            loss_history.append(loss)
            
            if verbose and (epoch + 1) % 5 == 0:
                print(f"Epoch {epoch + 1}/{self.epochs} - Loss: {loss:.4f}")
                
        return self

    def predict_raw(self, X):
        """Raw circuit outputs for each sample"""
        if self.params is None:
            raise ValueError("Model is not trained. Call fit or load_params first.")
        return pnp.array([self.qnode(self.params, x) for x in X])

    def predict_proba(self, X):
        """Map circuit output [-1,1] to [0,1] probabilities"""
        raw_outputs = self.predict_raw(X)
        probs = (1.0 - raw_outputs) / 2.0
        # Return as (N, 2) shaped probabilities for binary classification consistency
        return np.column_stack((1 - probs, probs))

    def predict(self, X, threshold=0.5):
        """Binary predictions"""
        probs = self.predict_proba(X)[:, 1]
        return (probs >= threshold).astype(int)

    def save_params(self, path=None):
        """Save params to config.QUANTUM_PARAMS_FILE using np.save"""
        if path is None:
            path = config.QUANTUM_PARAMS_FILE
        if self.params is None:
            raise ValueError("No parameters to save.")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.save(path, self.params)

    def load_params(self, path=None):
        """Load params from config.QUANTUM_PARAMS_FILE"""
        if path is None:
            path = config.QUANTUM_PARAMS_FILE
        if not os.path.exists(path):
            raise FileNotFoundError(f"Parameters file not found at {path}")
        self.params = pnp.array(np.load(path), requires_grad=True)

    def is_trained(self, path=None):
        """Returns True if params file exists"""
        if path is None:
            path = config.QUANTUM_PARAMS_FILE
        return os.path.exists(path)
