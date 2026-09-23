import streamlit as st


BRAND = "AI Attendance System"


def header_home():
    st.markdown(
        """
        <div class="app-topbar app-topbar-home">
            <div class="brand-lockup">
                <div class="brand-mark">AI</div>
                <div>
                    <div class="brand-name">AI Attendance System</div>
                    <div class="brand-tagline">Simple. Smart. Reliable.</div>
                </div>
            </div>
            <div class="topbar-status">Face + Voice · Built for classrooms</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def header_dashboard():
    st.markdown(
        f"""
        <div class="app-topbar">
            <div class="brand-lockup">
                <div class="brand-mark">AI</div>
                <div>
                    <div class="brand-name">{BRAND}</div>
                    <div class="brand-tagline">Attendance management</div>
                </div>
            </div>
            <div class="topbar-status topbar-status-soft">AI attendance workspace</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
