import html
import time
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.config import supabase
from src.database.db import get_attendance_for_teacher, get_teacher_subjects
from src.pipelines.face_pipeline import predict_attendance
import src.screens.teacher_screen as teacher_module


BLUE = "#6290C3"
MINT = "#C2E7DA"
PALE = "#F1FFE7"
NAVY = "#1A1B41"
LIME = "#BAFF29"
WHITE = "#FFFFFF"
SOFT_GRAY = "#E8EDF2"
RED = "#EF4444"
TEXT = "#1A1B41"
MUTED = "#64748B"


def _safe(value, fallback=""):
    return html.escape(str(value if value not in (None, "") else fallback))


def _parse_ts(value):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def _today_records(records):
    today = datetime.now(timezone.utc).date()
    return [
        r
        for r in (records or [])
        if (_parse_ts(r.get("timestamp")) or datetime.min.replace(tzinfo=timezone.utc)).date() == today
    ]


def _stats(records, total_students):
    today_records = _today_records(records)
    present = sum(1 for r in today_records if bool(r.get("is_present", False)))
    absent = min(max(total_students - present, 0), total_students)
    yet = max(total_students - present - absent, 0)
    rate = int(round((present / total_students) * 100)) if total_students else 0
    return present, absent, yet, rate


def _animated_number(value, session_key):
    value = int(value or 0)
    token = f"teacher_stat_animated_{session_key}"
    if st.session_state.get(token):
        return str(value)

    slot = st.empty()
    steps = min(max(value, 1), 18)
    for step in range(steps + 1):
        current = round(value * step / steps)
        slot.markdown(f"<div class='teacher-stat-value'>{current}</div>", unsafe_allow_html=True)
        time.sleep(0.018)
    st.session_state[token] = True
    return str(value)


