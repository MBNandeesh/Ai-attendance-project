import time
from src.ui.dialog_styles import apply_dialog_styles

import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():
    apply_dialog_styles()
    st.write(
        "Enter the subject code provided by your teacher to enroll."
    )

    join_code = st.text_input(
        "Subject Code",
        placeholder="Eg. CS101",
        key="student_enroll_code",
    )

    if st.button(
        "Enroll now",
        type="primary",
        width="stretch",
        key="student_enroll_submit",
    ):
        subject_code = join_code.strip().upper()

        if not subject_code:
            st.warning("Please enter a subject code.")
            return

        try:
            res = (
                supabase
                .table("subjects")
                .select("subject_id, name, subject_code")
                .ilike("subject_code", subject_code)
                .limit(1)
                .execute()
            )
        except Exception as exc:
            st.error(f"Could not find the subject: {exc}")
            return

        if not res.data:
            st.warning(
                f"No subject found with code '{subject_code}'."
            )
            return

        subject = res.data[0]
        student_id = st.session_state.student_data["student_id"]

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
            return

        if check.data:
            st.warning("You are already enrolled in this subject.")
            return

        try:
            enroll_student_to_subject(
                student_id,
                subject["subject_id"],
            )
            st.success(
                f"Successfully enrolled in {subject['name']}."
            )
            time.sleep(0.8)
            st.rerun()
        except Exception as exc:
            st.error(f"Enrollment failed: {exc}")
