import streamlit as st
import numpy as np
import pandas as pd

from datetime import datetime, timezone

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout,
)
from src.ui.premium_ui import apply_premium_ui, auth_brand_panel

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
)

from src.database.config import supabase

from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

from src.pipelines.face_pipeline import predict_attendance


def _reset_teacher_workspace():
    st.session_state["is_logged_in"] = False
    st.session_state["user_role"] = None
    st.session_state.pop("teacher_data", None)
    st.session_state["teacher_login_type"] = "login"
    st.session_state["current_teacher_tab"] = "take_attendance"
    st.session_state["attendance_images"] = []
    st.session_state["attendance_image_keys"] = set()
    st.session_state.pop("attendance_subject_id", None)


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard(st.session_state["teacher_data"])
    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

    # Final UI layer is applied after the active screen's own CSS.
    apply_premium_ui()


def teacher_dashboard(teacher_data=None):
    if teacher_data is None:
        teacher_data = st.session_state["teacher_data"]

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}")

        if st.button(
            "Logout",
            type="secondary",
            key="teacher_logout_button",
            shortcut="control+backspace",
        ):
            _reset_teacher_workspace()
            st.session_state["login_type"] = None
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = (
            "primary"
            if st.session_state.current_teacher_tab == "take_attendance"
            else "tertiary"
        )

        if st.button(
            "Take Attendance",
            type=type1,
            width="stretch",
            icon=":material/ar_on_you:",
            key="teacher_tab_take_attendance",
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = (
            "primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "tertiary"
        )

        if st.button(
            "Manage Subjects",
            type=type2,
            width="stretch",
            icon=":material/book_ribbon:",
            key="teacher_tab_manage_subjects",
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = (
            "primary"
            if st.session_state.current_teacher_tab == "attendance_records"
            else "tertiary"
        )

        if st.button(
            "Attendance Records",
            type=type3,
            width="stretch",
            icon=":material/cards_stack:",
            key="teacher_tab_attendance_records",
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    st.header("Take AI Attendance")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "attendance_image_keys" not in st.session_state:
        st.session_state.attendance_image_keys = set()

    subjects = get_teacher_subjects(teacher_id) or []

    if not subjects:
        st.warning(
            "You haven't created any subjects yet. Please create one to begin."
        )
        return

    subject_options = {
        f"{subject['name']} - {subject['subject_code']}": subject["subject_id"]
        for subject in subjects
    }

    col1, col2 = st.columns(
        [3, 1],
        vertical_alignment="bottom",
    )

    with col1:
        selected_subject_label = st.selectbox(
            "Select Subject",
            options=list(subject_options.keys()),
            key="attendance_subject_selector",
        )

    selected_subject_id = subject_options[selected_subject_label]

    previous_subject_id = st.session_state.get("attendance_subject_id")
    if previous_subject_id != selected_subject_id:
        st.session_state.attendance_subject_id = selected_subject_id
        if previous_subject_id is not None and st.session_state.attendance_images:
            st.session_state.attendance_images = []
            st.session_state.attendance_image_keys = set()
            st.info("Photos were cleared because you changed the subject.")

    with col2:
        if st.button(
            "Add Photos",
            type="primary",
            icon=":material/photo_prints:",
            width="stretch",
            key="add_attendance_photos",
        ):
            add_photos_dialog()

    st.divider()

    if st.session_state.attendance_images:
        st.header("Added Photos")

        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(
                    img,
                    width="stretch",
                    caption=f"Photo {idx + 1}",
                )

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "Clear all photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            disabled=not has_photos,
            key="clear_attendance_photos",
        ):
            st.session_state.attendance_images = []
            st.session_state.attendance_image_keys = set()
            st.rerun()

    with c2:
        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/analytics:",
            disabled=not has_photos,
            key="run_face_analysis",
        ):
            with st.spinner("Deep scanning classroom photos..."):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert("RGB"))
                    detected, _, _ = predict_attendance(img_np)

                    for sid in detected.keys():
                        student_id = int(sid)
                        all_detected_ids.setdefault(student_id, []).append(
                            f"Photo {idx + 1}"
                        )

                enrolled_res = (
                    supabase
                    .table("subject_students")
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
                current_timestamp = datetime.now(timezone.utc).isoformat()

                for node in enrolled_students:
                    student = node.get("students") if isinstance(node, dict) else None
                    if not isinstance(student, dict) or student.get("student_id") is None:
                        continue

                    student_id = int(student["student_id"])
                    sources = all_detected_ids.get(student_id, [])
                    is_present = bool(sources)

                    results.append({
                        "Name": student.get("name", "Unknown"),
                        "ID": student_id,
                        "Source": ", ".join(sources) if is_present else "-",
                        "Status": "Present" if is_present else "Absent",
                    })

                    attendance_to_log.append({
                        "student_id": student_id,
                        "subject_id": selected_subject_id,
                        "timestamp": current_timestamp,
                        "is_present": is_present,
                    })

                if not attendance_to_log:
                    st.warning("No valid enrolled students were found.")
                    return

                attendance_result_dialog(
                    pd.DataFrame(results),
                    attendance_to_log,
                )

    with c3:
        if st.button(
            "Use Voice Attendance",
            type="primary",
            width="stretch",
            icon=":material/mic:",
            key="use_voice_attendance",
        ):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    col1, col2 = st.columns(2)

    with col1:
        st.header("Manage Subjects", width="stretch")

    with col2:
        if st.button(
            "Create New Subject",
            width="stretch",
            key="create_new_subject",
        ):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id) or []

    if not subjects:
        st.info("No subjects found. Create one above.")
        return

    for sub in subjects:
        subject_id = sub.get("subject_id")
        stats = [
            ("", "Students", sub.get("total_students", 0)),
            ("", "Classes", sub.get("total_classes", 0)),
        ]

        def share_btn(
            subject_name=sub.get("name", "Subject"),
            subject_code=sub.get("subject_code", ""),
            current_subject_id=subject_id,
        ):
            if st.button(
                "Share class link",
                key=f"share_{current_subject_id or subject_code}",
                icon=":material/share:",
                width="stretch",
            ):
                share_subject_dialog(subject_name, subject_code)

        subject_card(
            name=sub.get("name", "Unknown subject"),
            code=sub.get("subject_code", "Unknown"),
            section=sub.get("section", "-"),
            stats=stats,
            footer_callback=share_btn,
        )


