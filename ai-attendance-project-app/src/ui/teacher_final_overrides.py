import streamlit as st


def apply_teacher_final_overrides():
    """Final teacher-dashboard-only presentation fixes. UI styling only."""
    st.markdown(
        """
        <style>
        /* The animated counter used a temporary Streamlit element outside the
           statistic cards. Hide that temporary node while keeping the real
           values inside their cards visible. */
        .teacher-stat-value {
            display: none !important;
        }

        .teacher-stat-card .teacher-stat-value {
            display: block !important;
        }

        /* Increase teacher-dashboard readability without touching behaviour. */
        .teacher-search {
            font-size: 15px !important;
        }

        .teacher-profile-name {
            font-size: 16px !important;
        }

        .teacher-profile-role {
            font-size: 13px !important;
        }

        .teacher-greeting p {
            font-size: 17px !important;
        }

        .teacher-date-main {
            font-size: 15px !important;
        }

        .teacher-date-sub {
            font-size: 12px !important;
        }

        .teacher-stat-label {
            font-size: 14px !important;
        }

        .teacher-stat-value {
            font-size: 36px !important;
        }

        .teacher-stat-note {
            font-size: 13px !important;
        }

        .teacher-card-title {
            font-size: 20px !important;
        }

        .teacher-live {
            font-size: 13px !important;
        }

        .teacher-camera-title {
            font-size: 20px !important;
        }

        .teacher-camera-sub {
            font-size: 13px !important;
        }

        .teacher-table th {
            font-size: 13px !important;
        }

        .teacher-table td {
            font-size: 14px !important;
        }

        .teacher-status {
            font-size: 12px !important;
        }

        .teacher-view-all {
            font-size: 13px !important;
        }

        .teacher-footer-title {
            font-size: 23px !important;
        }

        .teacher-footer-copy {
            font-size: 14px !important;
        }

        /* Active sidebar item must remain readable on its blue surface. */
        section[data-testid="stSidebar"] .stButton > button[kind="primary"],
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] * {
            color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
