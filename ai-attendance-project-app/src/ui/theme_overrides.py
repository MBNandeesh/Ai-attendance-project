import streamlit as st


BLUE = "#6290C3"
MINT = "#C2E7DA"
PALE = "#F1FFE7"
NAVY = "#1A1B41"
LIME = "#BAFF29"
RED = "#D64545"


def style_theme_overrides():
    st.markdown(
        f"""
        <style>
            :root {{
                --ux-blue: {BLUE};
                --ux-mint: {MINT};
                --ux-pale: {PALE};
                --ux-navy: {NAVY};
                --ux-lime: {LIME};
                --ux-red: {RED};
            }}

            .stApp {{
                background:
                    radial-gradient(circle at 88% 5%, rgba(194,231,218,.78), transparent 24%),
                    radial-gradient(circle at 8% 76%, rgba(98,144,195,.18), transparent 27%),
                    radial-gradient(circle at 74% 94%, rgba(241,255,231,.92), transparent 29%),
                    linear-gradient(135deg, #FBFDFC 0%, #EDF7F4 50%, #F1FFE7 100%) !important;
                background-attachment: fixed !important;
            }}

            .stApp::before {{
                content:"";
                position:fixed;
                inset:-25%;
                z-index:0;
                pointer-events:none;
                background:
                    radial-gradient(circle at 20% 18%, rgba(98,144,195,.09) 0 2px, transparent 3px),
                    radial-gradient(circle at 76% 24%, rgba(186,255,41,.11) 0 2px, transparent 3px),
                    radial-gradient(circle at 56% 82%, rgba(194,231,218,.12) 0 2px, transparent 3px);
                background-size:190px 190px, 250px 250px, 220px 220px;
                animation:ux-particle-drift 20s linear infinite;
            }}

            .block-container {{ position:relative; z-index:1; animation:ux-page-in .62s cubic-bezier(.2,.8,.2,1) both; }}

            body,.stApp,[data-testid="stMarkdownContainer"],.stCaption,label {{ font-size:16px !important; }}
            h1 {{ font-size:clamp(2.45rem,4.8vw,4.1rem) !important; font-weight:950 !important; color:var(--ux-navy) !important; }}
            h2 {{ font-size:clamp(1.9rem,3.1vw,2.45rem) !important; font-weight:950 !important; color:var(--ux-navy) !important; }}
            h3 {{ font-size:1.38rem !important; font-weight:900 !important; color:var(--ux-navy) !important; }}
            h4 {{ font-size:1.12rem !important; font-weight:900 !important; color:var(--ux-navy) !important; }}

            .app-topbar,.teacher-topbar {{
                background:linear-gradient(135deg,#121331 0%,var(--ux-navy) 57%,#2B2E5E 100%) !important;
                color:#FFFFFF !important; border-color:rgba(255,255,255,.12) !important;
                box-shadow:0 20px 44px rgba(26,27,65,.22) !important;
            }}
            .app-topbar .brand-name,.app-topbar .brand-tagline,.app-topbar .topbar-status,
            .app-topbar .topbar-status-soft,.teacher-topbar * {{ color:#FFFFFF !important; }}
            .app-topbar .brand-tagline,.app-topbar .topbar-status-soft,.teacher-profile-role {{ color:rgba(255,255,255,.72) !important; }}
            .app-topbar .topbar-status {{ background:rgba(194,231,218,.12) !important; border-color:rgba(194,231,218,.25) !important; }}
            .app-topbar .brand-mark {{ background:linear-gradient(145deg,#FFFFFF,var(--ux-mint)) !important; color:var(--ux-navy) !important; }}
            .teacher-topbar {{ position:relative; overflow:hidden; }}
            .teacher-topbar::after,.app-topbar::after {{ content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(105deg,transparent 35%,rgba(194,231,218,.15) 50%,transparent 64%);transform:translateX(-120%);animation:ux-shimmer 5.8s ease-in-out infinite; }}
            .teacher-search {{ background:rgba(255,255,255,.10) !important;border-color:rgba(255,255,255,.18) !important;color:rgba(255,255,255,.82) !important;font-size:16px !important; }}
            .teacher-profile-name {{ color:#FFFFFF !important;font-size:18px !important;font-weight:950 !important; }}
            .teacher-profile-role {{ font-size:13px !important; }}
            .teacher-bell {{ background:rgba(255,255,255,.10) !important;border-color:rgba(255,255,255,.16) !important;color:#FFFFFF !important; }}

            section[data-testid="stSidebar"] {{ background:radial-gradient(circle at 80% 10%,rgba(98,144,195,.24),transparent 23%),linear-gradient(180deg,#11122F 0%,var(--ux-navy) 57%,#10122D 100%) !important; }}
            section[data-testid="stSidebar"] * {{ color:#FFFFFF !important; }}
            section[data-testid="stSidebar"] .sidebar-brand-subtitle,section[data-testid="stSidebar"] .sidebar-section-label,section[data-testid="stSidebar"] .sidebar-user-role {{ color:rgba(255,255,255,.68) !important; }}
            section[data-testid="stSidebar"] .stButton > button {{ min-height:54px !important;font-size:16px !important;font-weight:900 !important;border-radius:15px !important;transition:transform .2s ease,box-shadow .2s ease,background .2s ease !important; }}
            section[data-testid="stSidebar"] .stButton > button[kind="tertiary"] {{ background:transparent !important;border-color:transparent !important;color:#FFFFFF !important; }}
            section[data-testid="stSidebar"] .stButton > button[kind="tertiary"]:hover {{ background:rgba(194,231,218,.10) !important;transform:translateX(5px) !important; }}
            section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{ background:linear-gradient(135deg,var(--ux-blue),#7DA7CF) !important;color:var(--ux-navy) !important;box-shadow:0 12px 30px rgba(98,144,195,.30) !important;animation:ux-active-pulse 2.7s ease-in-out infinite; }}
            section[data-testid="stSidebar"] .stButton > button[kind="primary"] * {{ color:var(--ux-navy) !important; }}

            .stButton > button,.stDownloadButton > button {{ min-height:54px !important;padding:.68rem 1.15rem !important;border-radius:15px !important;font-size:17px !important;font-weight:900 !important;letter-spacing:.005em !important;transition:transform .22s ease,box-shadow .22s ease,filter .22s ease !important; }}
            .stButton > button:hover,.stDownloadButton > button:hover {{ transform:translateY(-3px) scale(1.01) !important;filter:brightness(1.03) !important; }}
            .stButton > button[kind="primary"] {{ position:relative !important;overflow:hidden !important;background:linear-gradient(110deg,#536F9E 0%,var(--ux-blue) 52%,var(--ux-navy) 100%) !important;color:#FFFFFF !important;border:0 !important;box-shadow:0 14px 32px rgba(98,144,195,.28) !important; }}
            .stButton > button[kind="primary"]::after {{ content:"";position:absolute;left:-70%;top:0;width:34%;height:100%;background:linear-gradient(90deg,transparent,rgba(186,255,41,.38),transparent);transform:skewX(-20deg);animation:ux-button-glint 3.2s ease-in-out infinite;pointer-events:none; }}
            .stButton > button[kind="primary"]:hover {{ background:linear-gradient(110deg,#789FC9,var(--ux-blue),var(--ux-navy)) !important;box-shadow:0 18px 38px rgba(26,27,65,.24) !important; }}
            .stButton > button[kind="secondary"] {{ background:linear-gradient(135deg,#FFFFFF,var(--ux-pale)) !important;color:var(--ux-navy) !important;border:1px solid rgba(98,144,195,.28) !important;box-shadow:0 10px 24px rgba(26,27,65,.07) !important; }}
            .stButton > button[kind="tertiary"] {{ font-size:16px !important;font-weight:850 !important;color:var(--ux-navy) !important; }}

            [data-testid="stIconMaterial"],[data-testid="stIconMaterial"] *,span[class*="material-symbols"],span[class*="Material-Symbols"] {{ font-family:'Material Symbols Rounded' !important;color:inherit !important; }}

            [data-testid="stVerticalBlockBorderWrapper"],.teacher-card,.teacher-stat-card {{ border-color:rgba(98,144,195,.20) !important;background:rgba(255,255,255,.94) !important;box-shadow:0 15px 36px rgba(26,27,65,.075) !important;animation:ux-card-in .62s cubic-bezier(.2,.8,.2,1) both; }}
            [data-testid="stVerticalBlockBorderWrapper"]:hover,.teacher-card:hover,.teacher-stat-card:hover {{ transform:translateY(-5px) !important;border-color:rgba(98,144,195,.38) !important;box-shadow:0 22px 46px rgba(98,144,195,.16) !important; }}

            .stTextInput input,.stTextArea textarea,.stSelectbox input,.stNumberInput input,.stDateInput input,.stTimeInput input {{ min-height:48px !important;font-size:17px !important;font-weight:650 !important; }}
            .stTextInput > label,.stTextArea > label,.stSelectbox > label,.stNumberInput > label,.stDateInput > label,.stTimeInput > label,.stMultiSelect > label,.stRadio > label,.stCheckbox > label {{ font-size:16px !important;font-weight:850 !important;color:var(--ux-navy) !important; }}
            .stTextInput > div > div:focus-within,.stTextArea > div > div:focus-within,.stSelectbox > div > div:focus-within,.stNumberInput > div > div:focus-within,.stDateInput > div > div:focus-within,.stTimeInput > div > div:focus-within {{ border-color:var(--ux-blue) !important;box-shadow:0 0 0 4px rgba(98,144,195,.15),0 10px 22px rgba(98,144,195,.10) !important; }}

            .stAlert,div[role="alert"] {{ border-radius:17px !important;font-size:16px !important;font-weight:800 !important;animation:ux-alert-in .48s ease-out both;box-shadow:0 12px 28px rgba(26,27,65,.09) !important; }}
            .stAlert p,.stAlert [data-testid="stMarkdownContainer"],div[role="alert"] p {{ font-size:16px !important;font-weight:800 !important; }}
            /* Brand colors by default. Reserve red for warning/error components. */
            .stAlert {{ border-left:5px solid var(--ux-blue) !important; }}

            [data-testid="stMetric"] {{ border-top:4px solid var(--ux-blue) !important;animation:ux-card-in .62s ease-out both; }}
            [data-testid="stMetricLabel"] {{ font-size:15px !important;font-weight:850 !important; }}
            [data-testid="stMetricValue"] {{ font-size:2.05rem !important;font-weight:950 !important;color:var(--ux-navy) !important; }}
            button[data-baseweb="tab"] {{ font-size:16px !important;font-weight:850 !important; }}
            button[data-baseweb="tab"][aria-selected="true"] {{ color:var(--ux-navy) !important;border-bottom-color:var(--ux-lime) !important; }}
            [data-testid="stExpander"] {{ border-color:rgba(98,144,195,.22) !important;border-radius:17px !important;animation:ux-card-in .58s ease-out both; }}
            [data-testid="stExpander"] summary {{ font-size:16px !important;font-weight:850 !important; }}
            [data-testid="stDataFrame"] {{ animation:ux-card-in .62s ease-out both;border-radius:17px !important; }}

            [data-testid="stCameraInput"],[data-testid="stAudioInput"] {{ border-radius:20px !important;animation:ux-card-in .65s cubic-bezier(.2,.8,.2,1) both; }}
            [data-testid="stCameraInput"] button,[data-testid="stAudioInput"] button {{ font-size:17px !important;font-weight:900 !important; }}

            .teacher-greeting h1,.teacher-card-title,.teacher-stat-value {{ color:var(--ux-navy) !important; }}
            .teacher-greeting h1 {{ font-size:clamp(2.2rem,4vw,3.6rem) !important; }}
            .teacher-greeting p {{ color:#52657C !important;font-size:17px !important;font-weight:650 !important; }}
            .teacher-date-card {{ background:linear-gradient(135deg,#FFFFFF,var(--ux-pale)) !important; }}
            .teacher-date-sub {{ display:none !important; }}
            .teacher-stat-card:nth-child(1) {{ background:linear-gradient(135deg,var(--ux-blue),#7EA9D2) !important;color:#FFFFFF !important; }}
            .teacher-stat-card:nth-child(2) {{ background:linear-gradient(135deg,#D8F1E8,var(--ux-mint)) !important; }}
            .teacher-stat-card:nth-child(3) {{ background:linear-gradient(135deg,#F8FFE9,var(--ux-pale)) !important; }}
            .teacher-stat-card:nth-child(4) {{ background:linear-gradient(135deg,var(--ux-navy),#2D3165) !important;color:#FFFFFF !important; }}
            .teacher-stat-card:nth-child(1) *, .teacher-stat-card:nth-child(4) * {{ color:#FFFFFF !important; }}
            .teacher-stat-ring {{ background:conic-gradient(var(--ux-lime) var(--pct),rgba(255,255,255,.28) 0) !important; }}
            .teacher-live-dot,.teacher-recognized {{ background:var(--ux-lime) !important;color:var(--ux-navy) !important; }}
            .teacher-camera-frame {{ border-color:var(--ux-lime) !important;animation:ux-camera-pulse 2.25s ease-in-out infinite !important; }}
            .teacher-camera-preview::before {{ background:linear-gradient(90deg,transparent,var(--ux-lime),transparent) !important;box-shadow:0 0 20px rgba(186,255,41,.65) !important; }}
            .teacher-table th {{ font-size:13px !important;font-weight:900 !important;color:var(--ux-navy) !important;background:#EDF5F4 !important; }}
            .teacher-table td {{ font-size:14px !important;font-weight:700 !important; }}
            .teacher-status.present {{ background:var(--ux-mint) !important;color:#16745A !important; }}
            .teacher-status.absent {{ background:#FFF3DA !important;color:#B7791F !important; }}
            .teacher-footer-banner {{ display:none !important; }}

            /* Owner footer: name only. */
            .app-footer-minimal {{ justify-content:center !important;border-top:0 !important;padding-top:2.4rem !important;margin-top:2.7rem !important;animation:ux-fade-up .8s ease-out both; }}
            .footer-credit-only {{ color:var(--ux-navy) !important;font-size:16px !important;font-weight:950 !important;letter-spacing:.08em !important; }}

            .ui-hero {{ background:linear-gradient(135deg,#FFFFFF 0%,#F5FBF8 48%,var(--ux-pale) 100%) !important;box-shadow:0 24px 56px rgba(98,144,195,.13) !important; }}
            .ui-hero-gradient-text {{ background:linear-gradient(90deg,var(--ux-blue),var(--ux-navy),var(--ux-lime),var(--ux-blue)) !important;background-size:240% 100% !important;-webkit-background-clip:text !important;background-clip:text !important;color:transparent !important;animation:ux-gradient-flow 5s ease infinite; }}
            .ui-card-title,.ui-feature-title {{ font-size:1.16rem !important;font-weight:900 !important; }}
            .ui-card-copy,.ui-feature-copy {{ font-size:.96rem !important;font-weight:650 !important;line-height:1.62 !important; }}

            /* Welcome toasts: white text on navy, exactly as requested. */
            [data-testid="stToast"] {{
                background:linear-gradient(135deg,var(--ux-navy),var(--ux-blue)) !important;
                border:1px solid rgba(194,231,218,.30) !important;
                color:#FFFFFF !important;
                box-shadow:0 20px 44px rgba(26,27,65,.28) !important;
                animation:ux-toast-in .5s cubic-bezier(.2,.8,.2,1) both !important;
            }}
            [data-testid="stToast"] * {{ color:#FFFFFF !important;font-size:16px !important;font-weight:900 !important; }}

            @keyframes ux-page-in {{ from{{opacity:0;transform:translateY(14px)}} to{{opacity:1;transform:translateY(0)}} }}
            @keyframes ux-card-in {{ from{{opacity:0;transform:translateY(18px) scale(.985)}} to{{opacity:1;transform:translateY(0) scale(1)}} }}
            @keyframes ux-alert-in {{ from{{opacity:0;transform:translateX(-14px)}} to{{opacity:1;transform:translateX(0)}} }}
            @keyframes ux-toast-in {{ from{{opacity:0;transform:translateY(14px) scale(.97)}} to{{opacity:1;transform:translateY(0) scale(1)}} }}
            @keyframes ux-fade-up {{ from{{opacity:0;transform:translateY(12px)}} to{{opacity:1;transform:translateY(0)}} }}
            @keyframes ux-shimmer {{ 0%,35%{{transform:translateX(-120%)}} 58%,100%{{transform:translateX(165%)}} }}
            @keyframes ux-button-glint {{ 0%,22%{{left:-70%;opacity:0}} 32%{{opacity:1}} 54%{{left:140%;opacity:0}} 100%{{left:140%;opacity:0}} }}
            @keyframes ux-active-pulse {{ 0%,100%{{box-shadow:0 12px 30px rgba(98,144,195,.25)}} 50%{{box-shadow:0 17px 38px rgba(98,144,195,.40)}} }}
            @keyframes ux-gradient-flow {{ 0%,100%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} }}
            @keyframes ux-camera-pulse {{ 0%,100%{{box-shadow:0 0 0 7px rgba(186,255,41,.06),0 0 25px rgba(186,255,41,.08)}} 50%{{box-shadow:0 0 0 12px rgba(186,255,41,.10),0 0 45px rgba(186,255,41,.20)}} }}
            @keyframes ux-particle-drift {{ from{{transform:translate3d(0,0,0)}} to{{transform:translate3d(45px,30px,0)}} }}

            @media (prefers-reduced-motion: reduce) {{ *,*::before,*::after {{ animation-duration:.01ms !important;animation-iteration-count:1 !important;transition-duration:.01ms !important; }} }}
        </style>
        """,
        unsafe_allow_html=True,
    )
