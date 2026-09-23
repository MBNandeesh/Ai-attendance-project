import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.ui.premium_ui import apply_premium_ui


BLUE = "#6290C3"
MINT = "#C2E7DA"
CREAM = "#F1FFE7"
NAVY = "#1A1B41"
LIME = "#BAFF29"
WHITE = "#FFFFFF"
MUTED = "#B8C5DC"


def home_screen():
    style_background_home()
    style_base_layout()

    st.markdown(
        f"""
        <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
            background:
                radial-gradient(circle at 8% 12%, rgba(98,144,195,.42), transparent 25%),
                radial-gradient(circle at 91% 10%, rgba(194,231,218,.34), transparent 25%),
                radial-gradient(circle at 76% 88%, rgba(186,255,41,.10), transparent 22%),
                linear-gradient(140deg, #10152F 0%, {NAVY} 46%, #294A72 100%) !important;
            background-attachment: fixed !important;
            color: {WHITE} !important;
            animation: home-bg 15s ease-in-out infinite alternate;
        }}

        [data-testid="stMainBlockContainer"], .block-container {{ background: transparent !important; }}

        .stApp::before, .stApp::after {{
            content:"";position:fixed;pointer-events:none;border-radius:50%;filter:blur(10px);z-index:0;
        }}
        .stApp::before {{ width:42vw;height:42vw;left:-15vw;top:18vh;background:radial-gradient(circle,rgba(98,144,195,.46),transparent 70%);animation:blob-left 11s ease-in-out infinite; }}
        .stApp::after {{ width:38vw;height:38vw;right:-13vw;top:10vh;background:radial-gradient(circle,rgba(194,231,218,.38),transparent 70%);animation:blob-right 13s ease-in-out infinite; }}

        .app-topbar {{
            background:linear-gradient(135deg,{NAVY} 0%,#202759 58%,{BLUE} 155%) !important;
            border:1px solid rgba(255,255,255,.13) !important;
            box-shadow:0 18px 42px rgba(0,0,0,.26) !important;
            animation:rise .65s ease-out both, topbar-flow 9s ease-in-out infinite alternate !important;
        }}
        .app-topbar, .app-topbar * {{ color:{WHITE} !important; }}
        .app-topbar .brand-tagline,.app-topbar .topbar-status,.app-topbar .topbar-status-soft {{ display:none !important; }}
        .app-topbar .brand-mark {{ background:{WHITE} !important;color:{NAVY} !important;animation:float 4s ease-in-out infinite; }}
        .app-topbar .brand-name {{ font-size:1.18rem !important;font-weight:900 !important; }}

        .home-page-polish {{ position:relative;z-index:2; }}
        .home-page-polish .ui-hero {{
            position:relative;overflow:hidden;isolation:isolate;
            background:
                radial-gradient(circle at 92% 18%,rgba(194,231,218,.40),transparent 25%),
                radial-gradient(circle at 5% 95%,rgba(98,144,195,.36),transparent 28%),
                linear-gradient(132deg,#121737 0%,{NAVY} 48%,#315B89 140%) !important;
            border:1px solid rgba(255,255,255,.14) !important;
            box-shadow:0 28px 70px rgba(0,0,0,.30) !important;
            animation:rise .72s ease-out both,hero-breathe 6s ease-in-out infinite;
        }}
        .home-page-polish .ui-hero::before {{
            content:"";position:absolute;width:390px;height:390px;right:-120px;top:-190px;border-radius:50%;
            background:radial-gradient(circle,rgba(194,231,218,.56),rgba(98,144,195,.20) 46%,transparent 72%);
            animation:orb 8s ease-in-out infinite;z-index:-1;
        }}
        .home-page-polish .ui-hero::after {{
            content:"";position:absolute;width:3px;height:115%;right:42%;top:-8%;
            background:linear-gradient(to bottom,transparent,rgba(194,231,218,.72),rgba(98,144,195,.12),transparent);
            box-shadow:0 0 20px rgba(194,231,218,.22);transform:rotate(18deg);animation:scan 5.5s ease-in-out infinite;
        }}
        .home-page-polish .ui-eyebrow {{ color:{MINT} !important;font-weight:900 !important;letter-spacing:.13em !important; }}
        .home-page-polish .ui-eyebrow::before {{ background:{LIME} !important;box-shadow:0 0 0 5px rgba(186,255,41,.18) !important; }}
        .home-page-polish .ui-hero-title {{ color:{WHITE} !important;animation:title-rise .8s ease-out both; }}
        .home-page-polish .ui-hero-gradient-text {{ color:{LIME} !important;background:none !important;-webkit-text-fill-color:{LIME} !important;animation:lime-glow 3s ease-in-out infinite;filter:none !important; }}
        .home-page-polish .ui-hero-copy-text {{ color:rgba(255,255,255,.78) !important;font-size:1.08rem !important;line-height:1.72 !important;animation:title-rise 1s ease-out .08s both; }}
        .home-portal-signal {{ display:inline-flex;align-items:center;gap:.5rem;margin-top:.75rem;padding:.44rem .74rem;border:1px solid rgba(194,231,218,.26);border-radius:999px;background:rgba(255,255,255,.08);color:{WHITE} !important;font-weight:850;animation:signal-float 2.8s ease-in-out infinite; }}
        .home-portal-signal-dot {{ width:8px;height:8px;border-radius:50%;background:{LIME};animation:pulse-ring 1.9s ease-out infinite; }}

        .stApp [data-testid="stVerticalBlockBorderWrapper"] {{
            background:rgba(255,255,255,.97) !important;
            border:1px solid rgba(194,231,218,.55) !important;
            border-radius:22px !important;
            box-shadow:0 18px 45px rgba(0,0,0,.17) !important;
            animation:rise .75s ease-out both !important;
            transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease !important;
        }}
        .stApp [data-testid="stVerticalBlockBorderWrapper"]:hover {{ transform:translateY(-7px) !important;border-color:rgba(186,255,41,.58) !important;box-shadow:0 27px 52px rgba(0,0,0,.23) !important; }}
        .ui-card-kicker {{ color:{BLUE} !important;font-weight:900 !important;letter-spacing:.13em !important; }}
        .ui-card-kicker::before {{ background:{LIME} !important;box-shadow:0 0 0 5px rgba(186,255,41,.18) !important; }}
        .ui-card-title {{ color:{NAVY} !important;font-size:1.32rem !important;font-weight:900 !important; }}
        .ui-card-copy {{ color:#607089 !important;font-size:1rem !important;line-height:1.65 !important; }}

        .stButton > button[kind="primary"] {{
            min-height:56px !important;border:0 !important;border-radius:15px !important;
            background:linear-gradient(100deg,{BLUE} 0%,#6FA2D0 45%,{LIME} 125%) !important;
            color:{NAVY} !important;font-size:17px !important;font-weight:900 !important;
            box-shadow:0 13px 30px rgba(98,144,195,.32) !important;position:relative !important;overflow:hidden !important;
            transition:transform .18s ease,box-shadow .18s ease,filter .18s ease !important;
        }}
        .stButton > button[kind="primary"]::after {{ content:"";position:absolute;inset:0 auto 0 -48%;width:30%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.34),transparent);transform:skewX(-18deg);animation:button-sheen 3.8s ease-in-out infinite;pointer-events:none; }}
        .stButton > button[kind="primary"]:hover {{ transform:translateY(-3px) scale(1.012) !important;box-shadow:0 20px 40px rgba(98,144,195,.42),0 0 0 2px rgba(186,255,41,.10) !important;filter:saturate(1.06) !important; }}
        .stButton > button[kind="primary"]:active {{ transform:translateY(-1px) scale(.995) !important; }}

        .ui-feature-strip {{ display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px !important;margin-top:18px !important; }}
        .ui-feature {{ min-height:118px;padding:20px;border-radius:19px;background:linear-gradient(145deg,rgba(26,27,65,.94),rgba(47,82,121,.90));border:1px solid rgba(194,231,218,.24);box-shadow:0 16px 34px rgba(0,0,0,.18);transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease;animation:feature-rise .65s ease-out both; }}
        .ui-feature:hover {{ transform:translateY(-5px);border-color:rgba(186,255,41,.55);box-shadow:0 23px 42px rgba(0,0,0,.25); }}
        .ui-feature-title {{ color:{WHITE} !important;font-size:1.08rem !important;font-weight:900 !important; }}
        .ui-feature-copy {{ color:rgba(255,255,255,.75) !important;font-size:.94rem !important;line-height:1.55 !important; }}
        .ui-quote {{ display:none !important; }}
        .app-footer {{ color:{WHITE} !important;border-top:1px solid rgba(194,231,218,.16) !important;background:transparent !important; }}
        .footer-credit-only,.footer-credit-only * {{ color:{WHITE} !important;font-weight:900 !important; }}

        @keyframes home-bg {{0%,100%{{background-position:0% 0%,100% 0%,70% 90%;}}50%{{background-position:12% 8%,88% 14%,64% 82%;}}}}
        @keyframes blob-left {{0%,100%{{transform:translate3d(0,0,0) rotate(-4deg) scale(1);}}50%{{transform:translate3d(3vw,4vh,0) rotate(4deg) scale(1.07);}}}}
        @keyframes blob-right {{0%,100%{{transform:translate3d(0,0,0) rotate(3deg) scale(1);}}50%{{transform:translate3d(-3vw,4vh,0) rotate(-4deg) scale(1.08);}}}}
        @keyframes rise {{from{{opacity:0;transform:translateY(16px);}}to{{opacity:1;transform:translateY(0);}}}}
        @keyframes title-rise {{from{{opacity:0;transform:translateY(12px);}}to{{opacity:1;transform:translateY(0);}}}}
        @keyframes orb {{0%,100%{{transform:translate3d(0,0,0) scale(1);opacity:.80;}}50%{{transform:translate3d(-18px,16px,0) scale(1.08);opacity:1;}}}}
        @keyframes scan {{0%{{opacity:0;transform:translate3d(-45px,0,0) rotate(18deg);}}18%{{opacity:.95;}}72%{{opacity:.95;}}100%{{opacity:0;transform:translate3d(160px,0,0) rotate(18deg);}}}}
        @keyframes topbar-flow {{from{{background-position:0% 50%;}}to{{background-position:100% 50%;}}}}
        @keyframes hero-breathe {{0%,100%{{box-shadow:0 28px 70px rgba(0,0,0,.28);}}50%{{box-shadow:0 32px 82px rgba(98,144,195,.25);}}}}
        @keyframes float {{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-4px);}}}}
        @keyframes lime-glow {{0%,100%{{filter:brightness(1);}}50%{{filter:brightness(1.15);}}}}
        @keyframes signal-float {{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-2px);}}}}
        @keyframes pulse-ring {{0%{{box-shadow:0 0 0 0 rgba(186,255,41,.42);}}72%{{box-shadow:0 0 0 8px rgba(186,255,41,0);}}100%{{box-shadow:0 0 0 0 rgba(186,255,41,0);}}}}
        @keyframes button-sheen {{0%,58%{{left:-48%;}}78%,100%{{left:125%;}}}}
        @keyframes feature-rise {{from{{opacity:0;transform:translateY(8px);}}to{{opacity:1;transform:translateY(0);}}}}
        @media(max-width:900px){{.ui-feature-strip{{grid-template-columns:1fr !important;}}.home-page-polish .ui-hero-title{{font-size:2.2rem !important;}}}}
        @media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none !important;}}}}
        </style>
        """,
        unsafe_allow_html=True,
    )

    header_home()

    st.markdown(
        """
        <div class="home-page-polish">
            <section class="ui-hero">
                <div class="ui-hero-copy">
                    <div class="ui-eyebrow">AI ATTENDANCE SYSTEM</div>
                    <h1 class="ui-hero-title">Smarter Attendance for a <span class="ui-hero-gradient-text">Brighter Tomorrow</span></h1>
                    <p class="ui-hero-copy-text">Face recognition, optional voice attendance, subject management, and clear records — built for everyday classrooms.</p>
                    <div class="home-portal-signal"><span class="home-portal-signal-dot"></span>AI attendance ready</div>
                </div>
            </section>
        </div>
        <div class="home-button-emphasis"></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="ui-card-kicker">STUDENT</div>
                <div class="ui-card-title">Student Portal</div>
                <div class="ui-card-copy">Sign in with Face ID, view subjects, and keep track of attendance.</div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Continue as Student", type="primary", width="stretch", icon=":material/arrow_forward:", key="student_portal"):
                st.session_state["login_type"] = "student"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown(
                """
                <div class="ui-card-kicker">TEACHER</div>
                <div class="ui-card-title">Teacher Portal</div>
                <div class="ui-card-copy">Create subjects, run AI attendance, use voice attendance, and review records.</div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Continue as Teacher", type="primary", width="stretch", icon=":material/arrow_forward:", key="teacher_portal"):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    st.markdown(
        """
        <div class="ui-feature-strip">
            <div class="ui-feature"><div class="ui-feature-title">Accurate</div><div class="ui-feature-copy">AI-powered recognition for classroom attendance.</div></div>
            <div class="ui-feature"><div class="ui-feature-title">Reliable</div><div class="ui-feature-copy">Fast workflows for real classroom use.</div></div>
            <div class="ui-feature"><div class="ui-feature-title">Clear records</div><div class="ui-feature-copy">Subjects, sessions, and attendance stay organized.</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    footer_home()
    apply_premium_ui()
