import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import streamlit as st
import config
from dashboard.components.ui import *
from dashboard.components.theme import *

import quantum.predict
import quantum.evaluate

def render_quantum_lab():
    section_header('Quantum Lab', 'Variational Quantum Circuit for Biomedical Classification')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card('Qubits', config.N_QUBITS)
    with col2:
        metric_card('Layers', config.N_QUANTUM_LAYERS)
    with col3:
        metric_card('Encoding', 'Angle (RX)')
    with col4:
        metric_card('Backend', 'default.qubit')
        
    st.markdown("""
    <div style="display: flex; justify-content: space-around; align-items: center; padding: 20px; background: #1a1a28; border-radius: 12px; margin-bottom: 20px; border: 1px solid #2a2a3e; color: #e8e8f0; font-weight: 500;">
        <div style="padding: 10px; border: 1px solid #6366f1; border-radius: 8px; background: rgba(99, 102, 241, 0.1);">Input Encoding</div>
        <div style="color: #6366f1;">➔</div>
        <div style="padding: 10px; border: 1px solid #6366f1; border-radius: 8px; background: rgba(99, 102, 241, 0.1);">Variational Layers</div>
        <div style="color: #6366f1;">➔</div>
        <div style="padding: 10px; border: 1px solid #6366f1; border-radius: 8px; background: rgba(99, 102, 241, 0.1);">Measurement</div>
        <div style="color: #6366f1;">➔</div>
        <div style="padding: 10px; border: 1px solid #6366f1; border-radius: 8px; background: rgba(99, 102, 241, 0.1);">Prediction</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3>Circuit Visualization</h3>', unsafe_allow_html=True)
    try:
        import quantum.circuit
        circuit_text = quantum.circuit.draw_circuit()
        quantum_circuit_panel(circuit_text)
    except Exception:
        explanation_panel("Circuit Description", "The circuit uses RX gates for angle encoding, trainable RY/RZ rotations with a CNOT entanglement chain, and a Pauli-Z measurement.")
        
    st.markdown('<h3>Circuit Properties</h3>', unsafe_allow_html=True)
    try:
        import quantum.circuit
        props = quantum.circuit.get_circuit_info()
        st.json(props)
    except Exception:
        st.write("Encoding method: Angle (RX)")
        st.write("Gate types: RX, CNOT, Rot")
        st.write("Measurement basis: Pauli-Z")
        
    st.markdown('<h3>Quantum Model Status</h3>', unsafe_allow_html=True)
    try:
        if quantum.predict.is_quantum_model_trained():
            st.markdown(status_badge('Trained', 'success'), unsafe_allow_html=True)
            metrics = quantum.evaluate.load_quantum_metrics()
            st.json(metrics)
        else:
            st.markdown(status_badge('Not Trained', 'warning'), unsafe_allow_html=True)
            st.write("The quantum model has not been trained yet.")
    except Exception as e:
        error_state(str(e))
