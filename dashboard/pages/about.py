import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
import config
from dashboard.components.ui import *
from dashboard.components.theme import *

def render_about() -> None:
    """Render the about page."""
    section_header('About Q-Dx', 'SIH26139 — Hybrid Quantum Machine Learning Platform for Early Disease Detection')
    
    sections = [
        ("1. Problem Statement", "SIH26139 description. Developing a hybrid quantum-classical machine learning solution for enhanced early disease detection, optimizing both accuracy and computational efficiency."),
        ("2. Problem Description", "Early disease detection challenges. Classical models often struggle with high-dimensional biomedical data and subtle complex correlations, leading to delayed or inaccurate diagnoses."),
        ("3. Proposed Solution", "Hybrid quantum-classical approach. Leveraging the robustness of classical preprocessing and the high-dimensional feature space representation of quantum computing to improve prediction performance."),
        ("4. Dataset", "Wisconsin Breast Cancer dataset. Includes 569 samples, 30 features, and 2 classes (Benign, Malignant), serving as the foundational benchmark for the platform."),
        ("5. Classical Methodology", "Implementation of established machine learning models including Logistic Regression, SVM, Random Forest, and XGBoost to establish baseline performance metrics."),
        ("6. Quantum Methodology", "Variational Quantum Classifier (VQC) using 4 qubits, RX angle encoding, trainable RY/RZ rotations, and a CNOT entanglement chain to learn a decision boundary on the reduced feature space."),
        ("7. Explainability", "Providing interpretability via SHAP values for classical models and perturbation sensitivity analysis for quantum models to ensure clinical trust."),
        ("8. Benchmarking", "Unified evaluation framework ensuring both classical and quantum models are tested on the same data split using rigorous metrics."),
        ("9. Limitations", "Currently operating on simulated quantum backends, restricted to a single dataset, and not yet validated for clinical-grade diagnostic use."),
        ("10. Future Scope", "Expanding to multiple diverse datasets, executing on real quantum hardware, exploring deeper quantum circuits, and undergoing clinical validation.")
    ]
    
    for title, content in sections:
        st.markdown(
            f'''
            <div class="qdx-card">
                <h3 style="color: {ACCENT_LIGHT}; margin-top: 0;">{title}</h3>
                <p style="color: {TEXT_SECONDARY}; line-height: 1.6; margin-bottom: 0;">{content}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
    disclaimer()
