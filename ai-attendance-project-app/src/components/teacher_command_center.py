import html
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from src.database.db import get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
import src.screens.teacher_screen as teacher_module


def _safe_name(value):
    return html.escape(str(value or "User"))


def _today_records(records):
    today = datetime.now(timezone.utc).date()
    present = 0
    total = 0
    for record in records or []:
        timestamp = record.get("timestamp")
        try:
            parsed = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
            if parsed.date() == today:
                total += 1
                present += int(bool(record.get("is_present", False)))
        except (TypeError, ValueError):
            continue
    return present, total


def _render_styles():
    st.markdown(
        """
        <style>
            .cc-shell { margin: -0.4rem 0 0; }
            .cc-topbar {
                display:flex; align-items:center; gap:14px; padding:12px 16px;
                border-radius:20px; margin-bottom:16px;
                background:linear-gradient(120deg,#EAF4FF,#F8FBFF 55%,#E8F2FF);
                border:1px solid rgba(30,107,214,.12);
                box-shadow:0 12px 30px rgba(22,67,120,.08);
            }
            .cc-search {
                flex:1; padding:11px 15px; border-radius:13px;
                background:#FFFFFFCC; border:1px solid #D8E6F5;
                color:#5B6B82; font-size:14px; font-weight:600;
            }
            .cc-user {
                display:flex; align-items:center; gap:10px; margin-left:auto;
                color:#0D2D57; font-size:15px; font-weight:800;
            }
            .cc-avatar {
                width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;
                background:linear-gradient(145deg,#DCEBFA,#B8D5F3);color:#123A68;font-weight:800;
                border:2px solid #FFFFFF; box-shadow:0 6px 18px rgba(30,107,214,.16);
            }
            .cc-hero {
                position:relative; overflow:hidden; padding:30px 32px 26px; border-radius:26px;
                background:linear-gradient(125deg,#F8FCFF 0%,#E8F3FF 55%,#DCEBFF 100%);
                border:1px solid rgba(30,107,214,.12);
                box-shadow:0 18px 42px rgba(30,107,214,.10); margin-bottom:16px;
            }
            .cc-hero::after {
                content:"";position:absolute;inset:auto -80px -100px auto;width:430px;height:250px;border-radius:50%;
                background:radial-gradient(circle,rgba(34,211,238,.18),transparent 68%);
                animation:cc-float 8s ease-in-out infinite;
            }
            .cc-eyebrow { color:#0FA9A3; font-size:12px; font-weight:900; letter-spacing:.17em; text-transform:uppercase; }
            .cc-title { margin:6px 0 7px; color:#102B55; font-size:42px; line-height:1.08; font-weight:900; letter-spacing:-.03em; }
            .cc-title span { background:linear-gradient(90deg,#1E6BD6,#5B43C6,#1E6BD6);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:cc-gradient 5s ease infinite; }
            .cc-copy { max-width:690px;color:#526A8B;font-size:17px;font-weight:600;line-height:1.6; }
            .cc-badges { display:flex; gap:10px; flex-wrap:wrap; margin-top:18px; }
            .cc-badge { display:flex;align-items:center;gap:8px;padding:9px 13px;border-radius:999px;background:#FFFFFFD9;border:1px solid #D9E9F8;color:#16355F;font-size:13px;font-weight:800;box-shadow:0 6px 16px rgba(30,107,214,.06); }
            .cc-dot { width:8px;height:8px;border-radius:50%;background:#20B477;box-shadow:0 0 0 5px rgba(32,180,119,.11); }
            .cc-grid { display:grid; grid-template-columns:1.08fr 1fr .78fr; gap:16px; }
            .cc-card { background:rgba(255,255,255,.94); border:1px solid rgba(30,107,214,.12); border-radius:22px; padding:18px; box-shadow:0 12px 32px rgba(23,61,105,.07); animation:cc-rise .65s cubic-bezier(.2,.8,.2,1) both; }
            .cc-card:hover { transform:translateY(-4px); box-shadow:0 20px 42px rgba(30,107,214,.12); transition:transform .2s ease,box-shadow .2s ease; }
            .cc-card-title { color:#0F2F61; font-size:19px;font-weight:900; }
            .cc-card-sub { color:#70819A;font-size:13px;font-weight:600;margin-top:3px; }
            .cc-camera { min-height:280px; border-radius:18px; background:radial-gradient(circle at 50% 35%,#3A3A3A,#151515 60%,#0D0D0D); color:white; display:flex;flex-direction:column;align-items:center;justify-content:center; gap:9px; border:3px solid #E3F1FF; box-shadow:inset 0 0 40px rgba(0,0,0,.22); }
            .cc-camera .material-symbols-rounded { font-size:42px; }
            .cc-camera-title { font-size:22px;font-weight:900; }
            .cc-camera-sub { color:#C8D1DB;font-size:13px;font-weight:600; }
            .cc-status { display:inline-flex;align-items:center;gap:8px;padding:8px 11px;border-radius:999px;background:#0C243DCC;color:#FFFFFF;font-size:12px;font-weight:800;margin-bottom:8px; }
            .cc-status .cc-dot { background:#20B477; }
            .cc-session-head { display:flex;align-items:center;justify-content:space-between;margin-bottom:12px; }
            .cc-mini-button { border:1px solid #CEE2F7;padding:7px 10px;border-radius:10px;background:#F6FBFF;color:#1E6BD6;font-size:12px;font-weight:800; }
            .cc-stat-grid { display:grid;grid-template-columns:1fr 1fr;gap:10px; }
            .cc-stat { padding:15px;border-radius:17px;background:linear-gradient(145deg,#F8FBFF,#F1F7FF);border:1px solid #DFECF9; }
            .cc-stat-label { color:#617895;font-size:12px;font-weight:800; }
            .cc-stat-value { color:#123A68;font-size:28px;font-weight:900;margin-top:4px; }
            .cc-stat-accent { color:#0FA9A3;font-size:11px;font-weight:900;margin-top:2px; }
            .cc-actions { display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0; }
            .cc-section { color:#102F5E;font-size:20px;font-weight:900;margin:18px 0 10px; }
            .cc-table { width:100%; border-collapse:separate;border-spacing:0;overflow:hidden;border:1px solid #DDEAF7;border-radius:16px;background:#FFFFFF; }
            .cc-table th { text-align:left;background:#F2F8FF;color:#547091;font-size:12px;font-weight:900;padding:11px 13px; }
            .cc-table td { color:#17375E;font-size:13px;font-weight:650;padding:11px 13px;border-top:1px solid #EEF4FA; }
            .cc-pill { display:inline-flex;padding:5px 9px;border-radius:999px;font-size:11px;font-weight:900; }
            .cc-pill.present { background:#E6FAF2;color:#159563; }
            .cc-pill.absent { background:#FFF3DA;color:#C27C06; }
            .cc-activity { display:flex;gap:11px;padding:10px 0;border-bottom:1px solid #EDF3F8;align-items:flex-start; }
            .cc-activity:last-child { border-bottom:0; }
            .cc-activity-dot { width:10px;height:10px;border-radius:50%;margin-top:5px;background:#1E6BD6;box-shadow:0 0 0 5px rgba(30,107,214,.10);flex:0 0 auto; }
            .cc-activity-title { color:#16365F;font-size:13px;font-weight:900; }
            .cc-activity-copy { color:#7A8CA4;font-size:11px;font-weight:650;margin-top:2px; }
            .cc-banner { margin-top:16px;padding:18px 22px;border-radius:20px;background:linear-gradient(120deg,#5B43C6,#2286E7 62%,#7BDBF1);color:white;box-shadow:0 14px 32px rgba(91,67,198,.20);display:flex;align-items:center;justify-content:space-between;gap:18px; }
            .cc-banner-title { font-size:20px;font-weight:900; }
            .cc-banner-copy { color:#EEF6FF;font-size:13px;font-weight:650;margin-top:3px; }
            @keyframes cc-rise { from {opacity:0;transform:translateY(16px)} to {opacity:1;transform:translateY(0)} }
            @keyframes cc-gradient { 0%,100% {background-position:0 50%} 50% {background-position:100% 50%} }
            @keyframes cc-float { 0%,100% {transform:translate3d(0,0,0)} 50% {transform:translate3d(-18px,8px,0)} }
            @media (max-width: 1100px) { .cc-grid{grid-template-columns:1fr 1fr}.cc-actions{grid-template-columns:1fr 1fr}.cc-hero{padding:24px}.cc-title{font-size:34px} }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _sidebar(teacher_data, active):
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-mark">AI</div>
                <div>
                    <div class="sidebar-brand-name">AI Attendance System</div>
                    <div class="sidebar-brand-subtitle">Simple. Smart. Reliable.</div>
                </div>
            </div>
            <div class="sidebar-section-label">Workspace</div>
            """,
            unsafe_allow_html=True,
        )

        items = [
            ("take_attendance", "Home", ":material/home:"),
            ("take_attendance", "Take Attendance", ":material/photo_camera:"),
            ("manage_subjects", "Manage Subjects", ":material/menu_book:"),
            ("attendance_records", "Attendance Records", ":material/bar_chart:"),
        ]
        clicked = None
        for key, label, icon in items:
            kind = "primary" if active == key and label != "Home" else "tertiary"
            if st.button(label, key=f"cc_nav_{label.lower().replace(' ','_')}", type=kind, width="stretch", icon=icon):
                clicked = key

        st.markdown('<div style="height:220px"></div>', unsafe_allow_html=True)
        name = _safe_name(teacher_data.get("name", "Teacher"))
        st.markdown(
            f"""
            <div class="sidebar-user-card">
                <div class="sidebar-user-avatar">{name[:1].upper()}</div>
                <div><div class="sidebar-user-name">{name}</div><div class="sidebar-user-role">Teacher</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Logout", key="cc_logout", type="secondary", width="stretch", icon=":material/logout:"):
            teacher_module._reset_teacher_workspace()
            st.session_state["login_type"] = None
            st.rerun()
    return clicked


def render_teacher_command_center():
    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data["teacher_id"]
    _render_styles()

    active = st.session_state.get("current_teacher_tab", "take_attendance")
    nav_click = _sidebar(teacher_data, active)
    if nav_click:
        st.session_state.current_teacher_tab = nav_click
        st.rerun()

    subjects = get_teacher_subjects(teacher_id) or []
    records = get_attendance_for_teacher(teacher_id) or []
    total_students = sum(int(s.get("total_students", 0) or 0) for s in subjects)
    present_today, records_today = _today_records(records)
    absent_today = max(total_students - present_today, 0)
    rate = int(round((present_today / total_students) * 100)) if total_students else 0

    st.markdown('<div class="cc-shell">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="cc-topbar">
            <div class="cc-search">Search anything... <span style="float:right;color:#8AA0BC">Ctrl + K</span></div>
            <div style="color:#1E6BD6;font-size:22px">●</div>
            <div class="cc-user"><div class="cc-avatar">{_safe_name(teacher_data.get('name','T'))[:1].upper()}</div><span>Welcome back,<br><b>{_safe_name(teacher_data.get('name','Teacher')).upper()}!</b></span></div>
        </div>
        <div class="cc-hero">
            <div class="cc-eyebrow">AI ATTENDANCE WORKSPACE</div>
            <div class="cc-title">Let's Make Attendance <span>Smarter</span></div>
            <div class="cc-copy">Use AI to quickly and accurately mark attendance for your class.<br>Save time, stay organized, and focus on what matters most.</div>
            <div class="cc-badges">
                <div class="cc-badge"><span style="color:#F59E0B">⚡</span> Fast</div>
                <div class="cc-badge"><span style="color:#20B477">✓</span> Accurate</div>
                <div class="cc-badge"><span style="color:#5B43C6">●</span> Secure</div>
                <div class="cc-badge"><span style="color:#1E6BD6">✦</span> AI-Powered</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([1.05, 1, .8], gap="medium")

    with left:
        with st.container(border=True):
            st.markdown('<div class="cc-card-title">Camera Preview</div><div class="cc-card-sub">AI face detection ready</div>', unsafe_allow_html=True)
            st.markdown('<div class="cc-camera"><div class="cc-status"><span class="cc-dot"></span> Ready</div><span class="material-symbols-rounded">photo_camera</span><div class="cc-camera-title">Camera Preview</div><div class="cc-camera-sub">Add classroom photos to start analysis</div></div>', unsafe_allow_html=True)
            if st.button("Start Camera", type="primary", width="stretch", icon=":material/play_arrow:", key="cc_start_camera"):
                if subjects:
                    st.session_state["current_teacher_tab"] = "take_attendance"
                    add_photos_dialog()
                else:
                    st.warning("Create a subject first, then start attendance.")

    with middle:
        with st.container(border=True):
            st.markdown('<div class="cc-session-head"><div><div class="cc-card-title">Today\'s Session</div><div class="cc-card-sub">Configure your attendance session</div></div></div>', unsafe_allow_html=True)
            if subjects:
                options = {f"{s.get('name','Subject')} - {s.get('subject_code','')}": s.get('subject_id') for s in subjects}
                selected = st.selectbox("Subject", list(options.keys()), key="cc_subject_select")
                selected_subject_id = options[selected]
                st.date_input("Date", value=datetime.now().date(), key="cc_session_date")
                section = next((s.get("section") for s in subjects if s.get("subject_id") == selected_subject_id), "-")
                st.text_input("Class / Batch", value=str(section or "-"), disabled=True, key="cc_section")
                if st.button("Start Attendance", type="primary", width="stretch", icon=":material/play_arrow:", key="cc_start_attendance"):
                    add_photos_dialog()
                if st.button("Use Voice Attendance", type="secondary", width="stretch", icon=":material/mic:", key="cc_voice_attendance"):
                    voice_attendance_dialog(selected_subject_id)
            else:
                st.info("Create a subject to start a session.")
                if st.button("Create Subject", type="primary", width="stretch", key="cc_create_subject"):
                    teacher_module.create_subject_dialog(teacher_id)

    with right:
        with st.container(border=True):
            st.markdown('<div class="cc-card-title">Quick Stats</div><div class="cc-card-sub">Today\'s classroom snapshot</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="cc-stat-grid">
                  <div class="cc-stat"><div class="cc-stat-label">Total Students</div><div class="cc-stat-value">{total_students}</div><div class="cc-stat-accent">Enrolled</div></div>
                  <div class="cc-stat"><div class="cc-stat-label">Present</div><div class="cc-stat-value">{present_today}</div><div class="cc-stat-accent">Today</div></div>
                  <div class="cc-stat"><div class="cc-stat-label">Absent</div><div class="cc-stat-value">{absent_today}</div><div class="cc-stat-accent">Not marked</div></div>
                  <div class="cc-stat"><div class="cc-stat-label">Attendance Rate</div><div class="cc-stat-value">{rate}%</div><div class="cc-stat-accent">For today</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="cc-section">Quick Actions</div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4, gap="medium")
    quick = [
        (q1, "Manage Subjects", "Create and organize subjects", "manage_subjects", ":material/menu_book:"),
        (q2, "Take Attendance", "Open AI attendance workflow", "take_attendance", ":material/photo_camera:"),
        (q3, "View Records", "Review attendance history", "attendance_records", ":material/bar_chart:"),
        (q4, "Voice Attendance", "Use voice attendance option", "voice", ":material/mic:"),
    ]
    for col, title, copy, target, icon in quick:
        with col:
            with st.container(border=True):
                st.markdown(f'<div class="cc-card-title">{title}</div><div class="cc-card-sub">{copy}</div>', unsafe_allow_html=True)
                if st.button("Open", type="secondary", width="stretch", icon=icon, key=f"cc_quick_{target}"):
                    if target == "voice" and subjects:
                        voice_attendance_dialog(subjects[0].get("subject_id"))
                    else:
                        st.session_state.current_teacher_tab = target
                        st.rerun()

    st.markdown('<div class="cc-section">Recent Attendance</div>', unsafe_allow_html=True)
    recent_rows = []
    for rec in records[:6]:
        student = rec.get("students") or {}
        subject = rec.get("subjects") or {}
        recent_rows.append({
            "Student Name": student.get("name", "Unknown"),
            "Subject": subject.get("name", "Unknown"),
            "Status": bool(rec.get("is_present", False)),
            "Time": rec.get("timestamp", "-"),
        })
    if recent_rows:
        rows_html = "".join(
            f"<tr><td>{_safe_name(r['Student Name'])}</td><td>{_safe_name(r['Subject'])}</td><td><span class='cc-pill {'present' if r['Status'] else 'absent'}'>{'Present' if r['Status'] else 'Absent'}</span></td><td>{_safe_name(r['Time'])}</td></tr>"
            for r in recent_rows
        )
        st.markdown(
            f"""
            <table class="cc-table"><thead><tr><th>Student Name</th><th>Subject</th><th>Status</th><th>Time</th></tr></thead><tbody>{rows_html}</tbody></table>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No attendance activity yet.")

    st.markdown('<div class="cc-section">Today\'s Activity</div>', unsafe_allow_html=True)
    events = [
        ("System Ready", "Attendance workspace loaded", "#20B477"),
        ("Subject Snapshot", f"{len(subjects)} subject(s) available", "#1E6BD6"),
        ("Attendance Engine", "Face recognition pipeline ready", "#5B43C6"),
    ]
    activity_html = "".join(
        f"<div class='cc-activity'><span class='cc-activity-dot' style='background:{color}'></span><div><div class='cc-activity-title'>{title}</div><div class='cc-activity-copy'>{copy}</div></div></div>"
        for title, copy, color in events
    )
    st.markdown(f"<div class='cc-card'>{activity_html}</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="cc-banner">
          <div><div class="cc-banner-title">Keep Going!</div><div class="cc-banner-copy">Consistent attendance leads to better learning outcomes.</div></div>
          <div style="font-weight:800;font-size:13px;text-align:right">Technology for a better, more present classroom.<br>— AI Attendance System</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
