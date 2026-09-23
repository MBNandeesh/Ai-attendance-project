import io
from src.ui.dialog_styles import apply_dialog_styles

import segno
import streamlit as st


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    apply_dialog_styles()
    base_url = st.context.url.rstrip("/")
    join_url = f"{base_url}/?join-code={subject_code}"

    st.header("Share class")
    st.write(
        f"Students can use this link to join **{subject_name}**."
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=8, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Class code")
        st.code(subject_code, language="text")
        st.markdown("### Join link")
        st.code(join_url, language="text")
        st.info("Share the link or class code with your students.")

    with col2:
        st.markdown("### Scan to join")
        st.image(
            out.getvalue(),
            caption="Class QR code",
            width="stretch",
        )
