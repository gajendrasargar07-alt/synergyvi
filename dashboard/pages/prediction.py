import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
import config
from dashboard.components.ui import *
from dashboard.components.theme import *

try:
    from sklearn.datasets import load_breast_cancer
    data = load_breast_cancer()
    default_values = data.data.mean(axis=0)
    feature_names = data.feature_names
except Exception:
    default_values = np.zeros(30)
    feature_names = [f"Feature {i+1}" for i in range(30)]

def render_prediction() -> None:
    """Render the prediction page."""
    section_header('Disease Prediction', 'Evaluate a biomedical sample using classical and quantum models.')
    
    # Check if models exist
    models_exist = True
    for model_file in config.CLASSICAL_MODEL_FILES.values():
        if not os.path.exists(os.path.join(config.CLASSICAL_MODELS_DIR, model_file)):
            models_exist = False
            break
            
    if not models_exist:
        empty_state('Run the training pipeline to populate models.')
        return
        
    with st.form("prediction_form"):
        st.markdown("### Enter Feature Values")
        cols = st.columns(3)
        user_inputs = []
        
        for i in range(30):
            with cols[i % 3]:
                val = st.number_input(
                    label=feature_names[i] if i < len(feature_names) else f"Feature {i+1}",
                    value=float(default_values[i]) if i < len(default_values) else 0.0,
                    format="%.4f"
                )
                user_inputs.append(val)
                
        submit = st.form_submit_button("Run Analysis")
        
    if submit:
        try:
            from integration.pipeline import run_inference
            
            with st.spinner("Running inference..."):
                results = run_inference(np.array(user_inputs))
                
            st.markdown("### Classical Predictions")
            classical_cols = st.columns(4)
            classical_results = results.get("classical", {})
            
            for idx, (model_name, pred_data) in enumerate(classical_results.items()):
                with classical_cols[idx % 4]:
                    prediction_card(
                        label=model_name,
                        prediction=pred_data.get("prediction", "Unknown"),
                        probability=pred_data.get("probability", None)
                    )
                    
            st.markdown("### Quantum Prediction")
            quantum_data = results.get("quantum", {})
            prediction_card(
                label="Variational Quantum Classifier (VQC)",
                prediction=quantum_data.get("prediction", "Unknown"),
                probability=quantum_data.get("probability", None),
                backend=quantum_data.get("backend", "Aer Simulator")
            )
            
            disclaimer()
        except ImportError:
            error_state("Failed to import integration pipeline. Ensure it is implemented.")
        except Exception as e:
            error_state(f"An error occurred during prediction: {str(e)}")
