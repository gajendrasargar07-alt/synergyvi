"""
Q-Dx Dashboard
==============
Hybrid Quantum Intelligence for Early Disease Detection

Main Streamlit application entry point.
Run with: streamlit run dashboard/app.py
"""

import sys
import os

# Ensure project root is on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import config

# ── Page Configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Q-Dx | Hybrid Quantum Intelligence",
    page_icon="◇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Theme CSS ──────────────────────────────────────────────────────────
from dashboard.components.theme import CUSTOM_CSS

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Ensure Directories ────────────────────────────────────────────────────────
config.ensure_dirs()

# ── Navigation ─────────────────────────────────────────────────────────────────
PAGES = {
    "Overview": "overview",
    "Disease Prediction": "prediction",
    "Model Benchmark": "benchmark",
    "Explainability": "explainability",
    "Quantum Lab": "quantum_lab",
    "Quantum Hardware": "quantum_hardware",
    "About": "about",
}

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 1rem 0 1.5rem 0;">
            <h1 style="margin:0;font-size:1.6rem;font-weight:800;letter-spacing:-0.03em;">
                ◇ {config.APP_NAME}
            </h1>
            <div style="color:#9898b0;font-size:0.78rem;margin-top:0.25rem;line-height:1.4;">
                {config.APP_SUBTITLE}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected = st.radio(
        "Navigation",
        list(PAGES.keys()),
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        '<div style="color:#68688f;font-size:0.7rem;padding:0.5rem 0;">'
        "SIH26139 · Research Prototype<br>"
        "Not for clinical use"
        "</div>",
        unsafe_allow_html=True,
    )


# ── Page Routing ───────────────────────────────────────────────────────────────
def render_page(page_key: str):
    """Route to the appropriate page renderer."""
    try:
        if page_key == "overview":
            from dashboard.pages.overview import render_overview
            render_overview()
        elif page_key == "prediction":
            from dashboard.pages.prediction import render_prediction
            render_prediction()
        elif page_key == "benchmark":
            from dashboard.pages.benchmark import render_benchmark
            render_benchmark()
        elif page_key == "explainability":
            from dashboard.pages.explainability import render_explainability
            render_explainability()
        elif page_key == "quantum_lab":
            from dashboard.pages.quantum_lab import render_quantum_lab
            render_quantum_lab()
        elif page_key == "quantum_hardware":
            from dashboard.pages.quantum_hardware import render_quantum_hardware
            render_quantum_hardware()
        elif page_key == "about":
            from dashboard.pages.about import render_about
            render_about()
        else:
            st.error(f"Unknown page: {page_key}")
    except Exception as e:
        st.error(f"Error loading page: {e}")
        st.exception(e)


render_page(PAGES[selected])
