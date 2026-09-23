import streamlit as st
from src.ui.dialog_styles import apply_dialog_styles

from src.database.config import supabase
from src.database.db import create_attendance


def _clear_attendance_workspace():
    st.session_state["attendance_images"] = []
    st.session_state["attendance_image_keys"] = set()
    st.session_state["attendance_input_version"] = (
        st.session_state.get("attendance_input_version", 0) + 1
    )
    st.session_state["voice_attendance_results"] = None


def show_attendance_result(df, logs):
    st.write("Please review attendance before confirming.")

    st.dataframe(
        df,
        hide_index=True,
        width="stretch",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Discard",
            width="stretch",
            key="attendance_discard",
        ):
            _clear_attendance_workspace()
            st.rerun()

    with col2:
        if st.button(
            "Confirm & Save",
            width="stretch",
            type="primary",
            key="attendance_confirm_save",
        ):
            try:
                if not logs:
                    st.warning("No attendance data to save.")
                    return

                subject_id = logs[0]["subject_id"]
                timestamp = logs[0]["timestamp"]

                existing = (
                    supabase
                    .table("attendance_logs")
                    .select("attendance_id")
                    .eq("subject_id", subject_id)
                    .eq("timestamp", timestamp)
                    .limit(1)
                    .execute()
                )

                if existing.data:
                    st.warning(
                        "This attendance session has already been saved."
                    )
                    _clear_attendance_workspace()
                    return

                create_attendance(logs)
                st.success("Attendance saved successfully.")
                _clear_attendance_workspace()
                st.rerun()

            except Exception as exc:
                st.error(f"Failed to save attendance: {exc}")


@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    apply_dialog_styles()
    show_attendance_result(df, logs)
