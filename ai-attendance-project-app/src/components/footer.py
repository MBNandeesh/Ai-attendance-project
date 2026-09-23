import streamlit as st


def _footer():
    st.markdown(
        """
        <div class="app-footer app-footer-minimal">
            <div class="footer-credit-only">M B NANDEESH</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer_home():
    _footer()


def footer_dashboard():
    _footer()
