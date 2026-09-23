import streamlit as st


def apply_light_surface_overrides():
    """Final product-wide light surfaces, contrast, motion, and responsive polish."""
    st.markdown(
        """
        <style>
        :root {
            --aa-bg-1: #EEF6FF;
            --aa-bg-2: #F7FBFF;
            --aa-bg-3: #F1F0FF;
            --aa-navy: #142A46;
            --aa-navy-2: #1A3C63;
            --aa-blue: #2F78D0;
            --aa-indigo: #5B4BC4;
            --aa-mint: #DDF5EE;
            --aa-green: #20B477;
            --aa-amber: #F59E0B;
            --aa-red: #C94B4B;
            --aa-text: #152238;
            --aa-muted: #617089;
            --aa-border: #DCE7F3;
            --aa-white: #FFFFFF;
        }

        /* ===== Product background ===== */
        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .block-container {
            color: var(--aa-text) !important;
        }

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background:
                radial-gradient(circle at 5% 8%, rgba(80,145,220,.17), transparent 24%),
                radial-gradient(circle at 94% 13%, rgba(120,108,210,.11), transparent 22%),
                radial-gradient(circle at 74% 91%, rgba(49,190,146,.09), transparent 22%),
                linear-gradient(145deg, var(--aa-bg-1) 0%, var(--aa-bg-2) 48%, var(--aa-bg-3) 100%) !important;
            background-size: 125% 125%, 125% 125%, 125% 125%, 100% 100% !important;
            background-attachment: fixed !important;
            animation: aa-product-bg 20s ease-in-out infinite alternate !important;
        }

        [data-testid="stMainBlockContainer"],
        .block-container {
            background: transparent !important;
        }

        /* ===== Typography ===== */
        .stApp p,
        .stApp li,
        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stMarkdownContainer"] p,
        .stApp [data-testid="stText"],
        .stApp .stCaption {
            color: var(--aa-text) !important;
        }

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4 {
            color: var(--aa-navy) !important;
            font-weight: 850 !important;
            letter-spacing: -.025em !important;
        }

        .stApp h1 {
            font-size: clamp(2.35rem, 4.2vw, 3.85rem) !important;
            line-height: 1.06 !important;
        }

        .stApp h2 {
            font-size: clamp(1.9rem, 3vw, 2.65rem) !important;
            line-height: 1.12 !important;
        }

        .stApp h3 {
            font-size: 1.42rem !important;
        }

        .stApp h4 {
            font-size: 1.2rem !important;
        }

        .stApp label {
            color: var(--aa-navy) !important;
            font-size: 16px !important;
            font-weight: 800 !important;
        }

        /* ===== Top bar + sidebar ===== */
        .app-topbar,
        .app-topbar * {
            color: #FFFFFF !important;
        }

        .app-topbar {
            background: linear-gradient(135deg, #102A49 0%, #173E67 58%, #2F78D0 150%) !important;
            border-color: rgba(255,255,255,.13) !important;
            box-shadow: 0 18px 44px rgba(16,42,73,.22) !important;
        }

        .app-topbar .brand-tagline,
        .app-topbar .topbar-status,
        .app-topbar .topbar-status-soft {
            color: rgba(255,255,255,.76) !important;
        }

        .app-topbar .brand-mark {
            background: #FFFFFF !important;
            color: #102A49 !important;
        }

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 90% 6%, rgba(47,120,208,.28), transparent 24%),
                linear-gradient(180deg, #0E2745 0%, #16385D 58%, #1D4771 100%) !important;
            border-right: 1px solid rgba(255,255,255,.10) !important;
        }

        section[data-testid="stSidebar"] *,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] label {
            color: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] .sidebar-section-label,
        section[data-testid="stSidebar"] .sidebar-user-role,
        section[data-testid="stSidebar"] .sidebar-brand-subtitle {
            color: rgba(255,255,255,.70) !important;
        }

        /* ===== White/glass cards ===== */
        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stExpander"],
        [data-testid="stMetric"],
        .teacher-shell-card,
        .student-shell-card,
        .student-auth-card {
            background: rgba(255,255,255,.93) !important;
            border-color: rgba(82,126,177,.18) !important;
            box-shadow: 0 15px 38px rgba(31,65,105,.09) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover,
        [data-testid="stExpander"]:hover,
        [data-testid="stMetric"]:hover {
            border-color: rgba(47,120,208,.34) !important;
            box-shadow: 0 22px 44px rgba(31,65,105,.13) !important;
        }

        /* ===== Buttons: blue/indigo with WHITE primary text ===== */
        .stButton > button,
        .stDownloadButton > button {
            min-height: 54px !important;
            border-radius: 14px !important;
            font-size: 17px !important;
            font-weight: 850 !important;
        }

        .stButton > button[kind="primary"],
        .stButton > button[kind="primary"] *,
        .stDownloadButton > button[kind="primary"],
        .stDownloadButton > button[kind="primary"] * {
            color: #FFFFFF !important;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2368B7 0%, #2F78D0 54%, #5B4BC4 115%) !important;
            border-color: transparent !important;
            box-shadow: 0 12px 28px rgba(47,120,208,.26) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #2F78D0 0%, #5B4BC4 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 18px 34px rgba(91,75,196,.27) !important;
        }

        .stButton > button[kind="secondary"] {
            background: rgba(255,255,255,.96) !important;
            border-color: rgba(47,120,208,.22) !important;
            color: var(--aa-navy) !important;
        }

        .stButton > button[kind="secondary"] *,
        .stButton > button[kind="tertiary"] * {
            color: var(--aa-navy) !important;
        }

        .stButton > button[kind="tertiary"] {
            background: transparent !important;
            border-color: transparent !important;
            box-shadow: none !important;
            color: var(--aa-muted) !important;
        }

        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] .stButton > button * {
            color: #FFFFFF !important;
        }

        /* ===== Student workspace ===== */
        .student-welcome {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            padding: 28px 30px;
            margin: 0 0 22px;
            border-radius: 22px;
            background:
                radial-gradient(circle at 92% 8%, rgba(99,206,177,.22), transparent 25%),
                linear-gradient(135deg, #102D4E 0%, #173E67 58%, #2F78D0 145%);
            border: 1px solid rgba(255,255,255,.12);
            box-shadow: 0 24px 52px rgba(16,42,73,.20);
            animation: aa-student-hero-in .55s ease-out both;
        }

        .student-eyebrow {
            color: #DDF5EE !important;
            font-size: 12px !important;
            font-weight: 900 !important;
            letter-spacing: .14em;
            margin-bottom: 7px;
        }

        .student-welcome-title {
            color: #FFFFFF !important;
            font-size: clamp(1.75rem, 3vw, 2.55rem) !important;
            line-height: 1.08;
            font-weight: 900 !important;
        }

        .student-welcome-copy {
            color: rgba(255,255,255,.76) !important;
            margin-top: 8px;
            font-size: 16px !important;
        }

        .student-status-pill {
            flex: 0 0 auto;
            display: inline-flex;
            align-items: center;
            gap: 9px;
            padding: 10px 14px;
            border-radius: 999px;
            background: rgba(255,255,255,.10);
            border: 1px solid rgba(255,255,255,.15);
            color: #FFFFFF !important;
            font-size: 13px !important;
            font-weight: 850 !important;
            white-space: nowrap;
        }

        .student-status-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: #20B477;
            box-shadow: 0 0 0 5px rgba(32,180,119,.15);
            animation: aa-status-pulse 1.9s ease-out infinite;
        }

        .student-stat-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }

        .student-stat-card {
            min-height: 122px;
            padding: 19px 20px;
            border-radius: 18px;
            background: rgba(255,255,255,.92);
            border: 1px solid rgba(82,126,177,.16);
            box-shadow: 0 13px 30px rgba(31,65,105,.075);
            transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
            animation: aa-student-card-in .5s ease-out both;
        }

        .student-stat-card:hover {
            transform: translateY(-4px);
            border-color: rgba(47,120,208,.33);
            box-shadow: 0 20px 38px rgba(31,65,105,.12);
        }

        .student-stat-label {
            color: #6B7890 !important;
            font-size: 13px !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: .06em;
        }

        .student-stat-value {
            color: #142A46 !important;
            font-size: 32px !important;
            line-height: 1.05;
            font-weight: 900 !important;
            margin-top: 10px;
        }

        .student-stat-note {
            color: #7A879A !important;
            font-size: 12px !important;
            font-weight: 650 !important;
            margin-top: 7px;
        }

        .student-stat-card-accent {
            background: linear-gradient(145deg, #FFFFFF 0%, #F0F5FF 100%);
            border-color: rgba(91,75,196,.20);
        }

        .student-section-heading {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 18px;
            margin: 10px 0 15px;
        }

        .student-section-kicker {
            color: #2F78D0 !important;
            font-size: 12px !important;
            font-weight: 900 !important;
            letter-spacing: .13em;
        }

        .student-section-title {
            color: #142A46 !important;
            font-size: 27px !important;
            font-weight: 900 !important;
            margin-top: 3px;
        }

        .student-section-copy {
            color: #718097 !important;
            font-size: 13px !important;
            font-weight: 650 !important;
            text-align: right;
        }

        .student-empty-state {
            margin: 12px 0 28px;
            padding: 42px 22px;
            text-align: center;
            border: 1px dashed rgba(47,120,208,.30);
            border-radius: 20px;
            background: rgba(255,255,255,.72);
            animation: aa-student-card-in .5s ease-out both;
        }

        .student-empty-icon {
            width: 46px;
            height: 46px;
            margin: 0 auto 12px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #EAF3FF;
            color: #2F78D0 !important;
            font-size: 26px !important;
            font-weight: 500 !important;
        }

        .student-empty-title {
            color: #142A46 !important;
            font-size: 20px !important;
            font-weight: 900 !important;
        }

        .student-empty-copy {
            color: #718097 !important;
            font-size: 14px !important;
            margin-top: 5px;
        }

        .student-subject-inner {
            padding: 1px 0 7px;
        }

        .student-subject-kicker {
            color: #2F78D0 !important;
            font-size: 11px !important;
            letter-spacing: .13em;
            font-weight: 900 !important;
        }

        .student-subject-title {
            color: #142A46 !important;
            font-size: 22px !important;
            font-weight: 900 !important;
            margin-top: 5px;
        }

        .student-subject-meta {
            color: #6C7890 !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            margin-top: 7px;
        }

        .student-subject-code {
            color: #2F78D0 !important;
            font-weight: 900 !important;
        }

        .student-subject-separator {
            color: #AFBCCB !important;
            padding: 0 7px;
        }

        .student-subject-stat {
            margin-top: 13px;
            padding: 12px 13px;
            border-radius: 13px;
            background: #F5F8FC;
            border: 1px solid #E5ECF4;
        }

        .student-subject-stat-value {
            color: #142A46 !important;
            font-size: 22px !important;
            font-weight: 900 !important;
            line-height: 1.05;
        }

        .student-subject-stat-label {
            color: #718097 !important;
            font-size: 11px !important;
            font-weight: 800 !important;
            margin-top: 3px;
            text-transform: uppercase;
            letter-spacing: .05em;
        }

        .student-status-meta {
            color: #718097 !important;
            font-size: 12px !important;
            font-weight: 700 !important;
            text-align: right;
            margin-top: 8px;
        }

        .student-subject-progress-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-top: 15px;
        }

        .student-subject-progress-label {
            color: #718097 !important;
            font-size: 11px !important;
            font-weight: 850 !important;
            text-transform: uppercase;
            letter-spacing: .07em;
        }

        .student-subject-progress-value {
            color: #2F78D0 !important;
            font-size: 14px !important;
            font-weight: 900 !important;
        }

        .student-subject-progress-track {
            width: 100%;
            height: 8px;
            margin-top: 8px;
            border-radius: 999px;
            overflow: hidden;
            background: #E8EEF6;
        }

        .student-subject-progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #2F78D0 0%, #5B4BC4 100%);
            box-shadow: 0 0 12px rgba(47,120,208,.20);
            transition: width .45s ease;
        }

        /* ===== Inputs / selectors ===== */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input,
        .stSelectbox input {
            min-height: 50px !important;
            border-radius: 13px !important;
            border-color: rgba(75,123,175,.26) !important;
            background: rgba(255,255,255,.94) !important;
            color: var(--aa-text) !important;
            font-size: 17px !important;
            font-weight: 650 !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #718097 !important;
            opacity: 1 !important;
        }

        .stTextInput > div > div:focus-within,
        .stTextArea > div > div:focus-within,
        .stNumberInput > div > div:focus-within,
        .stDateInput > div > div:focus-within,
        .stTimeInput > div > div:focus-within,
        .stSelectbox > div > div:focus-within {
            border-color: #2F78D0 !important;
            box-shadow: 0 0 0 3px rgba(47,120,208,.13), 0 8px 22px rgba(47,120,208,.07) !important;
        }

        /* ===== Tables / alerts / toast ===== */
        [data-testid="stDataFrame"] {
            border-radius: 16px !important;
            overflow: hidden !important;
            box-shadow: 0 14px 32px rgba(31,65,105,.08) !important;
        }

        .stAlert {
            border-radius: 14px !important;
            font-size: 16px !important;
            font-weight: 760 !important;
        }

        [data-testid="stToast"] {
            background: #142A46 !important;
            border: 1px solid rgba(255,255,255,.14) !important;
            border-radius: 15px !important;
            box-shadow: 0 18px 38px rgba(20,42,70,.24) !important;
        }

        [data-testid="stToast"] * {
            color: #FFFFFF !important;
            font-size: 16px !important;
            font-weight: 800 !important;
        }

        /* ===== Keep dark custom surfaces readable ===== */
        .dark-surface,
        .dark-surface *,
        .aa-auth-brand,
        .aa-auth-brand *,
        .teacher-footer-banner,
        .teacher-footer-banner *,
        .teacher-camera-preview,
        .teacher-camera-preview * {
            color: #FFFFFF !important;
        }

        /* ===== Status colours ===== */
        .status-present,
        .status-success {
            color: #147A53 !important;
            background: #E4F7EF !important;
        }

        .status-warning {
            color: #9A6700 !important;
            background: #FFF5D6 !important;
        }

        .status-error {
            color: var(--aa-red) !important;
            background: #FBEAEA !important;
        }

        /* ===== Global motion ===== */
        .block-container {
            animation: aa-page-in .58s ease-out both !important;
        }

        @keyframes aa-product-bg {
            from { background-position: 0% 0%, 100% 0%, 70% 90%, 0% 0%; }
            to { background-position: 12% 9%, 88% 16%, 62% 82%, 0% 0%; }
        }

        @keyframes aa-student-hero-in {
            from { opacity: 0; transform: translateY(10px) scale(.99); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes aa-student-card-in {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes aa-status-pulse {
            0% { box-shadow: 0 0 0 0 rgba(32,180,119,.42); }
            72% { box-shadow: 0 0 0 9px rgba(32,180,119,0); }
            100% { box-shadow: 0 0 0 0 rgba(32,180,119,0); }
        }

        @keyframes aa-page-in {
            from { opacity: 0; transform: translateY(9px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 900px) {
            .student-welcome {
                flex-direction: column;
                align-items: flex-start;
                padding: 24px;
            }

            .student-stat-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .student-section-heading {
                align-items: flex-start;
                flex-direction: column;
            }

            .student-status-meta {
                text-align: left;
            }

            .student-section-copy {
                text-align: left;
            }

            .stApp p,
            .stApp li,
            .stApp [data-testid="stMarkdownContainer"],
            .stApp [data-testid="stMarkdownContainer"] p {
                font-size: 16px !important;
            }

            .stButton > button,
            .stDownloadButton > button {
                min-height: 52px !important;
                font-size: 16px !important;
            }

            .stApp h1 {
                font-size: 2.35rem !important;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: .01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: .01ms !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
