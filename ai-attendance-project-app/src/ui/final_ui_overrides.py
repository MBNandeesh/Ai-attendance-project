import streamlit as st


def apply_final_ui_overrides():
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
                --text-main: #1A1B41;
                --text-muted: #52607A;
            }

            /* Global background */
            .stApp,
            [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at 8% 12%, rgba(194,231,218,.72), transparent 28%),
                    radial-gradient(circle at 92% 18%, rgba(98,144,195,.20), transparent 30%),
                    linear-gradient(135deg, #F1FFE7 0%, #F8FFF3 48%, #EAF4FB 100%) !important;
                background-size: 120% 120%, 130% 130%, 100% 100% !important;
                animation: aa-background-flow 18s ease-in-out infinite alternate !important;
                color: var(--text-main) !important;
            }

            /* Readability */
            .stApp,
            [data-testid="stMarkdownContainer"],
            [data-testid="stText"],
            .stCaption,
            .stAlert,
            .stToast,
            label,
            input,
            textarea,
            [role="combobox"] {
                font-size: 17px !important;
            }

            h1 { font-size: clamp(2.25rem, 4vw, 3.5rem) !important; font-weight: 850 !important; line-height: 1.06 !important; }
            h2 { font-size: clamp(1.8rem, 3vw, 2.5rem) !important; font-weight: 850 !important; }
            h3 { font-size: 1.45rem !important; font-weight: 820 !important; }
            h4 { font-size: 1.18rem !important; font-weight: 800 !important; }

            /* Header */
            .app-topbar {
                background: linear-gradient(135deg, #1A1B41 0%, #1A1B41 58%, #6290C3 140%) !important;
                border-color: rgba(255,255,255,.12) !important;
                box-shadow: 0 16px 38px rgba(26,27,65,.24) !important;
                animation: aa-topbar-flow 9s ease-in-out infinite alternate, aa-rise .65s ease-out both !important;
            }

            .app-topbar,
            .app-topbar * {
                color: #FFFFFF !important;
            }

            /* Remove marketing/tagline clutter */
            .app-topbar .brand-tagline,
            .app-topbar .topbar-status,
            .app-topbar .topbar-status-soft,
            .footer-brand,
            .footer-copy {
                display: none !important;
            }

            .app-topbar .brand-name {
                font-size: 1.15rem !important;
                font-weight: 850 !important;
            }

            .app-topbar .brand-mark {
                background: #FFFFFF !important;
                color: #1A1B41 !important;
                box-shadow: 0 8px 24px rgba(0,0,0,.18) !important;
                animation: aa-float 4s ease-in-out infinite !important;
            }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1A1B41 0%, #1A1B41 62%, #6290C3 145%) !important;
                animation: aa-sidebar-flow 14s ease-in-out infinite alternate !important;
            }

            section[data-testid="stSidebar"] * {
                color: #FFFFFF !important;
            }

            section[data-testid="stSidebar"] .stButton > button {
                min-height: 50px !important;
                border-radius: 14px !important;
                font-size: 16px !important;
                font-weight: 850 !important;
                transition: transform .18s ease, box-shadow .18s ease, background .18s ease !important;
            }

            section[data-testid="stSidebar"] .stButton > button[kind="tertiary"] {
                background: transparent !important;
                border-color: transparent !important;
                color: #FFFFFF !important;
            }

            section[data-testid="stSidebar"] .stButton > button[kind="tertiary"]:hover {
                background: rgba(194,231,218,.14) !important;
                transform: translateX(4px) !important;
                box-shadow: inset 3px 0 0 #BAFF29 !important;
            }

            section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
                background: #6290C3 !important;
                border-color: rgba(255,255,255,.12) !important;
                color: #FFFFFF !important;
                box-shadow: 0 12px 28px rgba(98,144,195,.30) !important;
            }

            /* Buttons */
            .stButton > button,
            .stDownloadButton > button {
                min-height: 54px !important;
                border-radius: 14px !important;
                padding: .65rem 1.2rem !important;
                font-size: 17px !important;
                font-weight: 850 !important;
                transition: transform .18s ease, box-shadow .18s ease, background .18s ease !important;
            }

            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #1A1B41 0%, #1A1B41 55%, #6290C3 100%) !important;
                color: #FFFFFF !important;
                border-color: transparent !important;
                box-shadow: 0 12px 28px rgba(26,27,65,.24) !important;
                position: relative !important;
                overflow: hidden !important;
            }

            .stButton > button[kind="primary"]::after {
                content: "";
                position: absolute;
                inset: 0 auto 0 -45%;
                width: 28%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,.24), transparent);
                transform: skewX(-18deg);
                animation: aa-button-sweep 3.4s ease-in-out infinite;
                pointer-events: none;
            }

            .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #6290C3 0%, #1A1B41 72%) !important;
                transform: translateY(-3px) scale(1.01) !important;
                box-shadow: 0 18px 36px rgba(26,27,65,.30) !important;
            }

            .stButton > button[kind="secondary"] {
                color: #1A1B41 !important;
                font-weight: 820 !important;
            }

            .stButton > button[kind="secondary"]:hover {
                border-color: #6290C3 !important;
                box-shadow: 0 0 0 3px rgba(98,144,195,.12), 0 14px 28px rgba(26,27,65,.10) !important;
                transform: translateY(-2px) !important;
            }

            /* Cards, metrics, expanders */
            [data-testid="stVerticalBlockBorderWrapper"],
            [data-testid="stExpander"],
            [data-testid="stMetric"] {
                background: rgba(255,255,255,.90) !important;
                border-color: rgba(98,144,195,.24) !important;
                box-shadow: 0 14px 34px rgba(26,27,65,.08) !important;
                animation: aa-card-in .68s cubic-bezier(.2,.8,.2,1) both !important;
                transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease !important;
            }

            [data-testid="stVerticalBlockBorderWrapper"]:hover,
            [data-testid="stExpander"]:hover,
            [data-testid="stMetric"]:hover {
                transform: translateY(-5px) !important;
                border-color: rgba(98,144,195,.42) !important;
                box-shadow: 0 22px 44px rgba(26,27,65,.13) !important;
            }

            [data-testid="stMetric"] {
                border-top: 4px solid #BAFF29 !important;
            }

            [data-testid="stMetricValue"] {
                color: #1A1B41 !important;
                font-size: 2rem !important;
                font-weight: 850 !important;
            }

            /* Inputs */
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox input,
            .stNumberInput input,
            .stDateInput input,
            .stTimeInput input {
                border-radius: 12px !important;
                border-color: rgba(98,144,195,.30) !important;
                background: rgba(255,255,255,.88) !important;
                color: #1A1B41 !important;
                font-weight: 650 !important;
            }

            .stTextInput input:focus,
            .stTextArea textarea:focus,
            .stNumberInput input:focus,
            .stDateInput input:focus,
            .stTimeInput input:focus {
                border-color: #6290C3 !important;
                box-shadow: 0 0 0 3px rgba(98,144,195,.14) !important;
            }

            /* Alerts: only warning/error states use alert colours */
            .stAlert {
                border-radius: 14px !important;
                font-weight: 760 !important;
            }

            /* Toast */
            [data-testid="stToast"] {
                background: #1A1B41 !important;
                border: 1px solid rgba(255,255,255,.14) !important;
                color: #FFFFFF !important;
                box-shadow: 0 16px 34px rgba(26,27,65,.28) !important;
                border-radius: 14px !important;
            }

            [data-testid="stToast"] * {
                color: #FFFFFF !important;
                font-size: 16px !important;
                font-weight: 800 !important;
            }

            /* Footer: name only */
            .app-footer {
                justify-content: center !important;
                background: transparent !important;
                border-top: 1px solid rgba(98,144,195,.18) !important;
                padding-top: 18px !important;
                margin-top: 28px !important;
            }

            .footer-credit {
                color: #1A1B41 !important;
                font-size: 15px !important;
                font-weight: 850 !important;
            }

            .footer-credit span {
                display: none !important;
            }

            /* General page entrance */
            .block-container {
                animation: aa-rise .72s ease-out both !important;
            }

            /* Highlight utility */
            .ui-eyebrow,
            .ui-card-kicker {
                color: #1A1B41 !important;
                font-weight: 850 !important;
            }

            .ui-eyebrow::before,
            .ui-card-kicker::before {
                background: #BAFF29 !important;
                box-shadow: 0 0 0 5px rgba(186,255,41,.18) !important;
            }

            /* Remove legacy decorative accents from older components */
            .legacy-purple,
            .legacy-cyan,
            .legacy-teal,
            .legacy-amber {
                color: #1A1B41 !important;
                background-color: transparent !important;
                border-color: rgba(98,144,195,.24) !important;
            }

            @keyframes aa-rise {
                from { opacity: 0; transform: translateY(12px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes aa-card-in {
                from { opacity: 0; transform: translateY(14px) scale(.985); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }

            @keyframes aa-background-flow {
                from { background-position: 0% 0%, 100% 0%, 0% 0%; }
                to { background-position: 16% 12%, 82% 20%, 2% 6%; }
            }

            @keyframes aa-topbar-flow {
                from { background-position: 0% 50%; }
                to { background-position: 100% 50%; }
            }

            @keyframes aa-sidebar-flow {
                from { background-position: 50% 0%; }
                to { background-position: 50% 100%; }
            }

            @keyframes aa-float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-4px); }
            }

            @keyframes aa-button-sweep {
                0%, 58% { left: -45%; }
                78%, 100% { left: 125%; }
            }

            @media (max-width: 900px) {
                .stApp,
                [data-testid="stAppViewContainer"] {
                    background:
                        radial-gradient(circle at 8% 12%, rgba(194,231,218,.58), transparent 34%),
                        linear-gradient(145deg, #F1FFE7 0%, #F8FFF3 52%, #EAF4FB 100%) !important;
                }

                .stButton > button,
                .stDownloadButton > button {
                    min-height: 52px !important;
                    font-size: 16px !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
