import streamlit as st


def style_locked_visual_system():
    """Final product visual system: locked palette, readable type, and rich motion."""
    st.markdown(
        """
        <style>
            :root {
                --brand-blue: #6290C3;
                --brand-mint: #C2E7DA;
                --brand-cream: #F1FFE7;
                --brand-navy: #1A1B41;
                --brand-lime: #BAFF29;
                --brand-white: #FFFFFF;
            }

            /* ===== LOCKED PRODUCT PALETTE ===== */
            .stApp,
            [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at 10% 10%, rgba(194,231,218,.55), transparent 28%),
                    radial-gradient(circle at 90% 16%, rgba(98,144,195,.22), transparent 30%),
                    linear-gradient(145deg, var(--brand-cream) 0%, #F8FFF3 42%, #EAF4FB 100%) !important;
            }

            /* Keep the core identity exact; no decorative red/purple/teal theme colors. */
            .app-topbar,
            section[data-testid="stSidebar"] {
                background:
                    radial-gradient(circle at 85% 10%, rgba(98,144,195,.28), transparent 24%),
                    linear-gradient(145deg, var(--brand-navy) 0%, #24335F 55%, var(--brand-blue) 130%) !important;
            }

            .app-topbar,
            .app-topbar * {
                color: var(--brand-white) !important;
            }

            .app-topbar .brand-tagline,
            .app-topbar .topbar-status-soft {
                color: rgba(255,255,255,.82) !important;
            }

            /* ===== TYPOGRAPHY ===== */
            body,
            .stApp,
            .stMarkdown,
            [data-testid="stMarkdownContainer"],
            label,
            .stCaption,
            .stTextInput,
            .stTextArea,
            .stSelectbox,
            .stDateInput,
            .stTimeInput,
            .stMultiSelect,
            .stNumberInput,
            .stRadio,
            .stCheckbox {
                font-size: 17px !important;
            }

            h1 { font-size: clamp(2rem, 3vw, 3.15rem) !important; font-weight: 850 !important; letter-spacing: -0.025em !important; }
            h2 { font-size: clamp(1.55rem, 2.2vw, 2.15rem) !important; font-weight: 850 !important; }
            h3 { font-size: clamp(1.25rem, 1.7vw, 1.65rem) !important; font-weight: 800 !important; }
            h4 { font-size: 1.15rem !important; font-weight: 800 !important; }

            .ui-eyebrow,
            .ui-card-kicker,
            .sidebar-section-label {
                color: var(--brand-blue) !important;
                font-size: .9rem !important;
                font-weight: 850 !important;
                letter-spacing: .13em !important;
            }

            .ui-muted,
            .stCaption {
                font-size: 16px !important;
                line-height: 1.65 !important;
            }

            /* ===== BUTTONS ===== */
            .stButton > button,
            .stDownloadButton > button {
                min-height: 54px !important;
                padding: .65rem 1.2rem !important;
                font-size: 17px !important;
                font-weight: 850 !important;
                letter-spacing: .01em !important;
                border-radius: 14px !important;
                transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease, filter .22s ease !important;
            }

            .stButton > button[kind="primary"] {
                color: var(--brand-white) !important;
                background: linear-gradient(110deg, var(--brand-navy), var(--brand-blue), var(--brand-navy)) !important;
                background-size: 220% 100% !important;
                border: 1px solid rgba(255,255,255,.14) !important;
                box-shadow: 0 12px 28px rgba(26,27,65,.22), 0 0 0 1px rgba(186,255,41,.10) !important;
                animation: button-breathe 3.4s ease-in-out infinite;
            }

            .stButton > button[kind="primary"]:hover {
                color: var(--brand-white) !important;
                background-position: 100% 50% !important;
                filter: brightness(1.08) !important;
                transform: translateY(-4px) scale(1.015) !important;
                box-shadow: 0 18px 38px rgba(26,27,65,.28), 0 0 0 4px rgba(186,255,41,.13) !important;
            }

            .stButton > button[kind="secondary"] {
                color: var(--brand-navy) !important;
                border: 2px solid rgba(98,144,195,.55) !important;
                background: rgba(255,255,255,.72) !important;
            }

            .stButton > button[kind="secondary"]:hover {
                border-color: var(--brand-lime) !important;
                transform: translateY(-3px) !important;
                box-shadow: 0 12px 26px rgba(98,144,195,.18) !important;
            }

            .stButton > button[kind="tertiary"] {
                font-size: 16px !important;
                font-weight: 800 !important;
            }

            /* ===== SIDEBAR ===== */
            section[data-testid="stSidebar"] * {
                color: var(--brand-white) !important;
            }

            section[data-testid="stSidebar"] .sidebar-brand-subtitle,
            section[data-testid="stSidebar"] .sidebar-user-role {
                color: rgba(255,255,255,.78) !important;
            }

            section[data-testid="stSidebar"] .stButton > button {
                min-height: 52px !important;
                font-size: 16px !important;
                font-weight: 850 !important;
                border-radius: 13px !important;
                transition: all .22s ease !important;
            }

            section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
                background: linear-gradient(105deg, var(--brand-blue), #78A9D8) !important;
                color: var(--brand-white) !important;
                box-shadow: 0 10px 24px rgba(98,144,195,.32) !important;
                animation: sidebar-glow 4s ease-in-out infinite;
            }

            section[data-testid="stSidebar"] .stButton > button[kind="tertiary"]:hover {
                background: rgba(194,231,218,.16) !important;
                color: var(--brand-white) !important;
                transform: translateX(6px) !important;
            }

            section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
                background: linear-gradient(105deg, var(--brand-blue), #8BBBE7) !important;
                transform: translateX(5px) translateY(-2px) !important;
                box-shadow: 0 14px 30px rgba(98,144,195,.42), 0 0 0 3px rgba(186,255,41,.10) !important;
            }

            /* ===== CARDS / PANELS ===== */
            [data-testid="stVerticalBlockBorderWrapper"],
            [data-testid="stExpander"],
            [data-testid="stMetric"] {
                background: rgba(255,255,255,.78) !important;
                border-color: rgba(98,144,195,.24) !important;
                box-shadow: 0 12px 32px rgba(26,27,65,.08) !important;
                transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease !important;
            }

            [data-testid="stVerticalBlockBorderWrapper"]:hover,
            [data-testid="stExpander"]:hover,
            [data-testid="stMetric"]:hover {
                transform: translateY(-5px) !important;
                border-color: rgba(186,255,41,.62) !important;
                box-shadow: 0 20px 42px rgba(98,144,195,.16) !important;
            }

            /* ===== INPUTS ===== */
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox input,
            .stNumberInput input,
            .stDateInput input,
            .stTimeInput input,
            [data-baseweb="select"] * {
                font-size: 17px !important;
                font-weight: 650 !important;
            }

            .stTextInput > label,
            .stTextArea > label,
            .stSelectbox > label,
            .stNumberInput > label,
            .stDateInput > label,
            .stTimeInput > label,
            .stMultiSelect > label,
            .stRadio > label,
            .stCheckbox > label {
                color: var(--brand-navy) !important;
                font-size: 16px !important;
                font-weight: 800 !important;
            }

            .stTextInput > div > div:focus-within,
            .stTextArea > div > div:focus-within,
            .stSelectbox > div > div:focus-within,
            .stNumberInput > div > div:focus-within,
            .stDateInput > div > div:focus-within,
            .stTimeInput > div > div:focus-within {
                border-color: var(--brand-blue) !important;
                box-shadow: 0 0 0 4px rgba(98,144,195,.16), 0 8px 24px rgba(194,231,218,.28) !important;
                transform: translateY(-1px);
            }

            /* ===== ALERTS: red only when Streamlit explicitly uses error state ===== */
            .stAlert {
                font-size: 16px !important;
                font-weight: 750 !important;
                border-radius: 15px !important;
                animation: alert-pop .42s ease-out both;
            }

            .stAlert [data-testid="stMarkdownContainer"],
            .stAlert p {
                font-size: 16px !important;
                font-weight: 750 !important;
            }

            /* Success/info/warning use brand colors; errors retain Streamlit red for warnings/errors only. */
            [data-testid="stNotification"] {
                font-size: 16px !important;
                font-weight: 750 !important;
            }

            /* ===== METRICS / TABLES ===== */
            [data-testid="stMetricLabel"] { font-size: 15px !important; font-weight: 800 !important; }
            [data-testid="stMetricValue"] { font-size: 2.05rem !important; font-weight: 900 !important; color: var(--brand-navy) !important; }
            [data-testid="stDataFrame"] { border-radius: 16px !important; animation: rise-in .65s ease-out both; }
            [data-testid="stDataFrame"] * { font-size: 15px !important; }

            button[data-baseweb="tab"] { font-size: 16px !important; font-weight: 800 !important; }
            button[data-baseweb="tab"][aria-selected="true"] { color: var(--brand-navy) !important; border-bottom-color: var(--brand-lime) !important; }
            [data-testid="stExpander"] summary { font-size: 16px !important; font-weight: 800 !important; }

            /* ===== PRODUCT MOTION ===== */
            .block-container { animation: page-enter .72s cubic-bezier(.2,.75,.2,1) both; }
            .ui-hero,
            .ui-feature,
            .ui-stat,
            .ui-panel,
            .ui-card { animation: rise-in .72s cubic-bezier(.2,.75,.2,1) both; }

            .ui-feature:hover,
            .ui-stat:hover,
            .ui-panel:hover,
            .ui-card:hover { transform: translateY(-5px) !important; }

            /* Subtle ambient movement for backgrounds and branded decorative elements. */
            .app-topbar::before,
            section[data-testid="stSidebar"]::before {
                content: "";
                position: absolute;
                inset: -30%;
                background: radial-gradient(circle, rgba(194,231,218,.12) 0 8%, transparent 9% 100%);
                background-size: 120px 120px;
                animation: ambient-drift 18s linear infinite;
                pointer-events: none;
            }

            /* Lime is the signature interactive highlight, not a replacement for the core blue. */
            a:hover,
            .stLinkButton > a:hover { color: var(--brand-blue) !important; text-shadow: 0 0 16px rgba(186,255,41,.32); }

            @keyframes page-enter {
                from { opacity: 0; transform: translateY(18px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes rise-in {
                from { opacity: 0; transform: translateY(16px) scale(.985); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }
            @keyframes alert-pop {
                from { opacity: 0; transform: translateX(-14px) scale(.98); }
                to { opacity: 1; transform: translateX(0) scale(1); }
            }
            @keyframes button-breathe {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }
            @keyframes sidebar-glow {
                0%, 100% { box-shadow: 0 10px 24px rgba(98,144,195,.28); }
                50% { box-shadow: 0 14px 30px rgba(194,231,218,.18); }
            }
            @keyframes ambient-drift {
                from { transform: translate3d(-4%, -2%, 0) rotate(0deg); }
                to { transform: translate3d(4%, 2%, 0) rotate(360deg); }
            }

            @media (prefers-reduced-motion: reduce) {
                *, *::before, *::after {
                    animation-duration: .01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: .01ms !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
