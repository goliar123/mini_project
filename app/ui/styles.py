import streamlit as st


def get_theme(dark_mode: bool) -> dict:
    if dark_mode:
        return {
            "c_bg": "#0E1117",
            "c_bg_grad": "radial-gradient(circle at 10% 20%, #1a2230 0%, #0E1117 58%)",
            "c_sidebar": "#171d28",
            "c_text_main": "#F9FBFF",
            "c_text_light": "#D5DEED",
            "c_primary_btn": "#4ADE80",
            "c_primary_btn_hover": "#68EFA0",
            "c_on_primary": "#0B1A10",
            "c_secondary": "#1F2937",
            "c_secondary_hover": "#2B384A",
            "c_input_bg": "#1A2230",
            "c_input_text": "#FFFFFF",
            "c_input_border": "#4B607F",
            "c_card_border": "rgba(140, 165, 201, 0.4)",
            "c_shadow_sm": "0 8px 24px rgba(0,0,0,0.30)",
        }

    return {
        "c_bg": "#FAFAF8",
        "c_bg_grad": "#FAFAF8",
        "c_sidebar": "#F4F3ED",
        "c_text_main": "#151412",
        "c_text_light": "#615E5B",
        "c_primary_btn": "#201F1D",
        "c_primary_btn_hover": "#353230",
        "c_on_primary": "#FFFFFF",
        "c_secondary": "#EAE8E2",
        "c_secondary_hover": "#DFDCD4",
        "c_input_bg": "#FFFFFF",
        "c_input_text": "#1A1A1A",
        "c_input_border": "rgba(0, 0, 0, 0.12)",
        "c_card_border": "rgba(0, 0, 0, 0.08)",
        "c_shadow_sm": "0 6px 16px rgba(0,0,0,0.04)",
    }


