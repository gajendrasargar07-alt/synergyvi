import sys
import os
import pandas as pd
import plotly.graph_objects as go

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
import config
from dashboard.components.ui import *
from dashboard.components.theme import *

def render_benchmark() -> None:
    """Render the model benchmark page."""
    section_header('Model Benchmark', 'Unified comparison of classical and quantum model performance.')
    
    try:
        from integration.pipeline import load_benchmark_results
        benchmark = load_benchmark_results()
        # Benchmark files contain metadata plus the actual model dictionary.
        # Accept the legacy flat format too, so older artifacts remain usable.
        results = benchmark.get("models", benchmark) if benchmark else {}
        
        if not results:
            empty_state('Run the training pipeline to populate benchmark results.')
            return

        if benchmark.get("generated_at"):
            st.caption(f"Last generated: {benchmark['generated_at']}")
            
        # Extract data for dataframe
        df_data = []
        for model_name, metrics in results.items():
            df_data.append({
                "Model": model_name,
                "Type": metrics.get("type", "classical"),
                "Accuracy": metrics.get("accuracy", 0.0),
                "Precision": metrics.get("precision", 0.0),
                "Recall": metrics.get("recall", 0.0),
                "F1": metrics.get("f1", 0.0),
                "ROC-AUC": metrics.get("roc_auc", 0.0),
                "Training Time (s)": metrics.get("training_time", 0.0)
            })
            
        df = pd.DataFrame(df_data).set_index("Model")
        
        st.markdown("### Metrics Table")
        st.dataframe(df.drop(columns=["Type"]).style.format("{:.4f}"))
        
        # Plotly charts
        def create_bar_chart(metric_name, col_name, title, is_log=False):
            fig = go.Figure()
            colors = [QUANTUM_PURPLE if t == "quantum" else ACCENT for t in df["Type"]]
            
            fig.add_trace(go.Bar(
                x=df.index,
                y=df[col_name],
                marker_color=colors,
                text=df[col_name].round(4),
                textposition='auto',
            ))
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=30, b=20),
                yaxis_type="log" if is_log else None
            )
            
            chart_card(title)
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            create_bar_chart("accuracy", "Accuracy", "Accuracy Comparison")
        with col2:
            create_bar_chart("f1", "F1", "F1 Score Comparison")
            
        col3, col4 = st.columns(2)
        with col3:
            create_bar_chart("roc_auc", "ROC-AUC", "ROC-AUC Comparison")
        with col4:
            create_bar_chart("training_time", "Training Time (s)", "Training Time Comparison (Log Scale)", is_log=True)

    except ImportError:
        error_state("Failed to import load_benchmark_results from integration.pipeline. Ensure the module exists.")
    except Exception as e:
        error_state(f"An error occurred loading benchmark results: {str(e)}")
