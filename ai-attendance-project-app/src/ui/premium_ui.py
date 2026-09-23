import html

import streamlit as st


BLUE = "#6290C3"
MINT = "#C2E7DA"
CREAM = "#F1FFE7"
NAVY = "#1A1B41"
LIME = "#BAFF29"
WHITE = "#FFFFFF"
BORDER = "#E8EDF2"
ERROR = "#EF4444"
MUTED = "#5E6A82"


def apply_premium_ui():
    """UI-only theme layer. Does not alter application state or behaviour."""
    st.markdown(
        f"""
        <style>
        :root {{
            --aa-blue:{BLUE};
            --aa-mint:{MINT};
            --aa-cream:{CREAM};
            --aa-navy:{NAVY};
            --aa-lime:{LIME};
            --aa-white:{WHITE};
            --aa-border:{BORDER};
            --aa-error:{ERROR};
            --aa-muted:{MUTED};
        }}

        html, body {{
            background: var(--aa-cream) !important;
        }}

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .block-container {{
            color: var(--aa-navy) !important;
        }}

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background:
                radial-gradient(circle at 6% 12%, rgba(98,144,195,.24), transparent 25%),
                radial-gradient(circle at 94% 16%, rgba(194,231,218,.42), transparent 28%),
                radial-gradient(circle at 80% 88%, rgba(186,255,41,.08), transparent 22%),
                linear-gradient(145deg, #F1FFE7 0%, #F8FFF3 48%, #E8F2FB 100%) !important;
            background-size: 125% 125%, 130% 130%, 125% 125%, 100% 100% !important;
            background-attachment: fixed !important;
            animation: aa-bg-flow 18s ease-in-out infinite alternate !important;
        }}

        [data-testid="stMainBlockContainer"], .block-container {{
            background: transparent !important;
        }}

        /* Global typography */
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stText"],
        .stCaption,
        .stAlert,
        [data-testid="stToast"] {{
            font-size: 17px !important;
        }}

        h1, h2, h3, h4 {{
            color: var(--aa-navy) !important;
            letter-spacing: -.028em !important;
        }}
        h1 {{ font-size: clamp(2.25rem,4vw,3.8rem) !important; font-weight: 900 !important; line-height:1.06 !important; }}
        h2 {{ font-size: clamp(1.8rem,3vw,2.6rem) !important; font-weight: 900 !important; }}
        h3 {{ font-size: 1.42rem !important; font-weight: 850 !important; }}
        h4 {{ font-size: 1.18rem !important; font-weight: 850 !important; }}
        label {{ font-size:16px !important; font-weight:800 !important; color:var(--aa-navy) !important; }}

        /* Header */
        .app-topbar {{
            background: linear-gradient(135deg, var(--aa-navy) 0%, #202657 55%, var(--aa-blue) 145%) !important;
            border:1px solid rgba(255,255,255,.12) !important;
            box-shadow:0 18px 44px rgba(26,27,65,.24) !important;
            animation:aa-rise .48s ease-out both !important;
        }}
        .app-topbar, .app-topbar * {{ color:var(--aa-white) !important; }}
        .app-topbar .brand-tagline,
        .app-topbar .topbar-status,
        .app-topbar .topbar-status-soft {{ display:none !important; }}
        .app-topbar .brand-mark {{
            background:var(--aa-white) !important;
            color:var(--aa-navy) !important;
            box-shadow:0 8px 22px rgba(0,0,0,.20) !important;
            animation:aa-float 4s ease-in-out infinite !important;
        }}
        .app-topbar .brand-name {{ font-size:1.15rem !important; font-weight:900 !important; }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background:
                radial-gradient(circle at 88% 8%, rgba(98,144,195,.25), transparent 24%),
                linear-gradient(180deg, #11152F 0%, var(--aa-navy) 62%, #304B77 145%) !important;
            border-right:1px solid rgba(255,255,255,.10) !important;
            animation:aa-sidebar-flow 14s ease-in-out infinite alternate !important;
        }}
        section[data-testid="stSidebar"] * {{ color:var(--aa-white) !important; }}
        section[data-testid="stSidebar"] .stButton > button {{
            min-height:50px !important;
            border-radius:14px !important;
            font-size:16px !important;
            font-weight:850 !important;
            transition:transform .18s ease, box-shadow .18s ease, background .18s ease !important;
        }}
        section[data-testid="stSidebar"] .stButton > button[kind="tertiary"] {{
            background:transparent !important;
            border-color:transparent !important;
            box-shadow:none !important;
            color:var(--aa-white) !important;
        }}
        section[data-testid="stSidebar"] .stButton > button[kind="tertiary"]:hover {{
            background:rgba(194,231,218,.12) !important;
            box-shadow:inset 3px 0 0 var(--aa-lime) !important;
            transform:translateX(4px) !important;
        }}
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
            background:var(--aa-blue) !important;
            color:var(--aa-white) !important;
            border-color:rgba(255,255,255,.12) !important;
            box-shadow:0 12px 26px rgba(98,144,195,.28) !important;
        }}

        /* Standard controls */
        .stButton > button,
        .stDownloadButton > button {{
            min-height:52px !important;
            border-radius:14px !important;
            padding:.62rem 1.15rem !important;
            font-size:17px !important;
            font-weight:850 !important;
            transition:transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
        }}
        .stButton > button[kind="primary"] {{
            background:linear-gradient(105deg, var(--aa-blue) 0%, #5796CF 45%, var(--aa-lime) 125%) !important;
            color:var(--aa-navy) !important;
            border:0 !important;
            box-shadow:0 13px 30px rgba(98,144,195,.30) !important;
            position:relative !important;
            overflow:hidden !important;
        }}
        .stButton > button[kind="primary"]::after {{
            content:"";
            position:absolute;
            inset:0 auto 0 -42%;
            width:28%;
            background:linear-gradient(90deg,transparent,rgba(255,255,255,.34),transparent);
            transform:skewX(-18deg);
            animation:aa-button-sheen 3.6s ease-in-out infinite;
            pointer-events:none;
        }}
        .stButton > button[kind="primary"]:hover {{
            transform:translateY(-2px) scale(1.01) !important;
            box-shadow:0 18px 36px rgba(98,144,195,.38), 0 0 0 2px rgba(186,255,41,.12) !important;
            filter:saturate(1.05) !important;
        }}
        .stButton > button[kind="primary"]:active {{ transform:translateY(0) scale(.995) !important; }}
        .stButton > button[kind="secondary"] {{
            background:rgba(255,255,255,.80) !important;
            color:var(--aa-navy) !important;
            border-color:rgba(98,144,195,.28) !important;
        }}
        .stButton > button[kind="secondary"]:hover {{
            background:rgba(194,231,218,.52) !important;
            border-color:var(--aa-blue) !important;
            transform:translateY(-2px) !important;
            box-shadow:0 12px 26px rgba(26,27,65,.10) !important;
        }}
        .stButton > button[kind="tertiary"] {{
            color:var(--aa-navy) !important;
            font-weight:800 !important;
            background:transparent !important;
            border-color:transparent !important;
            box-shadow:none !important;
        }}

        /* Cards */
        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stExpander"] {{
            background:rgba(255,255,255,.94) !important;
            border:1px solid rgba(98,144,195,.20) !important;
            border-radius:20px !important;
            box-shadow:0 16px 38px rgba(26,27,65,.09) !important;
            animation:aa-card-in .48s cubic-bezier(.2,.8,.2,1) both !important;
            transition:transform .20s ease, box-shadow .20s ease, border-color .20s ease !important;
        }}
        [data-testid="stVerticalBlockBorderWrapper"]:hover,
        [data-testid="stExpander"]:hover {{
            transform:translateY(-4px) !important;
            border-color:rgba(98,144,195,.40) !important;
            box-shadow:0 22px 44px rgba(26,27,65,.13) !important;
        }}

        /* Inputs */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox input,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input {{
            min-height:48px !important;
            border-radius:13px !important;
            border-color:rgba(98,144,195,.30) !important;
            background:rgba(255,255,255,.96) !important;
            color:var(--aa-navy) !important;
            font-size:17px !important;
            transition:border-color .18s ease, box-shadow .18s ease, transform .18s ease !important;
        }}
        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus,
        .stTimeInput input:focus {{
            border-color:var(--aa-blue) !important;
            box-shadow:0 0 0 3px rgba(98,144,195,.15), 0 8px 20px rgba(26,27,65,.06) !important;
            transform:translateY(-1px) !important;
            outline:none !important;
        }}

        /* Toast and messages */
        [data-testid="stToast"] {{
            background:var(--aa-navy) !important;
            color:var(--aa-white) !important;
            border:1px solid rgba(255,255,255,.14) !important;
            border-radius:15px !important;
            box-shadow:0 18px 38px rgba(26,27,65,.26) !important;
            animation:aa-toast .32s ease-out both !important;
        }}
        [data-testid="stToast"] * {{ color:var(--aa-white) !important; font-size:16px !important; font-weight:800 !important; }}
        .stAlert {{ border-radius:14px !important; font-weight:760 !important; }}

        /* Metrics / data */
        [data-testid="stMetric"] {{
            background:rgba(255,255,255,.95) !important;
            border:1px solid rgba(98,144,195,.20) !important;
            border-top:4px solid var(--aa-lime) !important;
            border-radius:18px !important;
            box-shadow:0 14px 32px rgba(26,27,65,.09) !important;
            animation:aa-card-in .55s ease-out both !important;
            transition:transform .20s ease, box-shadow .20s ease !important;
        }}
        [data-testid="stMetric"]:hover {{ transform:translateY(-4px) !important; box-shadow:0 20px 38px rgba(26,27,65,.13) !important; }}
        [data-testid="stMetricValue"] {{ color:var(--aa-navy) !important; font-size:2rem !important; font-weight:900 !important; }}
        [data-testid="stMetricLabel"] {{ color:var(--aa-muted) !important; font-weight:800 !important; }}
        [data-testid="stDataFrame"] {{ border-radius:16px !important; overflow:hidden !important; box-shadow:0 14px 30px rgba(26,27,65,.08) !important; animation:aa-card-in .55s ease-out both !important; }}

        /* Authentication split-screen */
        .st-key-teacher-auth-layout,
        .st-key-student-auth-layout {{
            max-width:1220px !important;
            margin:2vh auto 0 !important;
            padding:0 !important;
            animation:aa-auth-enter .50s cubic-bezier(.2,.8,.2,1) both !important;
        }}
        .st-key-teacher-auth-layout > div,
        .st-key-student-auth-layout > div {{
            gap:1.25rem !important;
        }}
        .st-key-teacher-auth-layout .st-key-teacher-auth-card,
        .st-key-student-auth-layout .st-key-student-auth-card {{
            background:rgba(255,255,255,.92) !important;
            border:1px solid rgba(255,255,255,.80) !important;
            border-radius:26px !important;
            padding:clamp(1.15rem,2.5vw,2rem) !important;
            box-shadow:0 26px 70px rgba(26,27,65,.16) !important;
            backdrop-filter:blur(14px) !important;
            -webkit-backdrop-filter:blur(14px) !important;
            position:relative !important;
            overflow:hidden !important;
        }}
        .st-key-teacher-auth-layout .st-key-teacher-auth-card::before,
        .st-key-student-auth-layout .st-key-student-auth-card::before {{
            content:"";
            position:absolute;
            width:240px;
            height:240px;
            right:-120px;
            top:-120px;
            border-radius:50%;
            background:radial-gradient(circle, rgba(194,231,218,.60), transparent 70%);
            pointer-events:none;
            animation:aa-orbit 8s ease-in-out infinite;
        }}

        .aa-auth-brand {{
            min-height:630px;
            border-radius:28px;
            overflow:hidden;
            padding:clamp(1.6rem,4vw,3rem);
            position:relative;
            display:flex;
            flex-direction:column;
            justify-content:center;
            color:var(--aa-white);
            background:
                radial-gradient(circle at 85% 16%, rgba(194,231,218,.24), transparent 24%),
                radial-gradient(circle at 15% 75%, rgba(98,144,195,.38), transparent 30%),
                linear-gradient(145deg, #12152F 0%, var(--aa-navy) 58%, #315883 140%);
            box-shadow:0 26px 70px rgba(26,27,65,.25);
            isolation:isolate;
        }}
        .aa-auth-brand::before {{
            content:"";
            position:absolute;
            width:430px;height:430px;right:-180px;bottom:-210px;border-radius:44% 56% 49% 51%;
            background:radial-gradient(circle at 35% 35%, rgba(194,231,218,.56), rgba(98,144,195,.14) 46%, transparent 72%);
            z-index:-1;
            animation:aa-blob 10s ease-in-out infinite;
        }}
        .aa-auth-brand::after {{
            content:"";
            position:absolute;
            width:2px;height:118%;right:46%;top:-8%;
            background:linear-gradient(to bottom, transparent, rgba(194,231,218,.12), var(--aa-lime), rgba(194,231,218,.08), transparent);
            opacity:.52;
            transform:rotate(16deg);
            z-index:-1;
            animation:aa-scan 4.8s ease-in-out infinite;
        }}
        .aa-auth-logo {{ display:flex;align-items:center;gap:12px;margin-bottom:1.8rem; }}
        .aa-auth-logo-mark {{ width:48px;height:48px;border-radius:15px;background:var(--aa-white);color:var(--aa-navy);display:flex;align-items:center;justify-content:center;font-weight:950;box-shadow:0 12px 28px rgba(0,0,0,.18);animation:aa-float 4s ease-in-out infinite; }}
        .aa-auth-logo-name {{ font-size:1.15rem;font-weight:900;letter-spacing:-.02em; }}
        .aa-auth-kicker {{ color:var(--aa-mint);font-size:.73rem;font-weight:900;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.75rem; }}
        .aa-auth-title {{ margin:0;color:var(--aa-white);font-size:clamp(2.35rem,4vw,4rem);line-height:1.02;font-weight:950;letter-spacing:-.045em; }}
        .aa-auth-accent {{ color:var(--aa-lime); }}
        .aa-auth-copy {{ margin-top:1rem;color:rgba(255,255,255,.76);font-size:1rem;line-height:1.7;max-width:560px; }}
        .aa-auth-features {{ display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:2rem; }}
        .aa-auth-feature {{ padding:12px;border:1px solid rgba(194,231,218,.16);border-radius:15px;background:rgba(255,255,255,.06);backdrop-filter:blur(8px);transition:transform .18s ease,border-color .18s ease,background .18s ease; }}
        .aa-auth-feature:hover {{ transform:translateY(-3px);border-color:rgba(186,255,41,.45);background:rgba(194,231,218,.09); }}
        .aa-auth-feature-icon {{ width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;background:rgba(194,231,218,.12);color:var(--aa-lime);margin-bottom:8px;font-size:18px; }}
        .aa-auth-feature-title {{ color:var(--aa-white);font-size:.83rem;font-weight:900; }}
        .aa-auth-feature-copy {{ margin-top:3px;color:rgba(255,255,255,.62);font-size:.68rem;line-height:1.45; }}
        .aa-recognition-visual {{ margin-top:2rem;height:205px;border-radius:22px;border:1px solid rgba(194,231,218,.18);background:linear-gradient(155deg,rgba(255,255,255,.06),rgba(98,144,195,.10));position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 55px rgba(0,0,0,.14); }}
        .aa-recognition-visual::before {{ content:"";position:absolute;left:8%;right:8%;top:18%;height:2px;background:linear-gradient(90deg,transparent,var(--aa-lime),transparent);box-shadow:0 0 18px rgba(186,255,41,.42);animation:aa-rec-scan 2.6s linear infinite; }}
        .aa-face-ring {{ width:110px;height:110px;border:2px solid rgba(186,255,41,.78);border-radius:34px;position:relative;box-shadow:0 0 0 8px rgba(186,255,41,.05),0 0 30px rgba(186,255,41,.12);animation:aa-face-pulse 2.2s ease-in-out infinite; }}
        .aa-face-ring::before,.aa-face-ring::after {{ content:"";position:absolute;width:26px;height:26px;border-color:var(--aa-lime);border-style:solid; }}
        .aa-face-ring::before {{ left:-2px;top:-2px;border-width:3px 0 0 3px;border-radius:8px 0 0 0; }}
        .aa-face-ring::after {{ right:-2px;bottom:-2px;border-width:0 3px 3px 0;border-radius:0 0 8px 0; }}
        .aa-face-dot {{ position:absolute;width:8px;height:8px;border-radius:50%;background:var(--aa-lime);left:50%;top:50%;transform:translate(-50%,-50%);box-shadow:0 0 0 8px rgba(186,255,41,.08);animation:aa-live-dot 1.8s ease-out infinite; }}
        .aa-recognized-badge {{ position:absolute;left:50%;bottom:15px;transform:translateX(-50%);padding:6px 11px;border-radius:999px;background:var(--aa-lime);color:var(--aa-navy);font-size:.67rem;font-weight:950;box-shadow:0 8px 20px rgba(186,255,41,.16);animation:aa-badge 2.4s ease-in-out infinite; }}

        /* Auth card typography and action hierarchy */
        .st-key-teacher-auth-card h1,
        .st-key-student-auth-card h1,
        .st-key-teacher-auth-card h2,
        .st-key-student-auth-card h2,
        .st-key-teacher-auth-card h3,
        .st-key-student-auth-card h3 {{ color:var(--aa-navy) !important; }}
        .st-key-teacher-auth-card .stButton > button,
        .st-key-student-auth-card .stButton > button {{ width:100% !important; }}
        .st-key-teacher-auth-card .stButton > button[kind="secondary"],
        .st-key-student-auth-card .stButton > button[kind="secondary"] {{ background:transparent !important; }}
        .st-key-teacher-auth-card .stButton > button[kind="secondary"]:hover,
        .st-key-student-auth-card .stButton > button[kind="secondary"]:hover {{ background:rgba(194,231,218,.36) !important; }}

        /* Live AI recognition surfaces used on dashboards */
        .teacher-camera-preview {{ border-color:rgba(194,231,218,.52) !important; box-shadow:inset 0 0 55px rgba(0,0,0,.32),0 0 0 1px rgba(186,255,41,.06) !important; }}
        .teacher-camera-preview::before {{ background:linear-gradient(90deg,transparent,var(--aa-lime),transparent) !important; box-shadow:0 0 20px rgba(186,255,41,.58) !important; }}
        .teacher-camera-frame {{ border-color:rgba(186,255,41,.88) !important; box-shadow:0 0 0 8px rgba(186,255,41,.06),0 0 34px rgba(186,255,41,.16) !important; }}
        .teacher-recognized {{ background:var(--aa-lime) !important; color:var(--aa-navy) !important; animation:aa-success-pulse 1.8s ease-in-out infinite !important; }}

        /* Home/portal visual hierarchy: dark foundation + clean cards */
        .home-page-polish,
        .ui-hero {{ isolation:isolate !important; }}
        .home-page-polish .ui-hero {{
            background:linear-gradient(135deg,rgba(255,255,255,.97),rgba(241,255,231,.97)) !important;
            border-color:rgba(255,255,255,.82) !important;
            box-shadow:0 26px 64px rgba(26,27,65,.16) !important;
        }}
        .home-page-polish .ui-hero-title {{ color:var(--aa-navy) !important; }}
        .home-page-polish .ui-hero-gradient-text {{ color:var(--aa-blue) !important; background:linear-gradient(90deg,var(--aa-blue),var(--aa-navy),var(--aa-blue)) !important; -webkit-background-clip:text !important; background-clip:text !important; -webkit-text-fill-color:transparent !important; }}
        .home-page-polish .ui-hero-copy-text {{ color:var(--aa-muted) !important; }}
        .home-page-polish .ui-eyebrow,.ui-card-kicker {{ color:var(--aa-blue) !important; }}
        .home-page-polish .ui-eyebrow::before,.ui-card-kicker::before {{ background:var(--aa-lime) !important; box-shadow:0 0 0 5px rgba(186,255,41,.18) !important; }}
        .ui-card-title {{ color:var(--aa-navy) !important; }}
        .ui-card-copy {{ color:var(--aa-muted) !important; }}
        .ui-feature-strip .ui-feature {{ background:rgba(26,27,65,.82) !important; border-color:rgba(194,231,218,.18) !important; color:var(--aa-white) !important; }}
        .ui-feature-strip .ui-feature-title {{ color:var(--aa-white) !important; }}
        .ui-feature-strip .ui-feature-copy {{ color:rgba(255,255,255,.72) !important; }}

        /* Footer is intentionally just the owner's name */
        .app-footer {{ justify-content:center !important; background:transparent !important; border-top:1px solid rgba(98,144,195,.18) !important; padding-top:18px !important; margin-top:28px !important; }}
        .footer-brand,.footer-copy {{ display:none !important; }}
        .footer-credit-only {{ color:var(--aa-navy) !important; font-size:15px !important; font-weight:900 !important; letter-spacing:.04em !important; }}
        .footer-credit-only * {{ color:var(--aa-navy) !important; }}

        /* Responsive auth */
        @media (max-width: 900px) {{
            .st-key-teacher-auth-layout,
            .st-key-student-auth-layout {{ margin-top:0 !important; }}
            .aa-auth-brand {{ min-height:460px !important; }}
            .aa-auth-features {{ grid-template-columns:1fr !important; }}
        }}
        @media (max-width: 700px) {{
            .aa-auth-brand {{ min-height:auto !important; padding:1.35rem !important; }}
            .aa-auth-title {{ font-size:2.3rem !important; }}
            .aa-recognition-visual {{ height:165px !important; }}
            .stButton > button {{ min-height:50px !important; font-size:16px !important; }}
        }}

        /* Motion */
        @keyframes aa-rise {{ from {{ opacity:0;transform:translateY(10px); }} to {{ opacity:1;transform:translateY(0); }} }}
        @keyframes aa-auth-enter {{ from {{ opacity:0;transform:translateY(18px) scale(.992); }} to {{ opacity:1;transform:translateY(0) scale(1); }} }}
        @keyframes aa-card-in {{ from {{ opacity:0;transform:translateY(12px) scale(.988); }} to {{ opacity:1;transform:translateY(0) scale(1); }} }}
        @keyframes aa-bg-flow {{ from {{ background-position:0% 0%,100% 0%,78% 88%,0% 0%; }} to {{ background-position:10% 8%,90% 12%,70% 82%,100% 100%; }} }}
        @keyframes aa-sidebar-flow {{ from {{ background-position:50% 0%; }} to {{ background-position:50% 100%; }} }}
        @keyframes aa-button-sheen {{ 0%,58% {{ left:-42%; }} 78%,100% {{ left:125%; }} }}
        @keyframes aa-toast {{ from {{ opacity:0;transform:translateY(-8px) scale(.98); }} to {{ opacity:1;transform:translateY(0) scale(1); }} }}
        @keyframes aa-float {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-4px); }} }}
        @keyframes aa-orbit {{ 0%,100% {{ transform:translate3d(0,0,0) scale(1);opacity:.75; }} 50% {{ transform:translate3d(-14px,12px,0) scale(1.05);opacity:1; }} }}
        @keyframes aa-blob {{ 0%,100% {{ transform:translate3d(0,0,0) rotate(-4deg) scale(1); }} 50% {{ transform:translate3d(-16px,-8px,0) rotate(4deg) scale(1.05); }} }}
        @keyframes aa-scan {{ 0% {{ opacity:0;transform:translateX(-90px) rotate(16deg); }} 18% {{ opacity:.8; }} 74% {{ opacity:.8; }} 100% {{ opacity:0;transform:translateX(150px) rotate(16deg); }} }}
        @keyframes aa-rec-scan {{ 0% {{ transform:translateY(-70px);opacity:0; }} 15% {{ opacity:1; }} 75% {{ opacity:1; }} 100% {{ transform:translateY(135px);opacity:0; }} }}
        @keyframes aa-face-pulse {{ 0%,100% {{ transform:scale(1);box-shadow:0 0 0 8px rgba(186,255,41,.05),0 0 30px rgba(186,255,41,.10); }} 50% {{ transform:scale(1.03);box-shadow:0 0 0 12px rgba(186,255,41,.03),0 0 40px rgba(186,255,41,.18); }} }}
        @keyframes aa-live-dot {{ 0% {{ box-shadow:0 0 0 0 rgba(186,255,41,.34); }} 70% {{ box-shadow:0 0 0 9px rgba(186,255,41,0); }} 100% {{ box-shadow:0 0 0 0 rgba(186,255,41,0); }} }}
        @keyframes aa-badge {{ 0%,100% {{ transform:translateX(-50%) translateY(0); }} 50% {{ transform:translateX(-50%) translateY(-2px); }} }}
        @keyframes aa-success-pulse {{ 0%,100% {{ box-shadow:0 0 0 4px rgba(186,255,41,.09),0 8px 18px rgba(186,255,41,.14); }} 50% {{ box-shadow:0 0 0 9px rgba(186,255,41,.02),0 12px 26px rgba(186,255,41,.22); }} }}

        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{ animation-duration:.01ms !important; animation-iteration-count:1 !important; transition-duration:.01ms !important; scroll-behavior:auto !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def auth_brand_panel(role="teacher"):
    role = role.lower().strip()
    label = "TEACHER ACCESS" if role == "teacher" else "STUDENT ACCESS"
    title_line = "A Smarter Way to Build"
    accent = "Brighter Futures"
    copy = (
        "AI-powered attendance with face recognition, dependable classroom workflows, "
        "and clear records designed for everyday academic use."
    )
    return f"""
    <div class="aa-auth-brand">
        <div class="aa-auth-logo">
            <div class="aa-auth-logo-mark">AI</div>
            <div class="aa-auth-logo-name">AI Attendance System</div>
        </div>
        <div class="aa-auth-kicker">{html.escape(label)}</div>
        <h1 class="aa-auth-title">{title_line}<br><span class="aa-auth-accent">{accent}</span></h1>
        <div class="aa-auth-copy">{copy}</div>
        <div class="aa-auth-features">
            <div class="aa-auth-feature">
                <div class="aa-auth-feature-icon">◎</div>
                <div class="aa-auth-feature-title">Accurate Recognition</div>
                <div class="aa-auth-feature-copy">Powered by AI</div>
            </div>
            <div class="aa-auth-feature">
                <div class="aa-auth-feature-icon">✓</div>
                <div class="aa-auth-feature-title">Secure &amp; Reliable</div>
                <div class="aa-auth-feature-copy">Your data stays safe</div>
            </div>
            <div class="aa-auth-feature">
                <div class="aa-auth-feature-icon">▥</div>
                <div class="aa-auth-feature-title">Better Insights</div>
                <div class="aa-auth-feature-copy">For a smarter tomorrow</div>
            </div>
        </div>
        <div class="aa-recognition-visual">
            <div class="aa-face-ring"><div class="aa-face-dot"></div></div>
            <div class="aa-recognized-badge">STUDENT RECOGNIZED</div>
        </div>
    </div>
    """