def teacher_tab_attendance_records():
    st.header("Attendance Records")
    teacher_id = st.session_state.teacher_data["teacher_id"]
    records = get_attendance_for_teacher(teacher_id) or []

    if not records:
        st.info("No attendance records found.")
        return

    data = []
    for record in records:
        timestamp = record.get("timestamp")

        if not timestamp:
            formatted_time = "Unknown"
            timestamp_group = "Unknown"
        else:
            try:
                parsed_timestamp = datetime.fromisoformat(
                    str(timestamp).replace("Z", "+00:00")
                )
                formatted_time = parsed_timestamp.strftime(
                    "%Y-%m-%d %I:%M %p"
                )
                timestamp_group = parsed_timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except (ValueError, TypeError):
                formatted_time = str(timestamp)
                timestamp_group = str(timestamp)

        subject_data = record.get("subjects") or {}
        if not isinstance(subject_data, dict):
            subject_data = {}

        data.append({
            "ts_group": timestamp_group,
            "Time": formatted_time,
            "Subject": subject_data.get("name", "Unknown"),
            "Subject Code": subject_data.get("subject_code", "Unknown"),
            "is_present": bool(record.get("is_present", False)),
        })

    if not data:
        st.info("No attendance records found.")
        return

    df = pd.DataFrame(data)
    summary = (
        df.groupby(
            ["ts_group", "Time", "Subject", "Subject Code"]
        )
        .agg(
            Present_Count=("is_present", "sum"),
            Total_Count=("is_present", "count"),
        )
        .reset_index()
    )

    summary["Attendance Stats"] = (
        summary["Present_Count"].astype(str)
        + " / "
        + summary["Total_Count"].astype(str)
        + " Students"
    )

    display_df = (
        summary
        .sort_values(by="ts_group", ascending=False)
        [["Time", "Subject", "Subject Code", "Attendance Stats"]]
    )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
    )


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        st.session_state.login_type = "teacher"
        return True

    return False