def inject_global_styles(theme: dict, show_sidebar: bool) -> None:
    sidebar_visibility_css = ""
    if not show_sidebar:
        sidebar_visibility_css = """
    section[data-testid=\"stSidebar\"],
    div[data-testid=\"stSidebarNav\"],
    div[data-testid=\"stSidebarUserContent\"],
    button[data-testid=\"stSidebarNavCollapseButton\"],
    button[data-testid=\"stSidebarCollapsedControl\"] {
        display: none !important;
    }
        """

    st.markdown(
        f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&display=swap');

    :root {{
        --bg: {theme['c_bg']};
        --bg-grad: {theme['c_bg_grad']};
        --sidebar: {theme['c_sidebar']};
        --text-main: {theme['c_text_main']};
        --text-light: {theme['c_text_light']};
        --primary: {theme['c_primary_btn']};
        --primary-hover: {theme['c_primary_btn_hover']};
        --on-primary: {theme['c_on_primary']};
        --secondary: {theme['c_secondary']};
        --secondary-hover: {theme['c_secondary_hover']};
        --input-bg: {theme['c_input_bg']};
        --input-text: {theme['c_input_text']};
        --input-border: {theme['c_input_border']};
        --card-border: {theme['c_card_border']};
        --shadow-sm: {theme['c_shadow_sm']};
        --anim-fast: 160ms;
        --anim-med: 260ms;
        --anim-slow: 380ms;
    }}

    html, body {{
        font-family: 'Lexend', sans-serif;
        color: var(--text-main);
    }}

    header {{ background: transparent !important; }}
    .stDeployButton {{ display: none; }}
    footer {{ visibility: hidden; }}
    [data-testid="stDecoration"] {{ display: none; }}
    [data-testid="stSidebarCollapseButton"] {{ display:none !important; }}

    .stApp {{
        background: var(--bg-grad);
        color: var(--text-main);
    }}

    .block-container {{
        max-width: 96% !important;
        padding-top: 0.9rem !important;
        padding-bottom: 1.3rem !important;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--sidebar) 0%, var(--bg) 100%) !important;
        border-right: 1px solid var(--card-border);
        min-width: 280px !important;
        max-width: 320px !important;
    }}

    {sidebar_visibility_css}

    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {{
        color: var(--text-main) !important;
    }}

    .meta-sub,
    .log-sub,
    .command-sub,
    .preview-meta,
    .page-footer-line,
    .panel-history-sub,
    .resolve-panel-meta,
    .resolve-panel-note,
    .claude-hero-subtitle,
    .cg-desc {{
        color: var(--text-light) !important;
    }}

    .glass-card,
    .bento-card,
    .command-shell,
    .resolve-panel-shell,
    .preview-shell,
    .cg-card,
    .contact-card,
    .page-footer,
    .page-footer-card {{
        border: 1px solid var(--card-border);
        background: color-mix(in srgb, var(--input-bg) 94%, transparent);
        box-shadow: var(--shadow-sm);
    }}

    .glass-card,
    .bento-card {{
        border-radius: 16px;
        padding: 14px;
        animation: fade-slide-up var(--anim-med) ease;
    }}

    .sidebar-shell-card {{
        transition: transform var(--anim-fast) ease, box-shadow var(--anim-fast) ease;
    }}

    .sidebar-shell-card:hover {{
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(0,0,0,0.10);
    }}

    .meta-label,
    .dash-kicker,
    .command-kicker,
    .resolve-panel-kicker,
    .panel-history-kicker,
    .page-footer-kicker,
    .contact-kicker,
    .small-label {{
        font-size: 0.72rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 720;
        color: var(--text-light);
    }}

    .meta-value {{
        font-size: 1.2rem;
        font-weight: 800;
        color: var(--text-main);
    }}

    .log-title,
    .panel-history-title,
    .resolve-panel-title,
    .contact-label,
    .page-footer-title {{
        color: var(--text-main);
        font-weight: 700;
    }}

    .dash-shell {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        border-radius: 18px;
        padding: 12px 14px;
        animation: fade-slide-up var(--anim-med) ease;
    }}

    .dash-title {{
        font-size: clamp(1.95rem, 3vw, 2.7rem);
        line-height: 1.08;
        max-width: 23ch;
        margin: 0;
    }}

    .headline-title {{
        font-family: 'Fraunces', Georgia, serif;
        letter-spacing: -0.02em;
        color: var(--text-main);
    }}

    .headline-metrics {{
        display: flex;
        align-items: baseline;
        gap: 10px;
    }}

    .active-count {{
        font-size: clamp(2.1rem, 5.6vw, 3.1rem);
        font-weight: 800;
        line-height: 1;
    }}

    .active-label {{
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        font-weight: 700;
        color: var(--text-light);
    }}

    .command-shell {{
        border-radius: 14px;
        padding: 11px 12px;
        margin: 8px 0 12px 0;
        animation: fade-slide-in var(--anim-fast) ease;
    }}

    .command-actions-card {{
        border: 1px solid var(--card-border);
        border-radius: 12px;
        background: color-mix(in srgb, var(--input-bg) 92%, var(--bg));
        box-shadow: var(--shadow-sm);
        padding: 8px;
    }}

    .command-actions-title {{
        font-size: 0.72rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 760;
        color: var(--text-light);
        margin-bottom: 6px;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        background: color-mix(in srgb, var(--input-bg) 92%, var(--bg)) !important;
        box-shadow: var(--shadow-sm) !important;
        padding: 8px !important;
    }}

    .command-actions-note {{
        margin-top: 10px;
        font-size: 0.74rem;
        color: var(--text-light);
        text-align: center;
    }}

    .mode-transition-note {{
        margin: 8px 0;
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--text-light);
    }}

    .resolve-panel-shell {{
        border-radius: 14px;
        padding: 12px;
        animation: panel-slide-in var(--anim-med) ease;
        position: sticky;
        top: 8px;
        z-index: 25;
    }}

    .panel-align-offset {{
        height: 86px;
    }}

    .resolve-panel-head {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 8px;
        margin-bottom: 8px;
    }}

    .panel-history-item {{
        border: 1px solid var(--card-border);
        border-radius: 10px;
        padding: 8px 9px;
        background: color-mix(in srgb, var(--input-bg) 98%, transparent);
        margin-bottom: 6px;
    }}

    .small-value {{
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 4px;
        color: var(--text-main);
    }}

    .stTextInput > div,
    .stPasswordInput > div,
    div[data-testid="stTextInputRootElement"],
    div[data-testid="stTextInputRootElement"] > div {{
        background: transparent !important;
    }}

    div[data-baseweb="base-input"] {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }}

    div[data-baseweb="base-input"]:focus-within {{
        border-color: color-mix(in srgb, var(--primary) 72%, var(--input-border)) !important;
        box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary) 22%, transparent) !important;
    }}

    div[data-baseweb="base-input"] input {{
        color: var(--input-text) !important;
        caret-color: var(--input-text) !important;
        font-weight: 600 !important;
        background: transparent !important;
    }}

    .stPasswordInput button,
    div[data-baseweb="base-input"] button {{
        background: transparent !important;
        border: none !important;
        color: var(--text-light) !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: var(--text-light) !important;
        opacity: 0.9;
    }}

    div[data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 12px !important;
        color: var(--text-main) !important;
        transition: border-color var(--anim-fast) ease, box-shadow var(--anim-fast) ease;
    }}

    div[data-baseweb="select"] > div:focus-within {{
        border-color: color-mix(in srgb, var(--primary) 72%, var(--input-border)) !important;
        box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary) 22%, transparent) !important;
    }}

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] svg {{
        color: var(--text-main) !important;
        fill: var(--text-main) !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }}

    div[data-baseweb="popover"] > div {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-sm) !important;
    }}

    div[data-baseweb="popover"] li {{
        color: var(--text-main) !important;
        background: color-mix(in srgb, var(--input-bg) 98%, transparent) !important;
    }}

    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {{
        background: color-mix(in srgb, var(--secondary) 72%, var(--input-bg)) !important;
    }}

    .stRadio > label,
    .stRadio [role="radiogroup"] label,
    .stRadio [role="radiogroup"] span,
    .stRadio [data-baseweb="radio"] *,
    .stRadio [data-baseweb="radio"] label,
    .stRadio [data-baseweb="radio"] span,
    .stRadio [data-baseweb="radio"] div {{
        color: var(--text-main) !important;
        opacity: 1 !important;
        font-weight: 680 !important;
    }}

    .stRadio [role="radiogroup"] {{
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 6px 8px;
        background: color-mix(in srgb, var(--input-bg) 95%, transparent);
    }}

    .stRadio [role="radiogroup"] > label {{
        border-radius: 9px;
        transition: background var(--anim-fast) ease, transform var(--anim-fast) ease;
        padding: 2px 4px;
    }}

    .stRadio [role="radiogroup"] > label:hover {{
        transform: translateY(-1px);
    }}

    /* Heatmap hover/selected gradient: light red -> light yellow */
    .stRadio [role="radiogroup"] > label:nth-child(1):hover,
    .stRadio [role="radiogroup"] > label:nth-child(1):has(input:checked) {{
        background: linear-gradient(90deg, #ffe2d8 0%, #fff4bf 100%);
    }}

    /* Scatter hover/selected gradient */
    .stRadio [role="radiogroup"] > label:nth-child(2):hover,
    .stRadio [role="radiogroup"] > label:nth-child(2):has(input:checked) {{
        background: linear-gradient(90deg, #dce9ff 0%, #d8f3f8 100%);
    }}

    [data-testid="stSidebar"] .stRadio > div,
    [data-testid="stSidebar"] .stMultiSelect > div {{
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 8px;
        background: color-mix(in srgb, var(--input-bg) 92%, transparent);
    }}

    [data-testid="stSidebar"] [data-baseweb="tag"] {{
        background: color-mix(in srgb, var(--secondary) 88%, transparent) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="tag"] span,
    [data-testid="stSidebar"] [data-baseweb="tag"] div,
    [data-testid="stSidebar"] [data-baseweb="tag"] svg {{
        color: var(--text-main) !important;
        fill: var(--text-main) !important;
    }}

    .stButton > button {{
        border-radius: 12px !important;
        font-weight: 650;
        border: 1px solid transparent;
        padding: 0.64rem 1rem;
        transition: transform var(--anim-fast) ease, filter var(--anim-fast) ease, box-shadow var(--anim-fast) ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
    }}

    .stButton > button:focus-visible {{
        outline: 2px solid color-mix(in srgb, var(--primary) 62%, var(--text-main)) !important;
        outline-offset: 2px;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px !important;
        border: 1px solid #d8cd9a !important;
        background: #f5efc5 !important;
    }}

    [data-testid="stAlert"],
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div,
    [data-testid="stAlert"] strong {{
        color: #2f2a17 !important;
        opacity: 1 !important;
        font-weight: 650 !important;
    }}

    [data-testid="stAlert"] a {{
        color: #184a9c !important;
        text-decoration: underline !important;
    }}

    button[kind="primary"] {{
        background: var(--primary) !important;
        color: var(--on-primary) !important;
        border: none !important;
    }}

    button[kind="primary"] span,
    button[kind="primary"] p,
    button[kind="primary"] div {{
        color: var(--on-primary) !important;
    }}

    button[kind="secondary"] {{
        background: var(--secondary) !important;
        color: var(--text-main) !important;
        border-color: var(--card-border);
    }}

    button[kind="secondary"] span,
    button[kind="secondary"] p {{
        color: var(--text-main) !important;
    }}

    button[kind="secondary"][id*="dashboard_logout_btn"]:hover,
    .command-actions-title + div[data-testid="stVerticalBlockBorderWrapper"] .stButton:nth-of-type(2) > button:hover {{
        background: #ef4444 !important;
        border-color: #b91c1c !important;
        color: #ffffff !important;
    }}

    button[kind="secondary"][id*="dashboard_logout_btn"]:hover span,
    button[kind="secondary"][id*="dashboard_logout_btn"]:hover p,
    .command-actions-title + div[data-testid="stVerticalBlockBorderWrapper"] .stButton:nth-of-type(2) > button:hover span,
    .command-actions-title + div[data-testid="stVerticalBlockBorderWrapper"] .stButton:nth-of-type(2) > button:hover p {{
        color: #ffffff !important;
    }}

    div[data-testid="stDeckGlJsonChart"] {{
        border: 1px solid var(--card-border);
        border-radius: 18px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-sm);
        margin-bottom: 12px;
    }}

    div[data-testid="stDeckGlJsonChart"]:hover {{
        transform: translateY(-1px);
    }}

    .map-legend-shell {{
        border-radius: 12px;
        padding: 9px 12px;
        margin: 8px 0 10px 0;
        animation: fade-slide-in var(--anim-fast) ease;
        position: sticky;
        top: 6px;
        z-index: 20;
        backdrop-filter: blur(6px);
    }}

    .map-legend-topline {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }}

    .map-legend-stats {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }}

    .map-stat-pill {{
        border-radius: 999px;
        border: 1px solid var(--card-border);
        background: color-mix(in srgb, var(--input-bg) 96%, transparent);
        padding: 3px 10px;
        font-size: 0.72rem;
        color: var(--text-light);
        font-weight: 640;
    }}

    .map-stat-pill b {{
        color: var(--text-main);
        font-weight: 760;
    }}

    .map-chip-row {{
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        align-items: center;
    }}

    .map-chip {{
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 650;
    }}

    .map-chip-low {{
        background: #F3E9C9;
        color: #5F4C1F;
        border: 1px solid #D6C49B;
    }}

    .map-chip-medium {{
        background: #F1DDC7;
        color: #664424;
        border: 1px solid #D9B88F;
    }}

    .map-chip-high {{
        background: #E9CFCB;
        color: #6B2F2B;
        border: 1px solid #CEA19A;
    }}

    .map-mode-label {{
        font-size: 0.78rem;
        color: var(--text-light);
        font-weight: 700;
    }}

    .claude-hero-container {{
        margin-top: 0;
        padding: 6px 0 12px 0;
    }}

    .landing-topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0 0 8px 0;
        padding: 8px 10px;
        border: 1px solid var(--card-border);
        border-radius: 12px;
        background: color-mix(in srgb, var(--input-bg) 95%, transparent);
        box-shadow: var(--shadow-sm);
    }}

    .landing-topbar-brand {{
        font-size: 0.78rem;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        font-weight: 760;
        color: var(--text-light);
    }}

    .landing-login-link {{
        display: inline-block;
        border: 1px solid var(--card-border);
        border-radius: 999px;
        padding: 7px 14px;
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--text-main);
        text-decoration: none;
        background: color-mix(in srgb, var(--secondary) 88%, var(--input-bg));
        transition: transform var(--anim-fast) ease, background var(--anim-fast) ease;
    }}

    .landing-login-link:hover {{
        transform: translateY(-1px);
        background: color-mix(in srgb, var(--secondary-hover) 88%, var(--input-bg));
    }}

    .claude-hero-topline {{
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--text-light);
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .claude-hero-title {{
        font-size: clamp(2rem, 3.5vw, 3.2rem) !important;
        margin-bottom: 8px !important;
        line-height: 1.05;
    }}

    .preview-shell {{
        border-radius: 16px;
        padding: 12px;
        margin: 8px 0 12px 0;
    }}

    .preview-head {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 10px;
        margin: 0 2px 10px 2px;
    }}

    .preview-kicker {{
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        color: var(--text-main);
        font-weight: 760;
    }}

    .preview-scroll {{
        max-height: 276px;
        overflow-y: auto;
        display: grid;
        gap: 10px;
        padding-right: 4px;
    }}

    .preview-item {{
        border: 1px solid var(--card-border);
        background: color-mix(in srgb, var(--input-bg) 97%, transparent);
        border-radius: 12px;
        padding: 10px 12px;
        transition: transform var(--anim-fast) ease, box-shadow var(--anim-fast) ease;
    }}

    .preview-item:hover {{
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.06);
    }}

    .preview-item h3 {{
        margin: 7px 0 4px 0;
        font-size: 0.98rem;
        color: var(--text-main);
        font-weight: 710;
    }}

    .preview-item p {{
        margin: 0;
        font-size: 0.89rem;
        line-height: 1.46;
        color: var(--text-light);
    }}

    .preview-chip {{
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        font-size: 0.69rem;
        letter-spacing: 0.4px;
        text-transform: uppercase;
        font-weight: 760;
        padding: 3px 9px;
        border: 1px solid transparent;
    }}

    .preview-chip-progress {{
        color: #1E4C2E;
        background: #D8F0DD;
        border-color: #B8DDBF;
    }}

    .preview-chip-soon {{
        color: #5D421E;
        background: #F5E7D1;
        border-color: #E4CEAE;
    }}

    .auth-alignment-wrapper {{
        margin-top: 6px;
    }}

    .auth-panel {{
        border-radius: 20px;
        padding: 22px;
        animation: fade-slide-up var(--anim-med) ease;
    }}

    .auth-stage {{
        margin-top: 4px;
        margin-bottom: 8px;
    }}

    .auth-title {{
        font-family: 'Fraunces', Georgia, serif;
        font-size: 1.25rem;
        margin-bottom: 2px;
        color: var(--text-main);
    }}

    .auth-subtitle {{
        font-size: 0.9rem;
        color: var(--text-light);
        margin-bottom: 14px;
        line-height: 1.55;
    }}

    .claude-grid-visual {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 18px;
    }}

    .cg-card {{
        border-radius: 16px;
        padding: 22px;
        transition: transform var(--anim-med) ease, box-shadow var(--anim-med) ease;
        animation: fade-slide-up var(--anim-med) ease;
    }}

    .cg-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(0, 0, 0, 0.08);
    }}

    .cg-card-large,
    .cg-card-wide {{
        grid-column: span 2;
    }}

    .cg-icon {{
        font-size: 1.8rem;
        margin-bottom: 14px;
        color: var(--text-main);
    }}

    .cg-title {{
        font-weight: 700;
        font-size: 1.05rem;
        color: var(--text-main);
        margin-bottom: 6px;
    }}

    .contact-shell {{
        margin-top: 18px;
        margin-bottom: 14px;
        border-radius: 16px;
        border: 1px solid var(--card-border);
        padding: 14px;
        background: color-mix(in srgb, var(--input-bg) 95%, transparent);
        box-shadow: var(--shadow-sm);
    }}

    .contact-head {{
        margin-bottom: 10px;
    }}

    .contact-title {{
        margin: 0;
        font-family: 'Fraunces', Georgia, serif;
        font-size: clamp(1.1rem, 2.2vw, 1.55rem);
        color: var(--text-main);
    }}

    .contact-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
    }}

    .contact-card {{
        border-radius: 12px;
        padding: 10px 12px;
    }}

    .contact-value,
    .contact-copy {{
        font-size: 0.84rem;
        color: var(--text-light);
        margin-top: 2px;
    }}

    .page-footer {{
        margin-top: 24px;
        margin-bottom: 10px;
        border-radius: 16px;
        padding: 16px;
    }}

    .page-footer-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
    }}

    .page-footer-card {{
        border-radius: 12px;
        padding: 10px 12px;
    }}

    .page-footer-link {{
        display: block;
        font-size: 0.84rem;
        color: var(--text-main);
        text-decoration: none;
        margin-top: 4px;
    }}

    .page-footer-link:hover {{
        text-decoration: underline;
    }}

    .page-footer-bottom {{
        margin-top: 10px;
        border-top: 1px solid var(--card-border);
        padding-top: 8px;
        font-size: 0.76rem;
        color: var(--text-light);
        display: flex;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
    }}

    @keyframes fade-slide-in {{
        from {{ opacity: 0; transform: translateY(3px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes fade-slide-up {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes panel-slide-in {{
        from {{ opacity: 0; transform: translateX(20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}

    div[data-testid="stToast"] {{
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        min-width: 290px !important;
        box-shadow: var(--shadow-sm) !important;
    }}

    @media (max-width: 768px) {{
        .block-container {{
            max-width: 100% !important;
            padding-top: 0.5rem !important;
        }}

        .dash-shell {{
            flex-direction: column;
            gap: 10px;
        }}

        .dash-title {{
            max-width: none;
            font-size: clamp(1.6rem, 7vw, 2.1rem);
        }}

        .resolve-panel-shell {{
            position: static;
            margin-top: 8px;
        }}

        .preview-head {{
            flex-direction: column;
            align-items: flex-start;
            gap: 4px;
        }}

        .landing-topbar {{
            padding: 7px 8px;
        }}

        .preview-scroll {{
            max-height: 248px;
        }}

        .map-legend-topline {{
            flex-direction: column;
            align-items: flex-start;
            gap: 6px;
        }}

        .claude-grid-visual,
        .contact-grid,
        .page-footer-grid {{
            grid-template-columns: 1fr;
        }}

        .cg-card-large,
        .cg-card-wide {{
            grid-column: span 1;
        }}

        .page-footer-bottom {{
            flex-direction: column;
            align-items: flex-start;
        }}

        .panel-align-offset {{
            height: 0;
        }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            animation-duration: 1ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 1ms !important;
            scroll-behavior: auto !important;
        }}
    }}
</style>
""",
        unsafe_allow_html=True,
    )
