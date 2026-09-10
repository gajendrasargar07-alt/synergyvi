import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import streamlit as st
import config
from dashboard.components.ui import *
from dashboard.components.theme import *

import classical.train
import preprocessing.pipeline
import explainability.shap_analysis
import explainability.quantum_explainability
import quantum.predict

def render_explainability():
    section_header('Explainability', 'Why did the model make this prediction?')
    
    tab1, tab2 = st.tabs(['Classical Explainability', 'Quantum Explainability'])
    
    with tab1:
        try:
            model = classical.train.load_model("Random Forest")
            data = preprocessing.pipeline.load_processed_data()
            X_train = data["X_train"]
            X_test = data["X_test"]
            feature_names = [f"PC{i+1}" for i in range(X_train.shape[1])]
            
            @st.cache_data
            def get_shap_values(_model, _X_train, _X_test):
                return explainability.shap_analysis.compute_shap_values(_model, _X_train, _X_test, model_name="Random Forest")
                
            shap_values, base_value = get_shap_values(model, X_train, X_test)
            
            fig_summary = explainability.shap_analysis.plot_shap_summary(shap_values, X_test, feature_names=feature_names)
            st.plotly_chart(fig_summary, use_container_width=True)
            
            sample_idx = 0
            explanation = explainability.shap_analysis.explain_single_prediction(
                model=model,
                sample=X_test[sample_idx],
                X_background=X_train,
                model_name="Random Forest",
                feature_names=feature_names
            )
            fig_single = explainability.shap_analysis.plot_single_explanation(explanation)
            st.plotly_chart(fig_single, use_container_width=True)
            
        except Exception as e:
            error_state(str(e))
            
    with tab2:
        try:
            if not quantum.predict.is_quantum_model_trained():
                empty_state('Quantum model not trained. Run the training pipeline first.')
            else:
                q_model = quantum.predict.load_quantum_model()
                data = preprocessing.pipeline.load_processed_data()
                X_test_quantum = data["X_test_quantum"]
                
                # Pick test sample [0] quantum features
                sample = X_test_quantum[0]
                
                sensitivities, ranking = explainability.quantum_explainability.quantum_feature_sensitivity(
                    q_model, sample
                )
                
                st.plotly_chart(explainability.quantum_explainability.plot_quantum_sensitivity(sensitivities), use_container_width=True)
                st.plotly_chart(explainability.quantum_explainability.plot_perturbation_details(sensitivities), use_container_width=True)
                
                st.dataframe(ranking)
                
                explanation_panel(
                    "Methodology", 
                    "This method uses perturbation analysis to determine feature sensitivity in the quantum circuit, NOT SHAP."
                )
        except Exception as e:
            error_state(str(e))