def teacher_screen_login():
    with st.container(key="teacher-auth-layout"):
        col_left, col_right = st.columns(
            [1.08, 0.92],
            vertical_alignment="center",
            gap="large",
        )

        with col_left:
            st.markdown(auth_brand_panel("teacher"), unsafe_allow_html=True)

        with col_right:
            with st.container(border=True, key="teacher-auth-card"):
                if st.button(
                    "Back to Home",
                    type="tertiary",
                    key="teacher_login_back",
                    shortcut="control+backspace",
                    icon=":material/arrow_back:",
                ):
                    st.session_state["login_type"] = None
                    st.session_state["teacher_login_type"] = "login"
                    st.rerun()

                st.header("WELCOME BACK")
                st.markdown(
                    "<div style='color:#5E6A82;font-size:16px;font-weight:650;margin-bottom:1rem;'>"
                    "Login to AI Attendance · Continue to your dashboard"
                    "</div>",
                    unsafe_allow_html=True,
                )

                teacher_username = st.text_input(
                    "Username",
                    placeholder="Enter username",
                )

                teacher_pass = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter password",
                )

                st.markdown("<div style='height:.35rem'></div>", unsafe_allow_html=True)

                if st.button(
                    "Login",
                    icon=":material/arrow_forward:",
                    shortcut="control+enter",
                    width="stretch",
                    key="teacher_login_submit",
                ):
                    if login_teacher(teacher_username.strip(), teacher_pass):
                        st.toast("Welcome back!")
                        import time
                        time.sleep(0.8)
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

                if st.button(
                    "Register Instead",
                    type="secondary",
                    icon=":material/person_add:",
                    width="stretch",
                    key="teacher_register_switch",
                ):
                    st.session_state.teacher_login_type = "register"
                    st.rerun()

    footer_dashboard()


def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm,
):
    teacher_username = teacher_username.strip()
    teacher_name = teacher_name.strip()

    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required."

    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    if check_teacher_exists(teacher_username):
        return False, "Username already taken."

    try:
        create_teacher(
            teacher_username,
            teacher_pass,
            teacher_name,
        )
        return True, "Successfully created. Login now."
    except Exception as exc:
        return False, f"Unexpected error while creating account: {exc}"


def teacher_screen_register():
    with st.container(key="teacher-auth-layout"):
        col_left, col_right = st.columns(
            [1.08, 0.92],
            vertical_alignment="center",
            gap="large",
        )

        with col_left:
            st.markdown(auth_brand_panel("teacher"), unsafe_allow_html=True)

        with col_right:
            with st.container(border=True, key="teacher-auth-card"):
                if st.button(
                    "Back to Home",
                    type="tertiary",
                    key="teacher_register_back",
                    shortcut="control+backspace",
                    icon=":material/arrow_back:",
                ):
                    st.session_state["login_type"] = None
                    st.session_state["teacher_login_type"] = "login"
                    st.rerun()

                st.header("CREATE TEACHER PROFILE")
                st.markdown(
                    "<div style='color:#5E6A82;font-size:16px;font-weight:650;margin-bottom:1rem;'>"
                    "Set up your account to manage classroom attendance"
                    "</div>",
                    unsafe_allow_html=True,
                )

                teacher_username = st.text_input(
                    "Username",
                    placeholder="Enter username",
                )

                teacher_name = st.text_input(
                    "Name",
                    placeholder="Enter your name",
                )

                teacher_pass = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter password",
                )

                teacher_pass_confirm = st.text_input(
                    "Confirm password",
                    type="password",
                    placeholder="Re-enter password",
                )

                if st.button(
                    "Register now",
                    icon=":material/person_add:",
                    shortcut="control+enter",
                    width="stretch",
                    key="teacher_register_submit",
                ):
                    success, message = register_teacher(
                        teacher_username,
                        teacher_name,
                        teacher_pass,
                        teacher_pass_confirm,
                    )

                    if success:
                        st.success(message)
                        import time
                        time.sleep(1)
                        st.session_state.teacher_login_type = "login"
                        st.rerun()
                    else:
                        st.error(message)

                if st.button(
                    "Login Instead",
                    type="secondary",
                    icon=":material/login:",
                    width="stretch",
                    key="teacher_login_switch",
                ):
                    st.session_state.teacher_login_type = "login"
                    st.rerun()

    footer_dashboard()
