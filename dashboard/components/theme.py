"""
Dashboard Theme
===============
Premium dark theme configuration for the Q-Dx Streamlit dashboard.
Inspired by modern dark AI/SaaS product aesthetics.
"""

# ── Color Palette ──────────────────────────────────────────────────────────────
BG_PRIMARY = "#0a0a0f"       # Almost-black background
BG_SECONDARY = "#12121a"     # Dark charcoal surfaces
BG_CARD = "#1a1a28"          # Card background
BG_CARD_HOVER = "#22223a"    # Card hover state
BORDER = "#2a2a3e"           # Subtle borders
BORDER_ACCENT = "#3a3a5e"    # Active borders

TEXT_PRIMARY = "#e8e8f0"     # Off-white primary text
TEXT_SECONDARY = "#9898b0"   # Muted gray secondary text
TEXT_MUTED = "#6868880"      # Very muted text

ACCENT = "#6366f1"           # Primary indigo/violet accent
ACCENT_LIGHT = "#818cf8"     # Lighter accent
ACCENT_GLOW = "rgba(99, 102, 241, 0.15)"  # Subtle glow

SUCCESS = "#22c55e"          # Green - benign/good
DANGER = "#ef4444"           # Red - malignant/bad
WARNING = "#f59e0b"          # Amber - caution
INFO = "#3b82f6"             # Blue - informational

QUANTUM_PURPLE = "#8b5cf6"   # Quantum-specific accent
QUANTUM_GLOW = "rgba(139, 92, 246, 0.15)"

# ── Typography ─────────────────────────────────────────────────────────────────
FONT_FAMILY = "'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

