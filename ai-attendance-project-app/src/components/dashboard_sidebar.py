import streamlit as st


def _nav_button(label, key, active_key, icon):
    return st.button(
        label,
        key=f"sidebar_{key}",
        type="primary" if key == active_key else "tertiary",
        width="stretch",
        icon=icon,
    )


def render_dashboard_sidebar(role, active_key):
    user_key = "teacher_data" if role == "teacher" else "student_data"
    user = st.session_state.get(user_key) or {}
    name = user.get("name", "User")

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
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section-label">Workspace</div>',
            unsafe_allow_html=True,
        )

        selected = None
        if role == "teacher":
            items = [
                ("take_attendance", "Take Attendance", ":material/photo_camera:"),
                ("manage_subjects", "Manage Subjects", ":material/menu_book:"),
                ("attendance_records", "Attendance Records", ":material/bar_chart:"),
            ]
        else:
            items = [
                ("dashboard", "Dashboard", ":material/dashboard:"),
                ("face_profile", "Face Profile", ":material/face:"),
            ]

        for key, label, icon in items:
            if _nav_button(label, key, active_key, icon):
                selected = key

        st.markdown(
            '<div class="sidebar-spacer"></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="sidebar-user-card">
                <div class="sidebar-user-avatar">{name[:1].upper()}</div>
                <div>
                    <div class="sidebar-user-name">{name}</div>
                    <div class="sidebar-user-role">{role.title()}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Logout",
            key=f"sidebar_logout_{role}",
            type="secondary",
            width="stretch",
            icon=":material/logout:",
        ):
            selected = "logout"

    return selected
