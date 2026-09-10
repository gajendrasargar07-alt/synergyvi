"""
Dashboard Theme
===============
Premium dark theme configuration for the Q-Dx Streamlit dashboard.
Inspired by modern dark AI/SaaS product aesthetics.
"""

# ── Color Palette ──────────────────────────────────────────────────────────────
BG_PRIMARY = "#050505"       # Cinematic near-black background
BG_SECONDARY = "#0b0b0b"     # Dark charcoal surfaces
BG_CARD = "#111111"          # Card background
BG_CARD_HOVER = "#191919"    # Card hover state
BORDER = "#2a2a2a"           # Subtle borders
BORDER_ACCENT = "#5b171a"    # Active borders

TEXT_PRIMARY = "#f5f5f1"     # Warm white primary text
TEXT_SECONDARY = "#a4a4a0"   # Muted gray secondary text
TEXT_MUTED = "#676764"       # Very muted text

ACCENT = "#e50914"           # Cinematic red accent
ACCENT_LIGHT = "#ff4d56"     # Lighter red accent
ACCENT_GLOW = "rgba(229, 9, 20, 0.18)"  # Subtle glow

SUCCESS = "#22c55e"          # Green - benign/good
DANGER = "#ef4444"           # Red - malignant/bad
WARNING = "#f59e0b"          # Amber - caution
INFO = "#e9e9e4"             # Neutral - informational

QUANTUM_PURPLE = "#8b5cf6"   # Quantum-specific accent
QUANTUM_GLOW = "rgba(139, 92, 246, 0.15)"

# ── Typography ─────────────────────────────────────────────────────────────────
FONT_FAMILY = "'DM Sans', 'Segoe UI', sans-serif"

# ── Main CSS ───────────────────────────────────────────────────────────────────
CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

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

    /* ── Cinematic editorial overrides ─────────────────────────── */
    .stApp {{
        background:
            radial-gradient(ellipse 70% 42% at 78% -10%, rgba(229, 9, 20, .16), transparent 68%),
            linear-gradient(180deg, #090909 0%, {BG_PRIMARY} 42rem);
    }}
    .block-container {{ max-width: 1440px; padding: 2.2rem 3.4rem 4rem; }}
    section[data-testid="stSidebar"] {{ background: #080808; border-right-color: #252525; }}
    section[data-testid="stSidebar"] .stRadio label {{
        border-radius: 3px; font-size: .78rem; font-weight: 600; letter-spacing: .055em;
        padding: .35rem .45rem; text-transform: uppercase;
    }}
    section[data-testid="stSidebar"] .stRadio label:hover {{ background: #181818; color: {TEXT_PRIMARY}; }}
    .qdx-eyebrow {{
        color: {ACCENT_LIGHT}; font-family: 'DM Mono', monospace; font-size: .68rem;
        font-weight: 500; letter-spacing: .13em; text-transform: uppercase;
    }}
    .qdx-hero {{
        background: linear-gradient(115deg, rgba(20,20,20,.96), rgba(10,10,10,.72));
        border-color: #292929; border-radius: 4px; min-height: 330px; padding: 3.8rem 3.5rem;
    }}
    .qdx-hero::after {{
        content: ''; position: absolute; width: 44rem; height: 44rem; right: -21rem; top: -22rem;
        background: radial-gradient(circle, rgba(229,9,20,.28), rgba(229,9,20,.04) 34%, transparent 70%);
        pointer-events: none;
    }}
    .qdx-hero h1 {{
        font-size: clamp(2.5rem, 5vw, 4.75rem) !important; line-height: .98;
        max-width: 780px; margin: .7rem 0 1rem !important;
    }}
    .qdx-hero h1 span {{ color: {ACCENT}; }}
    .qdx-hero p {{ color: #c7c7c2; font-size: 1.04rem; line-height: 1.65; max-width: 580px; }}
    .qdx-hero-rule {{ background: {ACCENT}; height: 2px; margin: 1.5rem 0; width: 46px; }}
    .qdx-section-header {{ border-bottom-color: #303030; margin: .6rem 0 1.4rem; padding-bottom: .9rem; }}
    .qdx-section-header h2 {{ font-size: 1.85rem !important; }}
    .qdx-card {{
        background: linear-gradient(145deg, rgba(23,23,23,.96), rgba(14,14,14,.96));
        border-radius: 3px; transition: transform .2s ease, border-color .2s ease, background .2s ease;
    }}
    .qdx-card:hover {{ background: {BG_CARD_HOVER}; border-color: #5a282b; transform: translateY(-2px); }}
    .qdx-metric {{ border-radius: 0; border-top: 2px solid #353535; padding: 1.1rem .8rem; text-align: left; }}
    .qdx-metric:hover {{ border-top-color: {ACCENT}; }}
    .qdx-metric-label {{ font-family: 'DM Mono', monospace; font-size: .62rem; letter-spacing: .1em; }}
    .qdx-badge {{ border-radius: 1px; font-family: 'DM Mono', monospace; font-size: .64rem; letter-spacing: .07em; text-transform: uppercase; }}
    .qdx-badge-info {{ background: rgba(245,245,241,.08); border-color: #4a4a48; color: {INFO}; }}
    .qdx-prediction-benign, .qdx-prediction-malignant {{ border-radius: 3px; }}
    .qdx-prediction-benign {{ border-left: 3px solid {SUCCESS}; }}
    .qdx-prediction-malignant {{ border-left: 3px solid {DANGER}; }}
    .qdx-circuit {{ background: #090909; border-color: #303030; border-left: 3px solid {ACCENT}; border-radius: 2px; color: #f1f1ed; }}
    .qdx-disclaimer {{ background: rgba(229,9,20,.08); border-color: rgba(229,9,20,.3); border-radius: 2px; color: #ffb4b8; }}
    .stButton > button {{
        background: {ACCENT}; border-color: {ACCENT}; border-radius: 2px; font-size: .78rem;
        font-weight: 700; letter-spacing: .055em; text-transform: uppercase;
    }}
    .stButton > button:hover {{ background: #ff1722; border-color: #ff1722; box-shadow: none; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 1.2rem; border-bottom: 1px solid #303030; }}
    .stTabs [data-baseweb="tab"] {{ font-size: .78rem; font-weight: 600; letter-spacing: .05em; padding: .55rem 0; text-transform: uppercase; }}
    .stTabs [data-baseweb="tab-highlight"] {{ background-color: {ACCENT}; }}
    @media (max-width: 760px) {{
        .block-container {{ padding: 1.2rem 1rem 3rem; }}
        .qdx-hero {{ min-height: auto; padding: 2.3rem 1.5rem; }}
    }}

    /* ── Hide Streamlit defaults ────────────────────────────────── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
"""
