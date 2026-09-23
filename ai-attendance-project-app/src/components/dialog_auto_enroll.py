import time

import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_data = st.session_state.get("student_data")
    if not student_data:
        st.query_params.clear()
        st.rerun()
        return

    student_id = student_data["student_id"]
    normalized_code = subject_code.strip()

    try:
        response = (
            supabase
            .table("subjects")
            .select("subject_id, name, subject_code")
            .ilike("subject_code", normalized_code)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        st.error(f"Could not load the class: {exc}")
        if st.button("Close", key="auto_enroll_error_close"):
            st.query_params.clear()
            st.rerun()
        return

    if not response.data:
        st.error("Subject code not found.")
        if st.button("Close", key="auto_enroll_close"):
            st.query_params.clear()
            st.rerun()
        return

    subject = response.data[0]

    try:
        check = (
            supabase
            .table("subject_students")
            .select("id")
            .eq("subject_id", subject["subject_id"])
            .eq("student_id", student_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        st.error(f"Could not check your enrollment: {exc}")
        if st.button("Close", key="auto_enroll_check_close"):
            st.query_params.clear()
            st.rerun()
        return

    if check.data:
        st.info("You are already enrolled in this subject.")
        if st.button(
            "Got it",
            type="primary",
            width="stretch",
            key="auto_enroll_done",
        ):
            st.query_params.clear()
            st.rerun()
        return

    st.write(
        f"Would you like to enroll in **{subject['name']}**?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "No thanks",
            width="stretch",
            key="auto_enroll_cancel",
        ):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button(
            "Yes, enroll now",
            type="primary",
            width="stretch",
            key="auto_enroll_confirm",
        ):
            try:
                enroll_student_to_subject(
                    student_id,
                    subject["subject_id"],
                )
                st.success("Joined successfully.")
                st.query_params.clear()
                time.sleep(1)
                st.rerun()
            except Exception as exc:
                st.error(f"Enrollment failed: {exc}")
