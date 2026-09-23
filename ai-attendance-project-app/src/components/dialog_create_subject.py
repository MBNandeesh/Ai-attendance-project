import streamlit as st
from src.ui.dialog_styles import apply_dialog_styles

from src.database.db import create_subject
from src.database.config import supabase


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    apply_dialog_styles()
    st.write("Enter the details of the new subject.")

    sub_id = st.text_input(
        "Subject Code",
        placeholder="CS101",
    )

    sub_name = st.text_input(
        "Subject Name",
        placeholder="Introduction to Computer Science",
    )

    sub_section = st.text_input(
        "Section",
        placeholder="A",
    )

    if st.button(
        "Create Subject Now",
        type="primary",
        width="stretch",
        key="create_subject_now",
    ):
        subject_code = sub_id.strip().upper()
        subject_name = sub_name.strip()
        section = sub_section.strip().upper()

        if not subject_code or not subject_name or not section:
            st.warning("Please fill all the fields.")
            return

        existing_subject = (
            supabase
            .table("subjects")
            .select("subject_id")
            .ilike("subject_code", subject_code)
            .limit(1)
            .execute()
        )

        if existing_subject.data:
            st.warning(
                f"Subject code '{subject_code}' already exists."
            )
            return

        try:
            create_subject(
                subject_code,
                subject_name,
                section,
                teacher_id,
            )
            st.toast("Subject created successfully.")
            st.rerun()
        except Exception as exc:
            st.error(f"Could not create the subject: {exc}")
