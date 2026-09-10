import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

import pennylane as qml
import numpy as np

def create_device(n_qubits: int):
    """Creates qml.device('default.qubit', wires=n_qubits)"""
    return qml.device('default.qubit', wires=n_qubits)

def angle_encoding(features, wires):
    """Applies RX encoding of features to qubits"""
    for i, feature in enumerate(features):
        qml.RX(feature, wires=wires[i])

def variational_layer(params, wires):
    """One variational layer: RY + RZ rotations on each qubit + CNOT entanglement chain"""
    n_qubits = len(wires)
    for i in range(n_qubits):
        qml.RY(params[i, 0], wires=wires[i])
        qml.RZ(params[i, 1], wires=wires[i])
    for i in range(n_qubits - 1):
        qml.CNOT(wires=[wires[i], wires[i+1]])

def quantum_circuit(params, features, wires):
    """Full circuit: angle encoding → variational layers → returns qml.expval(qml.PauliZ(0))"""
    angle_encoding(features, wires)
    n_layers = params.shape[0]
    for layer in range(n_layers):
        variational_layer(params[layer], wires)
    return qml.expval(qml.PauliZ(0))

def get_qnode(n_qubits: int, n_layers: int):
    """Returns a QNode with the circuit, ready for training"""
    dev = create_device(n_qubits)
    wires = list(range(n_qubits))
    
    @qml.qnode(dev)
    def qnode(params, features):
        return quantum_circuit(params, features, wires)
    return qnode

def draw_circuit(n_qubits: int = None, n_layers: int = None) -> str:
    """Returns text representation of the circuit using qml.draw()"""
    if n_qubits is None:
        n_qubits = config.N_QUBITS
    if n_layers is None:
        n_layers = config.N_QUANTUM_LAYERS
    qnode = get_qnode(n_qubits, n_layers)
    params = np.random.uniform(0, np.pi, (n_layers, n_qubits, 2))
    features = np.random.uniform(0, np.pi, (n_qubits,))
    return qml.draw(qnode)(params, features)

def get_circuit_info() -> dict:
    """Returns dict with circuit info."""
    return {
        "n_qubits": config.N_QUBITS,
        "n_layers": config.N_QUANTUM_LAYERS,
        "encoding_method": "Angle Encoding (RX)",
        "gate_types": ["RX", "RY", "RZ", "CNOT"],
        "circuit_depth": config.N_QUANTUM_LAYERS * 3 + 1,
        "backend": "default.qubit"
    }
