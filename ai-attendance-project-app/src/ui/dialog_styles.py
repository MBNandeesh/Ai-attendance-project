import streamlit as st


def apply_dialog_styles():
    """Shared visual polish for all Streamlit dialogs."""
    st.markdown(
        """
        <style>
        div[role="dialog"],
        [data-testid="stDialog"] {
            border-radius: 22px !important;
            border: 1px solid rgba(47,120,208,.18) !important;
            background: rgba(255,255,255,.98) !important;
            box-shadow: 0 28px 70px rgba(20,42,70,.20) !important;
        }

        div[role="dialog"] h1,
        div[role="dialog"] h2,
        div[role="dialog"] h3,
        div[role="dialog"] h4,
        [data-testid="stDialog"] h1,
        [data-testid="stDialog"] h2,
        [data-testid="stDialog"] h3,
        [data-testid="stDialog"] h4 {
            color: #142A46 !important;
            font-weight: 850 !important;
        }

        div[role="dialog"] p,
        div[role="dialog"] label,
        [data-testid="stDialog"] p,
        [data-testid="stDialog"] label {
            color: #25344B !important;
            font-size: 16px !important;
        }

        div[role="dialog"] .stButton > button,
        [data-testid="stDialog"] .stButton > button {
            min-height: 52px !important;
            border-radius: 14px !important;
            font-size: 16px !important;
            font-weight: 850 !important;
        }

        div[role="dialog"] .stButton > button[kind="primary"],
        div[role="dialog"] .stButton > button[kind="primary"] *,
        [data-testid="stDialog"] .stButton > button[kind="primary"],
        [data-testid="stDialog"] .stButton > button[kind="primary"] * {
            color: #FFFFFF !important;
        }

        div[role="dialog"] .stButton > button[kind="primary"],
        [data-testid="stDialog"] .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2368B7, #2F78D0 56%, #5B4BC4) !important;
            border-color: transparent !important;
            box-shadow: 0 11px 25px rgba(47,120,208,.24) !important;
        }

        div[role="dialog"] .stTextInput input,
        div[role="dialog"] .stSelectbox input,
        [data-testid="stDialog"] .stTextInput input,
        [data-testid="stDialog"] .stSelectbox input {
            min-height: 48px !important;
            font-size: 16px !important;
            border-radius: 12px !important;
        }

        div[role="dialog"] [data-testid="stDataFrame"],
        [data-testid="stDialog"] [data-testid="stDataFrame"] {
            border-radius: 14px !important;
        }

        div[role="dialog"] .stAlert,
        [data-testid="stDialog"] .stAlert {
            border-radius: 13px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
