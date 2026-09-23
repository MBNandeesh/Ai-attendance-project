import streamlit as st

import src.screens.teacher_screen as teacher_screen_module
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.ui.theme_overrides import style_theme_overrides
from src.ui.emphasis_styles import style_emphasis_elements
from src.ui.final_ui_overrides import apply_final_ui_overrides
from src.ui.reference_background import apply_reference_background
from src.ui.mobile_glow_overrides import apply_mobile_glow_overrides
from src.components.teacher_dashboard_ui import render_teacher_dashboard
from src.ui.premium_ui import apply_premium_ui
from src.ui.light_surface_overrides import apply_light_surface_overrides
from src.ui.teacher_final_overrides import apply_teacher_final_overrides


# Keep the existing teacher workflows, but use the new reference-based teacher UI.
teacher_screen_module.teacher_dashboard = render_teacher_dashboard


def _hide_sidebar_on_home():
    if st.session_state.get("login_type") is None:
        st.markdown(
            """
            <style>
                section[data-testid="stSidebar"] { display: none !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def main():
    st.set_page_config(
        page_title="AI Attendance System",
        page_icon=":material/how_to_reg:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    apply_reference_background()
    style_theme_overrides()
    style_emphasis_elements()
    apply_final_ui_overrides()
    apply_mobile_glow_overrides()
    _hide_sidebar_on_home()

    match st.session_state["login_type"]:
        case "teacher":
            teacher_screen_module.teacher_screen()
        case "student":
            student_screen()
        case None:
            home_screen()

    # Final visual layer intentionally runs after the active screen so the
    # shared brand system wins over older page-specific cosmetic CSS.
    apply_premium_ui()
    apply_light_surface_overrides()
    apply_teacher_final_overrides()

    join_code = st.query_params.get("join-code")

    if join_code:
        if st.session_state.get("login_type") != "student":
            st.session_state["login_type"] = "student"
            st.rerun()

        if (
            st.session_state.get("is_logged_in")
            and st.session_state.get("user_role") == "student"
        ):
            auto_enroll_dialog(join_code)


main()
