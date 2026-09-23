import streamlit as st


CONTRAST = "#F59E0B"


def style_emphasis_elements():
    st.markdown(
        f"""
        <style>
            /* Stronger typography for every interactive button. */
            .stButton > button,
            .stDownloadButton > button {{
                font-size: 1rem !important;
                font-weight: 750 !important;
                letter-spacing: 0.005em !important;
                text-shadow: 0 1px 0 rgba(255,255,255,0.28);
            }}

            .stButton > button[kind="primary"] {{
                min-height: 48px !important;
                letter-spacing: 0.01em !important;
                box-shadow:
                    0 10px 24px rgba(30,58,95,0.23),
                    0 5px 18px rgba(245,158,11,0.12) !important;
                position: relative !important;
                overflow: hidden !important;
            }}

            .stButton > button[kind="primary"]::after {{
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                width: 5px;
                height: 100%;
                background: linear-gradient(180deg, #FCD34D, {CONTRAST}, #D97706);
                opacity: 0.95;
                pointer-events: none;
            }}

            .stButton > button[kind="primary"]:hover {{
                box-shadow:
                    0 15px 32px rgba(30,58,95,0.28),
                    0 7px 24px rgba(245,158,11,0.20) !important;
            }}

            .stButton > button[kind="secondary"] {{
                font-size: 0.96rem !important;
                font-weight: 720 !important;
                border-left: 4px solid {CONTRAST} !important;
            }}

            .stButton > button[kind="tertiary"] {{
                font-size: 0.95rem !important;
                font-weight: 650 !important;
            }}

            .stButton > button:focus-visible,
            .stDownloadButton > button:focus-visible {{
                outline: 3px solid rgba(245,158,11,0.38) !important;
                outline-offset: 2px !important;
            }}

            /* Make Streamlit notifications noticeably easier to read. */
            .stAlert {{
                border-radius: 16px !important;
                border-left: 5px solid {CONTRAST} !important;
                padding: 0.85rem 1rem !important;
                box-shadow:
                    0 10px 24px rgba(23,32,51,0.07),
                    0 3px 12px rgba(245,158,11,0.08) !important;
            }}

            .stAlert [data-testid="stMarkdownContainer"],
            .stAlert p,
            .stAlert li {{
                font-size: 0.98rem !important;
                font-weight: 650 !important;
                line-height: 1.55 !important;
                color: var(--text) !important;
            }}

            .stAlert strong,
            .stAlert b {{
                font-weight: 800 !important;
                color: var(--brand-dark) !important;
            }}

            .stAlert svg {{
                width: 1.4rem !important;
                height: 1.4rem !important;
            }}

            /* High-contrast text inside dark surfaces. */
            section[data-testid="stSidebar"] .stButton > button,
            section[data-testid="stSidebar"] .stMarkdown,
            section[data-testid="stSidebar"] label {{
                font-weight: 650 !important;
            }}

            .ui-eyebrow,
            .ui-card-kicker {{
                font-weight: 800 !important;
            }}

            .ui-hero-gradient-text {{
                background: linear-gradient(90deg, #1E5AA8 0%, #6C63CE 58%, {CONTRAST} 100%) !important;
                -webkit-background-clip: text !important;
                background-clip: text !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