# ── Main CSS ───────────────────────────────────────────────────────────────────
CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ─────────────────────────────────────────────────── */
    .stApp {{
        background-color: {BG_PRIMARY};
        color: {TEXT_PRIMARY};
        font-family: {FONT_FAMILY};
    }}

    /* ── Sidebar ────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {{
        background-color: {BG_SECONDARY};
        border-right: 1px solid {BORDER};
    }}
    section[data-testid="stSidebar"] .stMarkdown h1 {{
        color: {ACCENT};
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    section[data-testid="stSidebar"] .stRadio label {{
        color: {TEXT_SECONDARY};
        transition: color 0.2s ease;
    }}
    section[data-testid="stSidebar"] .stRadio label:hover {{
        color: {TEXT_PRIMARY};
    }}

    /* ── Headers ────────────────────────────────────────────────── */
    h1, h2, h3, h4 {{
        color: {TEXT_PRIMARY} !important;
        font-family: {FONT_FAMILY};
        letter-spacing: -0.02em;
    }}
    h1 {{ font-weight: 700 !important; }}
    h2 {{ font-weight: 600 !important; color: {TEXT_PRIMARY} !important; }}
    h3 {{ font-weight: 500 !important; }}

    /* ── Cards ──────────────────────────────────────────────────── */
    .qdx-card {{
        background: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}
    .qdx-card:hover {{
        border-color: {BORDER_ACCENT};
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }}

    /* ── Metric Cards ──────────────────────────────────────────── */
    .qdx-metric {{
        background: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        text-align: center;
    }}
    .qdx-metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin: 0.25rem 0;
    }}
    .qdx-metric-label {{
        font-size: 0.8rem;
        font-weight: 500;
        color: {TEXT_SECONDARY};
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    .qdx-metric-accent {{
        color: {ACCENT};
    }}

    /* ── Status Badges ─────────────────────────────────────────── */
    .qdx-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }}
    .qdx-badge-success {{
        background: rgba(34, 197, 94, 0.12);
        color: {SUCCESS};
        border: 1px solid rgba(34, 197, 94, 0.25);
    }}
    .qdx-badge-danger {{
        background: rgba(239, 68, 68, 0.12);
        color: {DANGER};
        border: 1px solid rgba(239, 68, 68, 0.25);
    }}
    .qdx-badge-warning {{
        background: rgba(245, 158, 11, 0.12);
        color: {WARNING};
        border: 1px solid rgba(245, 158, 11, 0.25);
    }}
    .qdx-badge-info {{
        background: rgba(99, 102, 241, 0.12);
        color: {ACCENT_LIGHT};
        border: 1px solid rgba(99, 102, 241, 0.25);
    }}
    .qdx-badge-quantum {{
        background: {QUANTUM_GLOW};
        color: {QUANTUM_PURPLE};
        border: 1px solid rgba(139, 92, 246, 0.25);
    }}

    /* ── Hero Section ──────────────────────────────────────────── */
    .qdx-hero {{
        background: linear-gradient(135deg, {BG_SECONDARY} 0%, {BG_CARD} 100%);
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }}
    .qdx-hero::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, {ACCENT_GLOW} 0%, transparent 70%);
        pointer-events: none;
    }}
    .qdx-hero h1 {{
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        line-height: 1.2;
        margin-bottom: 0.75rem;
        background: linear-gradient(135deg, {TEXT_PRIMARY} 0%, {ACCENT_LIGHT} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .qdx-hero p {{
        color: {TEXT_SECONDARY};
        font-size: 1.1rem;
        line-height: 1.6;
        max-width: 600px;
    }}

    /* ── Section Headers ───────────────────────────────────────── */
    .qdx-section-header {{
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid {BORDER};
    }}
    .qdx-section-header h2 {{
        margin: 0 !important;
        font-size: 1.5rem !important;
    }}
    .qdx-section-subtitle {{
        color: {TEXT_SECONDARY};
        font-size: 0.95rem;
        margin-top: 0.25rem;
    }}

    /* ── Prediction Result ─────────────────────────────────────── */
    .qdx-prediction-benign {{
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 12px;
        padding: 1.5rem;
    }}
    .qdx-prediction-malignant {{
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: 12px;
        padding: 1.5rem;
    }}

    /* ── Buttons ────────────────────────────────────────────────── */
    .stButton > button {{
        background: linear-gradient(135deg, {ACCENT} 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-family: {FONT_FAMILY};
        transition: all 0.3s ease;
        letter-spacing: 0.01em;
    }}
    .stButton > button:hover {{
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
        transform: translateY(-1px);
    }}

    /* ── Data Tables ───────────────────────────────────────────── */
    .stDataFrame {{
        border: 1px solid {BORDER} !important;
        border-radius: 8px;
    }}

    /* ── Tabs ───────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {TEXT_SECONDARY};
        font-family: {FONT_FAMILY};
        font-weight: 500;
        border-radius: 8px;
    }}
    .stTabs [aria-selected="true"] {{
        color: {TEXT_PRIMARY};
        background-color: {BG_CARD};
    }}

    /* ── Expander ───────────────────────────────────────────────── */
    .streamlit-expanderHeader {{
        background-color: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 8px;
        color: {TEXT_PRIMARY};
    }}

    /* ── Inputs ─────────────────────────────────────────────────── */
    .stNumberInput input, .stTextInput input, .stSelectbox select {{
        background-color: {BG_CARD} !important;
        color: {TEXT_PRIMARY} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
    }}

    /* ── Disclaimer ─────────────────────────────────────────────── */
    .qdx-disclaimer {{
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.8rem;
        color: {WARNING};
        margin-top: 1rem;
    }}

    /* ── Circuit Panel ─────────────────────────────────────────── */
    .qdx-circuit {{
        background: {BG_SECONDARY};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Fira Code', 'Cascadia Code', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
        color: {ACCENT_LIGHT};
    }}

    /* ── Empty State ───────────────────────────────────────────── */
    .qdx-empty {{
        text-align: center;
        padding: 3rem 1.5rem;
        color: {TEXT_SECONDARY};
    }}
    .qdx-empty-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }}

    /* ── Scrollbar ──────────────────────────────────────────────── */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: {BG_PRIMARY};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {BORDER};
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {BORDER_ACCENT};
    }}

    /* ── Hide Streamlit defaults ────────────────────────────────── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
"""
