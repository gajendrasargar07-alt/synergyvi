import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import streamlit as st
import config
from dashboard.components.ui import *
from dashboard.components.theme import *

def render_quantum_hardware():
    section_header('Quantum Hardware', 'Execution backends for quantum model inference')
    
    st.markdown('<h3>Local Simulator</h3>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="qdx-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-size: 1.1rem;">default.qubit (PennyLane)</strong>
            {status_badge('Available', 'success')}
        </div>
        <div style="color:{TEXT_SECONDARY}; font-size: 0.9rem; margin-top: 10px;">Type: Local Simulator</div>
        <div style="color:{TEXT_SECONDARY}; font-size: 0.9rem;">Qubits: {config.N_QUBITS}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3>IBM Quantum</h3>', unsafe_allow_html=True)
    try:
        import integration.quantum_hardware
        credentials = integration.quantum_hardware.check_ibm_credentials()
        
        if credentials["available"]:
            info = integration.quantum_hardware.get_backend_info()
            ibm_info = info["ibm_quantum"]
            st.markdown(f"""
            <div class="qdx-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="font-size: 1.1rem;">{ibm_info.get('name', 'IBM Quantum Backend')}</strong>
                    {status_badge(ibm_info.get('status', 'Unavailable'), 'success' if ibm_info.get('status') == 'Available' else 'warning')}
                </div>
                <div style="color:{TEXT_SECONDARY}; font-size: 0.9rem; margin-top: 10px;">Qubits: {ibm_info.get('n_qubits', 'Unknown')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(status_badge('Not Configured', 'warning'), unsafe_allow_html=True)
            explanation_panel(
                "Configuration Required", 
                "IBM Quantum hardware is not currently configured. Set the IBM_QUANTUM_TOKEN environment variable to enable hardware execution."
            )
            
    except Exception as e:
        error_state(str(e))
        
    st.markdown(f"""
    <div style="color:{TEXT_SECONDARY}; font-size: 0.9rem; margin-top: 20px; font-style: italic;">
        Note: The rest of the application works fully without IBM Quantum credentials.
    </div>
    """, unsafe_allow_html=True)
