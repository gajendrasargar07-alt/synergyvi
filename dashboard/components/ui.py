"""
Reusable UI Components
======================
Streamlit-compatible reusable components for the Q-Dx dashboard.
"""

import streamlit as st
from dashboard.components.theme import (
    ACCENT, ACCENT_LIGHT, SUCCESS, DANGER, WARNING,
    TEXT_PRIMARY, TEXT_SECONDARY, QUANTUM_PURPLE,
    BG_CARD, BORDER,
)


def metric_card(label: str, value, accent: bool = False, suffix: str = ""):
    """Render a compact metric card.

    Args:
        label: Metric label (uppercase).
        value: Metric value to display.
        accent: Use accent color for value.
        suffix: Optional suffix (e.g., '%', 's').
    """
    color_class = "qdx-metric-accent" if accent else ""
    display_val = f"{value}{suffix}" if value is not None else "—"
    st.markdown(
        f"""
        <div class="qdx-metric">
            <div class="qdx-metric-label">{label}</div>
            <div class="qdx-metric-value {color_class}">{display_val}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def model_card(name: str, model_type: str, metrics: dict = None):
    """Render a model summary card.

    Args:
        name: Model name.
        model_type: 'classical' or 'quantum'.
        metrics: Optional metrics dictionary.
    """
    badge = status_badge("Classical", "info") if model_type == "classical" else status_badge("Quantum", "quantum")

    metrics_html = ""
    if metrics:
        acc = metrics.get("accuracy")
        f1 = metrics.get("f1")
        if acc is not None:
            metrics_html += f'<span style="color:{TEXT_SECONDARY};font-size:0.85rem;">Accuracy: <strong style="color:{TEXT_PRIMARY}">{acc:.3f}</strong></span><br>'
        if f1 is not None:
            metrics_html += f'<span style="color:{TEXT_SECONDARY};font-size:0.85rem;">F1: <strong style="color:{TEXT_PRIMARY}">{f1:.3f}</strong></span>'
    else:
        metrics_html = f'<span style="color:{TEXT_SECONDARY};font-size:0.85rem;">Awaiting experiment</span>'

    st.markdown(
        f"""
        <div class="qdx-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                <strong style="font-size:1.05rem;">{name}</strong>
                {badge}
            </div>
            {metrics_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def prediction_card(label: str, prediction: str, probability: float = None, backend: str = None):
    """Render a prediction result card.

    Args:
        label: Model or section label.
        prediction: 'Benign' or 'Malignant'.
        probability: Optional confidence probability.
        backend: Optional backend name.
    """
    css_class = "qdx-prediction-benign" if prediction == "Benign" else "qdx-prediction-malignant"
    color = SUCCESS if prediction == "Benign" else DANGER

    prob_html = ""
    if probability is not None:
        prob_html = f'<div style="color:{TEXT_SECONDARY};font-size:0.85rem;margin-top:0.25rem;">Confidence: {probability:.1%}</div>'

    backend_html = ""
    if backend:
        backend_html = f'<div style="color:{TEXT_SECONDARY};font-size:0.75rem;margin-top:0.5rem;">Backend: {backend}</div>'

    st.markdown(
        f"""
        <div class="{css_class}">
            <div style="color:{TEXT_SECONDARY};font-size:0.8rem;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;">{label}</div>
            <div style="color:{color};font-size:1.5rem;font-weight:700;margin:0.25rem 0;">{prediction}</div>
            {prob_html}
            {backend_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):
    """Render a section header with optional subtitle.

    Args:
        title: Section title.
        subtitle: Optional description.
    """
    sub_html = f'<div class="qdx-section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="qdx-section-header">
            <h2>{title}</h2>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text: str, variant: str = "info") -> str:
    """Return HTML for a status badge.

    Args:
        text: Badge text.
        variant: One of 'success', 'danger', 'warning', 'info', 'quantum'.

    Returns:
        HTML string.
    """
    return f'<span class="qdx-badge qdx-badge-{variant}">{text}</span>'


def quantum_circuit_panel(circuit_text: str):
    """Render a quantum circuit diagram in a styled panel.

    Args:
        circuit_text: Text representation of the quantum circuit.
    """
    st.markdown(
        f"""
        <div class="qdx-circuit">
            <pre style="margin:0;white-space:pre;overflow-x:auto;">{circuit_text}</pre>
        </div>
        """,
        unsafe_allow_html=True,
    )


def explanation_panel(title: str, content: str):
    """Render an explanation panel.

    Args:
        title: Panel title.
        content: Explanation text or HTML.
    """
    st.markdown(
        f"""
        <div class="qdx-card">
            <div style="font-weight:600;margin-bottom:0.5rem;color:{ACCENT_LIGHT};">{title}</div>
            <div style="color:{TEXT_SECONDARY};line-height:1.6;">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card(title: str):
    """Render a chart wrapper card header. Use before st.plotly_chart().

    Args:
        title: Chart title.
    """
    st.markdown(
        f"""
        <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px 12px 0 0;
                     padding:1rem 1.5rem 0.5rem;margin-top:1rem;">
            <span style="font-weight:600;font-size:0.95rem;">{title}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(message: str, icon: str = "◇"):
    """Render an empty state placeholder.

    Args:
        message: Message to display.
        icon: Optional icon character.
    """
    st.markdown(
        f"""
        <div class="qdx-empty">
            <div class="qdx-empty-icon">{icon}</div>
            <div style="font-size:1.1rem;font-weight:500;margin-bottom:0.5rem;">No data available</div>
            <div>{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def loading_state(message: str = "Processing..."):
    """Render a loading state.

    Args:
        message: Loading message.
    """
    st.markdown(
        f"""
        <div class="qdx-empty">
            <div style="font-size:1.1rem;color:{ACCENT_LIGHT};">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def error_state(message: str):
    """Render an error state.

    Args:
        message: Error message.
    """
    st.markdown(
        f"""
        <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);
                     border-radius:12px;padding:1.5rem;text-align:center;">
            <div style="color:{DANGER};font-weight:600;margin-bottom:0.5rem;">Error</div>
            <div style="color:{TEXT_SECONDARY};">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def disclaimer():
    """Render the research prototype disclaimer."""
    st.markdown(
        '<div class="qdx-disclaimer">⚠ Research prototype. This prediction is not a medical diagnosis. '
        "Q-Dx is an experimental platform and must not be used for clinical decision-making.</div>",
        unsafe_allow_html=True,
    )