def _inject_styles():
    st.markdown(
        f"""
        <style>
            :root {{
                --t-blue: {BLUE};
                --t-mint: {MINT};
                --t-pale: {PALE};
                --t-navy: {NAVY};
                --t-lime: {LIME};
                --t-white: {WHITE};
                --t-gray: {SOFT_GRAY};
                --t-red: {RED};
            }}

            .stApp {{
                background:
                    radial-gradient(circle at 85% 10%, rgba(194,231,218,.72), transparent 27%),
                    radial-gradient(circle at 7% 88%, rgba(98,144,195,.20), transparent 25%),
                    linear-gradient(135deg, #F9FCFD 0%, #EFF8F5 48%, #F1FFE7 100%) !important;
                background-attachment: fixed !important;
            }}

            section[data-testid="stSidebar"] {{
                background: {NAVY} !important;
                border-right: 1px solid rgba(255,255,255,.06) !important;
            }}
            section[data-testid="stSidebar"] > div {{
                background: linear-gradient(180deg, #20234E 0%, {NAVY} 58%, #14152F 100%) !important;
            }}
            section[data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}
            section[data-testid="stSidebar"] button {{
                border: 0 !important;
                border-radius: 14px !important;
                background: transparent !important;
                box-shadow: none !important;
                transition: background .24s ease, transform .24s ease !important;
            }}
            section[data-testid="stSidebar"] button:hover {{
                background: rgba(255,255,255,.09) !important;
                transform: translateX(2px) !important;
            }}
            section[data-testid="stSidebar"] button[kind="primary"] {{
                background: linear-gradient(135deg, {BLUE}, #79A7D5) !important;
                box-shadow: 0 10px 25px rgba(98,144,195,.22) !important;
            }}

            .teacher-page {{
                width: min(100%, 1500px);
                margin: 0 auto;
                animation: teacher-page-in .28s ease-out both;
            }}

            .teacher-topbar {{
                display:flex;
                align-items:center;
                gap:16px;
                padding:12px 16px;
                margin:0 0 18px;
                border:1px solid rgba(26,27,65,.08);
                border-radius:18px;
                background:rgba(255,255,255,.84);
                backdrop-filter:blur(18px);
                box-shadow:0 12px 35px rgba(26,27,65,.07);
            }}
            .teacher-search {{
                flex:1;
                min-height:46px;
                display:flex;
                align-items:center;
                gap:10px;
                padding:0 14px;
                border-radius:13px;
                border:1px solid {SOFT_GRAY};
                background:#F9FBFC;
                color:#89A0B5;
                font-size:14px;
                font-weight:700;
            }}
            .teacher-profile {{ display:flex; align-items:center; gap:10px; color:{NAVY}; }}
            .teacher-avatar {{
                width:44px;
                height:44px;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
                background:linear-gradient(135deg,{BLUE},#90B7DB);
                color:white;
                font-weight:900;
                box-shadow:0 8px 20px rgba(98,144,195,.24);
            }}
            .teacher-profile-name {{ font-size:14px; font-weight:900; }}
            .teacher-profile-role {{ margin-top:2px; color:{MUTED}; font-size:11px; font-weight:700; }}
            .teacher-bell {{
                width:38px;
                height:38px;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
                background:{WHITE};
                border:1px solid {SOFT_GRAY};
                color:{NAVY};
                position:relative;
            }}
            .teacher-bell::after {{
                content:"";
                width:7px;
                height:7px;
                border-radius:50%;
                position:absolute;
                top:8px;
                right:9px;
                background:{LIME};
                box-shadow:0 0 0 4px rgba(186,255,41,.18);
                animation:teacher-dot 1.8s ease-in-out infinite;
            }}

            .teacher-greeting {{
                display:flex;
                align-items:flex-end;
                justify-content:space-between;
                gap:20px;
                margin:4px 6px 18px;
                animation:teacher-rise .45s ease-out both;
            }}
            .teacher-greeting h1 {{
                margin:0;
                color:{NAVY};
                font-size:clamp(30px,3.3vw,46px);
                letter-spacing:-.04em;
                line-height:1.03;
                font-weight:950;
            }}
            .teacher-greeting p {{
                margin:7px 0 0;
                color:#617895;
                font-size:16px;
                font-weight:650;
            }}
            .teacher-date-card {{
                display:flex;
                align-items:center;
                gap:10px;
                padding:11px 14px;
                border:1px solid rgba(98,144,195,.18);
                background:rgba(255,255,255,.70);
                border-radius:14px;
                color:{NAVY};
                min-width:210px;
                justify-content:flex-end;
            }}
            .teacher-date-icon {{
                width:38px;
                height:38px;
                display:flex;
                align-items:center;
                justify-content:center;
                border-radius:12px;
                background:{MINT};
                font-size:21px;
            }}
            .teacher-date-main {{ font-weight:900; font-size:13px; }}
            .teacher-date-sub {{ margin-top:2px; color:{MUTED}; font-size:10px; font-weight:700; }}

            .teacher-stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:18px; }}
            .teacher-stat-card {{
                min-height:118px;
                padding:18px;
                border-radius:20px;
                border:1px solid rgba(26,27,65,.07);
                box-shadow:0 12px 30px rgba(26,27,65,.06);
                overflow:hidden;
                position:relative;
                transition:transform .22s ease, box-shadow .22s ease;
                animation:teacher-rise .5s ease-out both;
            }}
            .teacher-stat-card:nth-child(1) {{ background:linear-gradient(135deg,{BLUE},#7EA9D2); color:white; }}
            .teacher-stat-card:nth-child(2) {{ background:linear-gradient(135deg,#CFEFE4,{MINT}); }}
            .teacher-stat-card:nth-child(3) {{ background:linear-gradient(135deg,#F8FFE9,{PALE}); }}
            .teacher-stat-card:nth-child(4) {{ background:linear-gradient(135deg,{NAVY},#2D3165); color:white; }}
            .teacher-stat-card:hover {{ transform:translateY(-4px); box-shadow:0 18px 36px rgba(26,27,65,.12); }}
            .teacher-stat-label {{ font-size:12px; font-weight:850; opacity:.82; }}
            .teacher-stat-value {{ margin-top:7px; font-size:34px; line-height:1; font-weight:950; letter-spacing:-.04em; }}
            .teacher-stat-note {{ margin-top:8px; font-size:11px; font-weight:800; opacity:.82; }}
            .teacher-stat-icon {{
                position:absolute;
                right:16px;
                top:16px;
                width:42px;
                height:42px;
                border-radius:13px;
                display:flex;
                align-items:center;
                justify-content:center;
                background:rgba(255,255,255,.22);
                backdrop-filter:blur(8px);
            }}
            .teacher-stat-ring {{
                --pct: 0%;
                width:54px;
                height:54px;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
                background:conic-gradient({LIME} var(--pct), rgba(255,255,255,.28) 0);
                animation:teacher-ring 1s ease-out both;
                box-shadow:0 0 0 5px rgba(255,255,255,.08);
            }}
            .teacher-stat-ring span {{
                width:42px;
                height:42px;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
                background:rgba(26,27,65,.80);
                color:white;
                font-size:11px;
                font-weight:950;
            }}

            .teacher-main-grid {{ display:grid; grid-template-columns:1.1fr .9fr; gap:18px; align-items:stretch; }}
            .teacher-card {{
                background:rgba(255,255,255,.92);
                border:1px solid rgba(26,27,65,.08);
                border-radius:22px;
                box-shadow:0 16px 38px rgba(26,27,65,.06);
                overflow:hidden;
                animation:teacher-rise .55s ease-out both;
            }}
            .teacher-card-head {{
                display:flex;
                align-items:center;
                justify-content:space-between;
                gap:12px;
                padding:18px 20px 14px;
            }}
            .teacher-card-title {{ display:flex; align-items:center; gap:10px; color:{NAVY}; font-size:18px; font-weight:950; }}
            .teacher-card-icon {{
                width:34px;
                height:34px;
                border-radius:10px;
                display:flex;
                align-items:center;
                justify-content:center;
                background:{MINT};
                color:{NAVY};
            }}
            .teacher-live {{ display:flex; align-items:center; gap:8px; color:#203249; font-size:11px; font-weight:900; }}
            .teacher-live-dot {{
                width:9px;
                height:9px;
                border-radius:50%;
                background:{LIME};
                box-shadow:0 0 0 5px rgba(186,255,41,.16);
                animation:teacher-dot 1.6s ease-in-out infinite;
            }}
            .teacher-camera-wrap {{ padding:0 18px 18px; }}
            .teacher-camera-preview {{
                min-height:320px;
                border-radius:18px;
                background:linear-gradient(160deg,#15243D,#0C1527 62%,#111E34);
                border:2px solid rgba(194,231,218,.45);
                position:relative;
                overflow:hidden;
                display:flex;
                align-items:center;
                justify-content:center;
                color:white;
                box-shadow:inset 0 0 55px rgba(0,0,0,.32);
            }}
            .teacher-camera-preview::before {{
                content:"";
                position:absolute;
                left:8%;
                right:8%;
                top:0;
                height:2px;
                background:linear-gradient(90deg, transparent, {LIME}, transparent);
                box-shadow:0 0 18px rgba(186,255,41,.58);
                animation:teacher-scan 2.5s linear infinite;
            }}
            .teacher-camera-frame {{
                width:180px;
                height:180px;
                border-radius:28px;
                border:2px solid rgba(186,255,41,.78);
                box-shadow:0 0 0 8px rgba(186,255,41,.06), 0 0 36px rgba(186,255,41,.13);
                position:relative;
                animation:teacher-frame-pulse 2.3s ease-in-out infinite;
            }}
            .teacher-camera-frame::before, .teacher-camera-frame::after {{
                content:"";
                position:absolute;
                width:30px;
                height:30px;
                border-color:{LIME};
                border-style:solid;
            }}
            .teacher-camera-frame::before {{ top:-2px; left:-2px; border-width:3px 0 0 3px; border-radius:8px 0 0 0; }}
            .teacher-camera-frame::after {{ right:-2px; bottom:-2px; border-width:0 3px 3px 0; border-radius:0 0 8px 0; }}
            .teacher-camera-center {{ text-align:center; position:absolute; inset:0; display:flex; flex-direction:column; justify-content:center; align-items:center; gap:8px; }}
            .teacher-camera-glyph {{ font-size:48px; opacity:.86; }}
            .teacher-camera-title {{ font-size:18px; font-weight:950; }}
            .teacher-camera-sub {{ color:#AFC0D6; font-size:11px; font-weight:650; }}
            .teacher-recognized {{
                position:absolute;
                left:50%;
                transform:translateX(-50%);
                bottom:24px;
                padding:6px 10px;
                border-radius:999px;
                background:{LIME};
                color:{NAVY};
                font-size:10px;
                font-weight:950;
                box-shadow:0 0 0 5px rgba(186,255,41,.10), 0 8px 20px rgba(186,255,41,.17);
                animation:teacher-success 2s ease-in-out infinite;
            }}
            .teacher-actions {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:12px; }}

            .teacher-table-shell {{ padding:0 18px 16px; }}
            .teacher-table {{ width:100%; border-collapse:separate; border-spacing:0; overflow:hidden; border:1px solid {SOFT_GRAY}; border-radius:15px; }}
            .teacher-table th {{ background:#F4F8FA; color:#49647D; font-size:11px; font-weight:900; text-align:left; padding:12px 13px; }}
            .teacher-table td {{ color:#304D68; font-size:12px; font-weight:700; padding:12px 13px; border-top:1px solid #EEF2F5; }}
            .teacher-table tbody tr {{ animation:teacher-row-in .34s ease-out both; transition:background .2s ease; }}
            .teacher-table tbody tr:hover {{ background:#FAFCFD; }}
            .teacher-table tbody tr:nth-child(2) {{ animation-delay:.04s; }}
            .teacher-table tbody tr:nth-child(3) {{ animation-delay:.08s; }}
            .teacher-table tbody tr:nth-child(4) {{ animation-delay:.12s; }}
            .teacher-table tbody tr:nth-child(5) {{ animation-delay:.16s; }}
            .teacher-table tbody tr:nth-child(6) {{ animation-delay:.20s; }}
            .teacher-status {{ padding:5px 9px; border-radius:8px; display:inline-flex; font-size:10px; font-weight:950; }}
            .teacher-status.present {{ background:#DCFCE7; color:#16803A; }}
            .teacher-status.absent {{ background:#FEE2E2; color:{RED}; }}
            .teacher-view-all {{ color:{BLUE}; font-size:12px; font-weight:900; }}

            .teacher-footer-banner {{
                margin-top:18px;
                padding:18px 24px;
                border-radius:20px;
                background:linear-gradient(100deg,{BLUE} 0%, #7FA9D0 50%, {MINT} 100%);
                color:{NAVY};
                position:relative;
                overflow:hidden;
                box-shadow:0 18px 38px rgba(98,144,195,.15);
                animation:teacher-rise .65s ease-out both;
            }}
            .teacher-footer-banner::after {{
                content:"";
                position:absolute;
                width:320px;
                height:180px;
                right:-100px;
                top:-80px;
                border-radius:50%;
                background:rgba(255,255,255,.23);
                filter:blur(18px);
                animation:teacher-float 7s ease-in-out infinite;
            }}
            .teacher-footer-title {{ font-size:21px; font-weight:950; }}
            .teacher-footer-copy {{ margin-top:3px; color:#F7FFFB; font-size:13px; font-weight:700; }}
            .teacher-footer-mark {{ position:absolute; right:24px; bottom:12px; font-size:17px; font-weight:900; font-style:italic; color:{NAVY}; }}

            .teacher-section-tabs {{
                display:grid;
                grid-template-columns:repeat(3,1fr);
                gap:10px;
                margin-bottom:18px;
                padding:7px;
                background:rgba(255,255,255,.72);
                border:1px solid rgba(26,27,65,.07);
                border-radius:16px;
                animation:teacher-rise .35s ease-out both;
            }}

            /* Streamlit controls */
            .stButton > button {{
                border-radius:12px !important;
                min-height:44px !important;
                font-weight:900 !important;
                font-size:14px !important;
                transition:transform .22s ease, box-shadow .22s ease, background .22s ease !important;
            }}
            .stButton > button:hover {{ transform:translateY(-2px) !important; }}
            .stButton > button[kind="primary"] {{
                background:linear-gradient(135deg,{NAVY},#2C2F60) !important;
                color:white !important;
                border:0 !important;
                box-shadow:0 10px 24px rgba(26,27,65,.18) !important;
            }}
            .stButton > button[kind="secondary"] {{
                background:{WHITE} !important;
                color:{NAVY} !important;
                border:1px solid {SOFT_GRAY} !important;
                box-shadow:0 8px 20px rgba(26,27,65,.05) !important;
            }}
            .stButton > button[kind="tertiary"] {{
                background:transparent !important;
                color:{NAVY} !important;
                border:1px solid rgba(26,27,65,.10) !important;
            }}
            [data-testid="stTextInput"] input,
            [data-testid="stSelectbox"] div[data-baseweb="select"],
            [data-testid="stTextArea"] textarea {{
                border-radius:12px !important;
                border:1px solid {SOFT_GRAY} !important;
                background:#FFFFFF !important;
            }}

            @keyframes teacher-page-in {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:translateY(0); }} }}
            @keyframes teacher-rise {{ from {{ opacity:0; transform:translateY(16px); }} to {{ opacity:1; transform:translateY(0); }} }}
            @keyframes teacher-row-in {{ from {{ opacity:0; transform:translateY(7px); }} to {{ opacity:1; transform:translateY(0); }} }}
            @keyframes teacher-scan {{ 0% {{ transform:translateY(-155px); opacity:0; }} 20% {{ opacity:1; }} 75% {{ opacity:1; }} 100% {{ transform:translateY(325px); opacity:0; }} }}
            @keyframes teacher-frame-pulse {{ 0%,100% {{ box-shadow:0 0 0 8px rgba(186,255,41,.06),0 0 24px rgba(186,255,41,.07); }} 50% {{ box-shadow:0 0 0 12px rgba(186,255,41,.08),0 0 42px rgba(186,255,41,.16); }} }}
            @keyframes teacher-success {{ 0%,100% {{ transform:translateX(-50%) scale(1); }} 50% {{ transform:translateX(-50%) scale(1.04); }} }}
            @keyframes teacher-dot {{ 0%,100% {{ transform:scale(1); opacity:.75; }} 50% {{ transform:scale(1.25); opacity:1; }} }}
            @keyframes teacher-ring {{ from {{ opacity:.25; transform:rotate(-25deg) scale(.88); }} to {{ opacity:1; transform:rotate(0) scale(1); }} }}
            @keyframes teacher-float {{ 0%,100% {{ transform:translate3d(0,0,0) scale(1); }} 50% {{ transform:translate3d(-30px,16px,0) scale(1.07); }} }}

            @media (max-width: 1080px) {{
                .teacher-stats {{ grid-template-columns:1fr 1fr; }}
                .teacher-main-grid {{ grid-template-columns:1fr; }}
            }}
            @media (max-width: 760px) {{
                .teacher-topbar {{ flex-wrap:wrap; }}
                .teacher-search {{ width:100%; flex-basis:100%; }}
                .teacher-greeting {{ flex-direction:column; align-items:flex-start; }}
                .teacher-date-card {{ width:100%; justify-content:flex-start; }}
                .teacher-stats {{ grid-template-columns:1fr; }}
                .teacher-section-tabs {{ grid-template-columns:1fr; }}
                .teacher-actions {{ grid-template-columns:1fr; }}
                .teacher-camera-preview {{ min-height:250px; }}
                .teacher-footer-mark {{ display:none; }}
            }}
            @media (prefers-reduced-motion: reduce) {{
                *, *::before, *::after {{ animation-duration:.01ms !important; transition-duration:.01ms !important; }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _sidebar(teacher_data, active):
    with st.sidebar:
        name = _safe(teacher_data.get("name", "Teacher"), "Teacher")
        initial = html.escape(name[:1].upper() or "T")
        st.markdown(
            f"""
            <div style="padding:16px 8px 22px;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#7BA8D4,#C2E7DA);color:#1A1B41;display:flex;align-items:center;justify-content:center;font-weight:950;font-size:16px;box-shadow:0 10px 22px rgba(0,0,0,.16);">AI</div>
                    <div>
                        <div style="font-size:17px;font-weight:950;line-height:1.05;">AI Attendance</div>
                        <div style="font-size:10px;opacity:.65;margin-top:3px;font-weight:700;">Recognize · Record · Empower</div>
                    </div>
                </div>
            </div>
            <div style="padding:0 8px 8px;font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.55;font-weight:900;">Workspace</div>
            """,
            unsafe_allow_html=True,
        )

        items = [
            ("take_attendance", "Dashboard", ":material/dashboard:"),
            ("take_attendance", "Take Attendance", ":material/photo_camera:"),
            ("manage_subjects", "Manage Subjects", ":material/groups:"),
            ("attendance_records", "Attendance Records", ":material/description:"),
        ]
        selected = None
        for key, label, icon in items:
            kind = "primary" if active == key and label == "Dashboard" else "tertiary"
            if st.button(
                label,
                key=f"teacher_nav_{label.replace(' ', '_').lower()}",
                type=kind,
                width="stretch",
                icon=icon,
            ):
                selected = key

        st.markdown('<div style="height:15rem"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:10px;padding:12px 10px;border:1px solid rgba(255,255,255,.10);background:rgba(255,255,255,.06);border-radius:14px;">
                <div style="width:36px;height:36px;border-radius:50%;background:#C2E7DA;color:#1A1B41;display:flex;align-items:center;justify-content:center;font-weight:950;">{initial}</div>
                <div><div style="font-size:12px;font-weight:900;">{name}</div><div style="font-size:10px;opacity:.6;font-weight:700;">Faculty</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Logout",
            key="teacher_nav_logout",
            type="secondary",
            width="stretch",
            icon=":material/logout:",
        ):
            teacher_module._reset_teacher_workspace()
            st.session_state["login_type"] = None
            st.rerun()

    return selected


def _recent_rows(records):
    rows = []
    for record in (records or [])[:6]:
        student = record.get("students") or {}
        subject = record.get("subjects") or {}
        ts = _parse_ts(record.get("timestamp"))
        rows.append(
            {
                "student": student.get("name", "Unknown"),
                "subject": subject.get("name", "Unknown"),
                "status": bool(record.get("is_present", False)),
                "time": ts.strftime("%I:%M %p") if ts else "-",
            }
        )
    return rows


def _render_recent_table(records):
    rows = _recent_rows(records)
    if not rows:
        st.markdown(
            "<div style='padding:42px 18px;color:#64748B;text-align:center;font-size:13px;font-weight:700;'>No attendance records yet. Start a recognition session to see results here.</div>",
            unsafe_allow_html=True,
        )
        return

    body = []
    for idx, row in enumerate(rows, 1):
        status = "Present" if row["status"] else "Absent"
        cls = "present" if row["status"] else "absent"
        body.append(
            f"<tr><td>{idx}</td><td>{_safe(row['student'])}</td><td>{_safe(row['subject'])}</td><td><span class='teacher-status {cls}'>{status}</span></td><td>{_safe(row['time'])}</td></tr>"
        )

    st.markdown(
        f"""
        <div class="teacher-table-shell">
            <table class="teacher-table">
                <thead><tr><th>#</th><th>Name</th><th>Subject</th><th>Status</th><th>Time</th></tr></thead>
                <tbody>{''.join(body)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_dashboard(teacher_data, subjects, records):
    teacher_name = _safe(teacher_data.get("name", "Teacher"), "Teacher")
    today = datetime.now().astimezone()
    total_students = sum(int(s.get("total_students", 0) or 0) for s in subjects)
    present, absent, yet, rate = _stats(records, total_students)
    initials = html.escape((teacher_name[:1] or "T").upper())
    weekday = today.strftime("%A")
    date_text = today.strftime("%d %b %Y")

    # Keep the dashboard count-up as a one-time entry animation per teacher session.
    total_display = _animated_number(total_students, "total")
    present_display = _animated_number(present, "present")
    absent_display = _animated_number(absent, "absent")
    yet_display = _animated_number(yet, "yet")

    st.markdown(
        f"""
        <div class="teacher-page">
            <div class="teacher-topbar">
                <div class="teacher-search"><span class="material-symbols-rounded">search</span><span>Search students, records...</span></div>
                <div class="teacher-bell"><span class="material-symbols-rounded">notifications_none</span></div>
                <div class="teacher-profile">
                    <div class="teacher-avatar">{initials}</div>
                    <div><div class="teacher-profile-name">{teacher_name}</div><div class="teacher-profile-role">Faculty</div></div>
                </div>
            </div>

            <div class="teacher-greeting">
                <div><h1>Good Morning, {teacher_name}!</h1><p>Here’s your attendance overview for today.</p></div>
                <div class="teacher-date-card"><div class="teacher-date-icon">▣</div><div><div class="teacher-date-main">{weekday}, {date_text}</div><div class="teacher-date-sub">Consistency Builds Better Futures</div></div></div>
            </div>

            <div class="teacher-stats">
                <div class="teacher-stat-card"><div class="teacher-stat-icon">●</div><div class="teacher-stat-label">Total Students</div><div class="teacher-stat-value">{total_display}</div><div class="teacher-stat-note">Across your subjects</div></div>
                <div class="teacher-stat-card"><div class="teacher-stat-icon"><div class="teacher-stat-ring" style="--pct:{rate}%;"><span>{rate}%</span></div></div><div class="teacher-stat-label">Present</div><div class="teacher-stat-value">{present_display}</div><div class="teacher-stat-note">Marked today</div></div>
                <div class="teacher-stat-card"><div class="teacher-stat-icon"><div class="teacher-stat-ring" style="--pct:{10 if absent else 0}%;"><span>{10 if absent else 0}%</span></div></div><div class="teacher-stat-label">Absent</div><div class="teacher-stat-value">{absent_display}</div><div class="teacher-stat-note">Requires attention</div></div>
                <div class="teacher-stat-card"><div class="teacher-stat-icon"><div class="teacher-stat-ring" style="--pct:{round((yet / total_students) * 100) if total_students else 0}%;"><span>{round((yet / total_students) * 100) if total_students else 0}%</span></div></div><div class="teacher-stat-label">Yet to Mark</div><div class="teacher-stat-value">{yet_display}</div><div class="teacher-stat-note">Waiting for recognition</div></div>
            </div>

            <div class="teacher-main-grid">
                <div class="teacher-card">
                    <div class="teacher-card-head"><div class="teacher-card-title"><span class="teacher-card-icon">▣</span>Live Attendance</div><div class="teacher-live"><span class="teacher-live-dot"></span>Real-time Recognition</div></div>
                    <div class="teacher-camera-wrap">
                        <div class="teacher-camera-preview">
                            <div class="teacher-camera-frame"><div class="teacher-camera-center"><div class="teacher-camera-glyph">◉</div><div class="teacher-camera-title">AI Recognition Ready</div><div class="teacher-camera-sub">Camera feed appears when you start attendance</div></div></div>
                            <div class="teacher-recognized">Recognition Engine Ready</div>
                        </div>
                        <div class="teacher-actions">
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button(
            "Start Attendance",
            type="primary",
            width="stretch",
            icon=":material/play_arrow:",
            key="teacher_dashboard_start_attendance",
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()
    with c2:
        if st.button(
            "Upload Image / Video",
            type="secondary",
            width="stretch",
            icon=":material/upload:",
            key="teacher_dashboard_upload_media",
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.session_state.dashboard_open_upload = True
            st.rerun()

    st.markdown(
        """
                        </div>
                    </div>
                </div>
                <div class="teacher-card">
                    <div class="teacher-card-head"><div class="teacher-card-title"><span class="teacher-card-icon">▤</span>Recent Attendance</div><div class="teacher-view-all">View All →</div></div>
        """,
        unsafe_allow_html=True,
    )
    _render_recent_table(records)
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="teacher-footer-banner">
            <div class="teacher-footer-title">AI-Powered Attendance</div>
            <div class="teacher-footer-copy">Save time. Improve accuracy. Focus on what matters.</div>
            <div class="teacher-footer-mark">Same faces. Brighter futures.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _run_face_analysis(selected_subject_id):
    images = st.session_state.get("attendance_images", []) or []
    if not images:
        st.warning("Add at least one photo before running face analysis.")
        return

    with st.spinner("Scanning classroom photos..."):
        all_detected_ids = {}
        for idx, img in enumerate(images):
            img_np = __import__("numpy").array(img.convert("RGB"))
            detected, _, _ = predict_attendance(img_np)
            for sid in detected.keys():
                student_id = int(sid)
                all_detected_ids.setdefault(student_id, []).append(f"Photo {idx + 1}")

        enrolled_res = (
            supabase.table("subject_students")
            .select("*, students(*)")
            .eq("subject_id", selected_subject_id)
            .execute()
        )
        enrolled_students = enrolled_res.data or []
        if not enrolled_students:
            st.warning("No students are enrolled in this course.")
            return

        results = []
        attendance_to_log = []
        timestamp = datetime.now(timezone.utc).isoformat()
        for node in enrolled_students:
            student = node.get("students") if isinstance(node, dict) else None
            if not isinstance(student, dict) or student.get("student_id") is None:
                continue
            student_id = int(student["student_id"])
            sources = all_detected_ids.get(student_id, [])
            present = bool(sources)
            results.append(
                {
                    "Name": student.get("name", "Unknown"),
                    "ID": student_id,
                    "Source": ", ".join(sources) if present else "-",
                    "Status": "Present" if present else "Absent",
                }
            )
            attendance_to_log.append(
                {
                    "student_id": student_id,
                    "subject_id": selected_subject_id,
                    "timestamp": timestamp,
                    "is_present": present,
                }
            )

        if not attendance_to_log:
            st.warning("No valid enrolled students were found.")
            return
        attendance_result_dialog(pd.DataFrame(results), attendance_to_log)


def _render_take_attendance(teacher_id):
    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []
    if "attendance_image_keys" not in st.session_state:
        st.session_state.attendance_image_keys = set()

    subjects = get_teacher_subjects(teacher_id) or []
    if not subjects:
        st.info("Create a subject first, then start an attendance session.")
        return

    st.markdown(
        """
        <div class="teacher-page">
            <div class="teacher-card" style="padding:20px;">
                <div class="teacher-card-head" style="padding:0 0 14px;"><div class="teacher-card-title"><span class="teacher-card-icon">◉</span>Take Attendance</div><div class="teacher-live"><span class="teacher-live-dot"></span>AI Recognition Online</div></div>
        """,
        unsafe_allow_html=True,
    )

    labels = {f"{s.get('name','Unknown')} · {s.get('subject_code','')}": s["subject_id"] for s in subjects}
    selected_label = st.selectbox("Select Subject", list(labels.keys()), key="attendance_subject_selector")
    selected_subject_id = labels[selected_label]

    previous = st.session_state.get("attendance_subject_id")
    if previous != selected_subject_id:
        st.session_state.attendance_subject_id = selected_subject_id
        if previous is not None and st.session_state.attendance_images:
            st.session_state.attendance_images = []
            st.session_state.attendance_image_keys = set()
            st.info("Photos were cleared because you changed the subject.")

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("Add Photos", type="primary", width="stretch", icon=":material/add_a_photo:", key="add_attendance_photos"):
            add_photos_dialog()
    with c2:
        if st.button("Use Voice Attendance", type="secondary", width="stretch", icon=":material/mic:", key="use_voice_attendance"):
            voice_attendance_dialog(selected_subject_id)

    if st.session_state.attendance_images:
        st.markdown("<div style='margin:18px 0 10px;color:#1A1B41;font-size:15px;font-weight:950;'>Added Photos</div>", unsafe_allow_html=True)
        gallery = st.columns(min(4, len(st.session_state.attendance_images)))
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery[idx % len(gallery)]:
                st.image(img, width="stretch", caption=f"Photo {idx + 1}")

    has_photos = bool(st.session_state.attendance_images)
    b1, b2 = st.columns(2, gap="small")
    with b1:
        if st.button("Clear Photos", type="tertiary", width="stretch", icon=":material/delete:", disabled=not has_photos, key="clear_attendance_photos"):
            st.session_state.attendance_images = []
            st.session_state.attendance_image_keys = set()
            st.rerun()
    with b2:
        if st.button("Run Face Analysis", type="primary", width="stretch", icon=":material/face:", disabled=not has_photos, key="run_face_analysis"):
            _run_face_analysis(selected_subject_id)

    st.markdown("</div></div>", unsafe_allow_html=True)


def _render_manage_subjects(teacher_id):
    subjects = get_teacher_subjects(teacher_id) or []
    st.markdown("<div class='teacher-page'><div class='teacher-card' style='padding:20px;'><div class='teacher-card-title'><span class='teacher-card-icon'>◫</span>Manage Subjects</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("Create New Subject", type="primary", width="stretch", icon=":material/add:", key="create_new_subject"):
        create_subject_dialog(teacher_id)

    if not subjects:
        st.info("No subjects found. Create one above.")
    else:
        for subject in subjects:
            st.markdown(
                f"""
                <div style="margin-top:14px;padding:16px;border:1px solid {SOFT_GRAY};border-radius:16px;background:#FBFDFE;animation:teacher-rise .4s ease-out both;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">
                        <div><div style="font-size:17px;font-weight:950;color:{NAVY};">{_safe(subject.get('name','Unknown'))}</div><div style="margin-top:4px;color:{MUTED};font-size:11px;font-weight:750;">{_safe(subject.get('subject_code','-'))} · Section {_safe(subject.get('section','-'))}</div></div>
                        <div style="padding:7px 10px;border-radius:999px;background:{MINT};color:{NAVY};font-size:10px;font-weight:900;">{int(subject.get('total_students',0) or 0)} students</div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px;">
                        <div style="padding:10px;border:1px solid {SOFT_GRAY};border-radius:12px;background:white;"><div style="font-size:10px;color:{MUTED};font-weight:800;">Classes</div><div style="font-size:20px;color:{NAVY};font-weight:950;margin-top:2px;">{int(subject.get('total_classes',0) or 0)}</div></div>
                        <div style="padding:10px;border:1px solid {SOFT_GRAY};border-radius:12px;background:white;"><div style="font-size:10px;color:{MUTED};font-weight:800;">Share</div><div style="font-size:12px;color:{BLUE};font-weight:900;margin-top:7px;">Use button below</div></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Share class link", key=f"share_subject_{subject.get('subject_id')}", type="secondary", width="stretch", icon=":material/share:"):
                share_subject_dialog(subject.get("name", "Subject"), subject.get("subject_code", ""))

    st.markdown("</div></div>", unsafe_allow_html=True)


def _render_records(teacher_id):
    records = get_attendance_for_teacher(teacher_id) or []
    st.markdown("<div class='teacher-page'><div class='teacher-card' style='padding:20px;'><div class='teacher-card-title'><span class='teacher-card-icon'>▤</span>Attendance Records</div><div style='height:14px'></div>", unsafe_allow_html=True)
    if not records:
        st.info("No attendance records found.")
        st.markdown("</div></div>", unsafe_allow_html=True)
        return

    data = []
    for record in records:
        timestamp = record.get("timestamp")
        parsed = _parse_ts(timestamp)
        subject = record.get("subjects") or {}
        data.append(
            {
                "Time": parsed.strftime("%Y-%m-%d %I:%M %p") if parsed else str(timestamp or "Unknown"),
                "Subject": subject.get("name", "Unknown"),
                "Subject Code": subject.get("subject_code", "Unknown"),
                "Present": bool(record.get("is_present", False)),
                "ts": parsed or datetime.min.replace(tzinfo=timezone.utc),
            }
        )
    df = pd.DataFrame(data).sort_values("ts", ascending=False)
    summary = (
        df.groupby(["Time", "Subject", "Subject Code"])
        .agg(Present=("Present", "sum"), Total=("Present", "count"))
        .reset_index()
    )
    summary["Attendance"] = summary["Present"].astype(str) + " / " + summary["Total"].astype(str) + " Students"
    st.dataframe(summary[["Time", "Subject", "Subject Code", "Attendance"]], width="stretch", hide_index=True)
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_teacher_command_center_v2():
    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data["teacher_id"]
    _inject_styles()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    active = st.session_state.current_teacher_tab
    selected = _sidebar(teacher_data, active)
    if selected:
        st.session_state.current_teacher_tab = selected
        if selected == "take_attendance" and st.session_state.get("dashboard_open_upload"):
            st.session_state.dashboard_open_upload = False
        st.rerun()

    subjects = get_teacher_subjects(teacher_id) or []
    records = get_attendance_for_teacher(teacher_id) or []

    if active == "take_attendance" and st.session_state.get("dashboard_mode") is None:
        # The first visible teacher landing page is the dashboard. Navigation still keeps the existing three workflows.
        st.session_state.dashboard_mode = True
    elif active != "take_attendance":
        st.session_state.dashboard_mode = False

    # Dashboard is explicitly the first sidebar item without adding any new workflow.
    if active == "take_attendance" and st.session_state.get("dashboard_mode", True):
        _render_dashboard(teacher_data, subjects, records)
        return

    if active == "take_attendance":
        _render_take_attendance(teacher_id)
    elif active == "manage_subjects":
        _render_manage_subjects(teacher_id)
    elif active == "attendance_records":
        _render_records(teacher_id)
