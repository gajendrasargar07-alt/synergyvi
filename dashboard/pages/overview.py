import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
import config
from dashboard.components.ui import *
from dashboard.components.theme import *

def render_overview() -> None:
    """Render the overview page for the Q-Dx dashboard."""
    # Hero section
    st.markdown(
        '''
        <div class="qdx-hero">
            <div class="qdx-eyebrow">Hybrid intelligence / disease research</div>
            <h1>Find signals.<br><span>Earlier.</span></h1>
            <div class="qdx-hero-rule"></div>
            <p>Q-Dx places classical machine learning and quantum experimentation in one focused research workspace for benchmarkable biomedical analysis.</p>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button(
            "Run Prediction",
            use_container_width=True,
            on_click=lambda: st.session_state.update({"navigation": "Disease Prediction"}),
        )
    with col2:
        st.button(
            "Explore Models",
            use_container_width=True,
            on_click=lambda: st.session_state.update({"navigation": "Model Benchmark"}),
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Project stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Classical Models", "4")
    with c2:
        metric_card("Quantum Model", "VQC", accent=True)
    with c3:
        metric_card("Features", "30→4")
    with c4:
        metric_card("Eval Metrics", "6")
        
    # Architecture diagram
    st.markdown("### Platform Architecture")
    diagram_html = f'''
    <div style="display: flex; justify-content: space-between; align-items: center; background: {BG_CARD}; padding: 1.5rem; border: 1px solid {BORDER}; border-radius: 12px; overflow-x: auto;">
        <div style="padding: 10px; background: {BG_SECONDARY}; border-radius: 8px; text-align: center; min-width: 100px;">Dataset</div>
        <div style="font-size: 1.5rem; color: {TEXT_SECONDARY};">→</div>
        <div style="padding: 10px; background: {BG_SECONDARY}; border-radius: 8px; text-align: center; min-width: 120px;">Preprocessing</div>
        <div style="font-size: 1.5rem; color: {TEXT_SECONDARY};">→</div>
        <div style="padding: 10px; background: rgba(99, 102, 241, 0.2); border-radius: 8px; text-align: center; min-width: 150px; border: 1px solid {ACCENT};">Classical +<br>Quantum Models</div>
        <div style="font-size: 1.5rem; color: {TEXT_SECONDARY};">→</div>
        <div style="padding: 10px; background: {BG_SECONDARY}; border-radius: 8px; text-align: center; min-width: 130px;">Benchmarking &<br>Explainability</div>
        <div style="font-size: 1.5rem; color: {TEXT_SECONDARY};">→</div>
        <div style="padding: 10px; background: rgba(34, 197, 94, 0.2); border-radius: 8px; text-align: center; min-width: 100px; border: 1px solid {SUCCESS};">Prediction</div>
    </div>
    '''
    st.markdown(diagram_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Benchmark results
    try:
        if os.path.exists(config.BENCHMARK_FILE):
            with open(config.BENCHMARK_FILE, "r") as f:
                results = json.load(f)
            # Display success or summary here if needed
            st.success("Benchmark results are available.")
        else:
            empty_state('Run the training pipeline to populate results.')
    except Exception as e:
        error_state(f"Error loading benchmark results: {str(e)}")
