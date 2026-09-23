import streamlit as st


NAVY = "#1E3A5F"
NAVY_DARK = "#17314F"
SECONDARY = "#3E6B9C"
BACKGROUND = "#F7F9FC"
SURFACE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#667085"
BORDER = "#E4E9F0"
SUCCESS = "#3F7D62"
WARNING = "#B7791F"
ERROR = "#B84A4A"
ACCENT = "#6C63CE"


def style_background_home():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background:
                    radial-gradient(circle at 88% 10%, rgba(62,107,156,0.15), transparent 28%),
                    radial-gradient(circle at 8% 84%, rgba(108,99,206,0.09), transparent 25%),
                    linear-gradient(135deg, #F7F9FC 0%, #F3F7FC 48%, #EDF4FC 100%) !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background:
                    radial-gradient(circle at 92% 4%, rgba(62,107,156,0.10), transparent 24%),
                    radial-gradient(circle at 5% 92%, rgba(108,99,206,0.05), transparent 24%),
                    {BACKGROUND} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0&display=swap');

            :root {{
                --brand: {NAVY};
                --brand-dark: {NAVY_DARK};
                --secondary: {SECONDARY};
                --surface: {SURFACE};
                --background: {BACKGROUND};
                --text: {TEXT};
                --muted: {MUTED};
                --border: {BORDER};
                --success: {SUCCESS};
                --warning: {WARNING};
                --error: {ERROR};
                --accent: {ACCENT};
            }}

            #MainMenu,
            footer,
            header {{
                visibility: hidden;
            }}

            .stApp {{
                font-family: 'Inter', sans-serif !important;
                color: var(--text) !important;
            }}

            .block-container {{
                max-width: 1180px !important;
                padding: 1.35rem 1.75rem 4rem !important;
            }}

            h1, h2, h3, h4 {{
                color: var(--text) !important;
                letter-spacing: -0.025em !important;
            }}

            h1 {{
                font-size: clamp(2.2rem, 4.2vw, 3.65rem) !important;
                line-height: 1.05 !important;
                font-weight: 700 !important;
            }}

            h2 {{
                font-size: clamp(1.65rem, 2.4vw, 2.05rem) !important;
                line-height: 1.14 !important;
                font-weight: 700 !important;
            }}

            h3 {{
                font-size: 1.12rem !important;
                line-height: 1.35 !important;
                font-weight: 650 !important;
            }}

            p, label, [data-testid="stMarkdownContainer"] {{
                color: var(--text);
            }}

            /* Streamlit Material Symbols must keep their own font.
               The visible strings such as arrow_forward were caused by the
               icon ligature being styled as ordinary Inter text. */
            [data-testid="stIconMaterial"],
            [data-testid="stIconMaterial"] *,
            span[class*="material-symbols"],
            span[class*="Material-Symbols"] {{
                font-family: 'Material Symbols Rounded' !important;
                font-weight: 400 !important;
                font-style: normal !important;
                font-size: 1.18rem !important;
                line-height: 1 !important;
                letter-spacing: normal !important;
                text-transform: none !important;
                white-space: nowrap !important;
                translate: none !important;
                font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
            }}

            .stButton [data-testid="stIconMaterial"] {{
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 1.25rem !important;
                height: 1.25rem !important;
                margin-right: 0.45rem !important;
                vertical-align: -0.18rem !important;
            }}

            .app-topbar {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                padding: 0.85rem 1rem;
                margin: 0 0 1.5rem;
                border: 1px solid rgba(255,255,255,0.72);
                border-radius: 18px;
                background: rgba(255,255,255,0.80);
                box-shadow: 0 10px 34px rgba(23,32,51,0.06);
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
            }}

            .brand-lockup {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                min-width: 0;
            }}

            .brand-mark {{
                width: 42px;
                height: 42px;
                flex: 0 0 auto;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 13px;
                color: #FFFFFF;
                background: linear-gradient(145deg, #1E3A5F, #315D8A);
                box-shadow: 0 8px 20px rgba(30,58,95,0.24);
                font-weight: 800;
                font-size: 0.9rem;
            }}

            .brand-name {{
                color: var(--text);
                font-size: 1rem;
                font-weight: 700;
                line-height: 1.15;
            }}

            .brand-tagline {{
                color: var(--muted);
                font-size: 0.72rem;
                margin-top: 3px;
            }}

            .topbar-status {{
                flex: 0 0 auto;
                padding: 0.55rem 0.8rem;
                border: 1px solid var(--border);
                border-radius: 999px;
                background: rgba(255,255,255,0.8);
                color: var(--brand);
                font-size: 0.72rem;
                font-weight: 600;
            }}

            .topbar-status-soft {{
                color: var(--muted);
                font-weight: 500;
            }}

            .stButton > button,
            .stDownloadButton > button {{
                min-height: 44px !important;
                border-radius: 12px !important;
                border: 1px solid var(--border) !important;
                background: rgba(255,255,255,0.96) !important;
                color: var(--brand) !important;
                font-weight: 600 !important;
                box-shadow: 0 7px 20px rgba(23,32,51,0.06) !important;
                transition: transform 160ms ease, box-shadow 160ms ease, background 160ms ease, border-color 160ms ease !important;
            }}

            .stButton > button:hover,
            .stDownloadButton > button:hover {{
                background: #FFFFFF !important;
                border-color: #CBD5E1 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 12px 26px rgba(23,32,51,0.10) !important;
            }}

            .stButton > button[kind="primary"] {{
                background: linear-gradient(135deg, #1E3A5F 0%, #2E5C8C 100%) !important;
                border-color: transparent !important;
                color: #FFFFFF !important;
                box-shadow: 0 10px 22px rgba(30,58,95,0.25) !important;
            }}

            .stButton > button[kind="primary"]:hover {{
                background: linear-gradient(135deg, #17314F 0%, #234A73 100%) !important;
                box-shadow: 0 14px 30px rgba(30,58,95,0.30) !important;
            }}

            .stButton > button[kind="secondary"] {{
                background: rgba(255,255,255,0.94) !important;
                border-color: var(--border) !important;
                color: var(--brand) !important;
            }}

            .stButton > button[kind="tertiary"] {{
                background: transparent !important;
                border-color: transparent !important;
                box-shadow: none !important;
                color: var(--muted) !important;
            }}

            .stButton > button[kind="tertiary"]:hover {{
                background: rgba(30,58,95,0.06) !important;
                color: var(--brand) !important;
                box-shadow: none !important;
            }}

            [data-testid="stVerticalBlockBorderWrapper"] {{
                border-color: var(--border) !important;
                border-radius: 18px !important;
                background: rgba(255,255,255,0.92) !important;
                box-shadow: 0 12px 30px rgba(23,32,51,0.055) !important;
                transition: transform 180ms ease, box-shadow 180ms ease !important;
            }}

            [data-testid="stVerticalBlockBorderWrapper"]:hover {{
                transform: translateY(-3px) !important;
                box-shadow: 0 16px 34px rgba(23,32,51,0.08) !important;
            }}

            .stTextInput > div > div,
            .stTextArea > div > div,
            .stSelectbox > div > div,
            .stDateInput > div > div,
            .stTimeInput > div > div {{
                border-radius: 12px !important;
                border-color: var(--border) !important;
                background: var(--surface) !important;
                box-shadow: 0 4px 14px rgba(23,32,51,0.03) !important;
            }}

            .stTextInput input,
            .stTextArea textarea {{
                color: var(--text) !important;
            }}

            .stAlert {{
                border-radius: 14px !important;
                border: 1px solid var(--border) !important;
                box-shadow: 0 6px 18px rgba(23,32,51,0.04) !important;
            }}

            [data-testid="stMetric"] {{
                background: rgba(255,255,255,0.88) !important;
                border: 1px solid var(--border) !important;
                border-radius: 16px !important;
                padding: 1rem !important;
                box-shadow: 0 8px 24px rgba(23,32,51,0.05) !important;
            }}

            [data-testid="stDataFrame"] {{
                border: 1px solid var(--border) !important;
                border-radius: 16px !important;
                overflow: hidden !important;
                background: var(--surface) !important;
                box-shadow: 0 8px 24px rgba(23,32,51,0.05) !important;
            }}

            .stDivider {{
                border-color: var(--border) !important;
            }}

            .ui-eyebrow {{
                color: var(--secondary);
                font-size: 0.74rem;
                font-weight: 700;
                letter-spacing: 0.13em;
                text-transform: uppercase;
                margin-bottom: 0.55rem;
            }}

            .ui-muted {{
                color: var(--muted) !important;
            }}

            .ui-hero {{
                position: relative;
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.78);
                background: linear-gradient(135deg, #FFFFFF 0%, #F7FAFF 62%, #EAF3FF 100%);
                padding: clamp(1.5rem, 4vw, 3rem);
                box-shadow: 0 22px 52px rgba(30,58,95,0.10);
            }}

            .ui-hero::before {{
                content: "";
                position: absolute;
                width: 430px;
                height: 430px;
                right: -120px;
                top: -160px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(62,107,156,0.20), rgba(62,107,156,0.02) 62%, transparent 72%);
                animation: float-orb 8s ease-in-out infinite;
                pointer-events: none;
            }}

            .ui-hero::after {{
                content: "";
                position: absolute;
                left: 52%;
                top: -22%;
                width: 2px;
                height: 150%;
                background: linear-gradient(to bottom, transparent, rgba(62,107,156,0.08), transparent);
                transform: rotate(18deg);
                animation: scan-line 7s linear infinite;
                pointer-events: none;
            }}

            .ui-hero-copy {{
                position: relative;
                z-index: 2;
                max-width: 720px;
            }}

            .ui-hero-title {{
                margin: 0 !important;
                color: var(--brand) !important;
            }}

            .ui-hero-gradient-text {{
                background: linear-gradient(90deg, #1E3A5F, #2F6EB0);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
            }}

            .ui-hero-copy-text {{
                margin: 0.8rem 0 0;
                max-width: 690px;
                color: var(--muted);
                font-size: 0.98rem;
                line-height: 1.7;
            }}

            .ui-feature-strip {{
                display: flex;
                gap: 1rem;
                flex-wrap: wrap;
                margin-top: 1.3rem;
            }}

            .ui-feature {{
                flex: 1 1 190px;
                min-width: 0;
                border: 1px solid var(--border);
                border-radius: 16px;
                background: rgba(255,255,255,0.90);
                padding: 1rem 1.1rem;
                box-shadow: 0 8px 22px rgba(23,32,51,0.04);
                transition: transform 160ms ease, box-shadow 160ms ease;
            }}

            .ui-feature:hover {{
                transform: translateY(-3px);
                box-shadow: 0 12px 26px rgba(23,32,51,0.08);
            }}

            .ui-feature-title {{
                font-weight: 700;
                color: var(--text);
                font-size: 0.9rem;
            }}

            .ui-feature-copy {{
                color: var(--muted);
                font-size: 0.78rem;
                line-height: 1.5;
                margin-top: 4px;
            }}

            .ui-card-kicker {{
                color: var(--secondary);
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.12em;
            }}

            .ui-card-title {{
                color: var(--text);
                font-size: 1.08rem;
                font-weight: 700;
                margin-top: 0.35rem;
            }}

            .ui-card-copy {{
                color: var(--muted);
                font-size: 0.82rem;
                line-height: 1.55;
                min-height: 3.1rem;
                margin-top: 0.45rem;
            }}

            .ui-quote {{
                margin-top: 1.4rem;
                padding: 1rem 1.2rem;
                border-left: 3px solid #4F79A5;
                border-radius: 0 14px 14px 0;
                background: rgba(255,255,255,0.68);
                color: #52657C;
                font-size: 0.84rem;
                font-style: italic;
            }}

            .app-footer {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                margin-top: 3rem;
                padding: 1.25rem 1rem 0.2rem;
                border-top: 1px solid var(--border);
            }}

            .footer-brand {{
                color: var(--brand);
                font-weight: 700;
                font-size: 0.8rem;
            }}

            .footer-copy {{
                color: #98A2B3;
                font-size: 0.7rem;
                margin-top: 3px;
            }}

            .footer-credit {{
                color: #7B8797;
                font-size: 0.72rem;
            }}

            .sidebar-brand {{
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 0.5rem 0.35rem 1.1rem;
            }}

            .sidebar-brand-mark {{
                width: 42px;
                height: 42px;
                border-radius: 12px;
                background: linear-gradient(135deg, #FFFFFF, #DCEBFA);
                color: var(--brand);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                box-shadow: 0 6px 18px rgba(0,0,0,0.14);
            }}

            .sidebar-brand-name {{
                color: #FFFFFF;
                font-size: 0.95rem;
                font-weight: 700;
            }}

            .sidebar-brand-subtitle {{
                color: rgba(255,255,255,0.64);
                font-size: 0.7rem;
                margin-top: 2px;
            }}

            .sidebar-section-label {{
                color: rgba(255,255,255,0.45);
                text-transform: uppercase;
                letter-spacing: 0.11em;
                font-size: 0.67rem;
                font-weight: 700;
                margin: 0.9rem 0 0.5rem;
            }}

            .sidebar-spacer {{
                height: 18rem;
            }}

            .sidebar-user-card {{
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 0.85rem;
                border-radius: 14px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.10);
                margin-bottom: 0.7rem;
            }}

            .sidebar-user-avatar {{
                width: 36px;
                height: 36px;
                border-radius: 11px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(255,255,255,0.16);
                color: #FFFFFF;
                font-weight: 700;
            }}

            .sidebar-user-name {{
                color: #FFFFFF;
                font-weight: 600;
                font-size: 0.8rem;
            }}

            .sidebar-user-role {{
                color: rgba(255,255,255,0.60);
                font-size: 0.68rem;
                margin-top: 2px;
            }}

            section[data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #0F2E52 0%, #163F6B 56%, #143458 100%) !important;
                border-right: 1px solid rgba(255,255,255,0.08) !important;
            }}

            @keyframes float-orb {{
                0%, 100% {{ transform: translate3d(0, 0, 0) scale(1); }}
                50% {{ transform: translate3d(-12px, 10px, 0) scale(1.04); }}
            }}

            @keyframes scan-line {{
                0% {{ opacity: 0; transform: translateX(-90px) rotate(18deg); }}
                20% {{ opacity: 1; }}
                80% {{ opacity: 1; }}
                100% {{ opacity: 0; transform: translateX(180px) rotate(18deg); }}
            }}

            @media (max-width: 780px) {{
                .block-container {{
                    padding: 1rem 0.85rem 3rem !important;
                }}

                .app-topbar {{
                    align-items: flex-start;
                    flex-direction: column;
                    padding: 0.8rem;
                }}

                .topbar-status {{
                    width: 100%;
                    text-align: center;
                }}

                .app-footer {{
                    flex-direction: column;
                    align-items: flex-start;
                }}

                .ui-hero {{
                    border-radius: 20px;
                    padding: 1.4rem;
                }}
            }}

            @media (prefers-reduced-motion: reduce) {{
                *,
                *::before,
                *::after {{
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                    scroll-behavior: auto !important;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
