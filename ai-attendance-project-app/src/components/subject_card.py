import html

import streamlit as st


def subject_card(
    name,
    code,
    section,
    stats=None,
    progress=None,
    footer_callback=None,
):
    safe_name = html.escape(str(name))
    safe_code = html.escape(str(code))
    safe_section = html.escape(str(section))

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="student-subject-inner">
                <div class="student-subject-kicker">COURSE</div>
                <div class="student-subject-title">{safe_name}</div>
                <div class="student-subject-meta">
                    <span class="student-subject-code">{safe_code}</span>
                    <span class="student-subject-separator">•</span>
                    <span>Section {safe_section}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if progress is not None:
            progress_value = max(0, min(100, int(progress)))
            st.markdown(
                f"""
                <div class="student-subject-progress-row">
                    <div class="student-subject-progress-label">Attendance</div>
                    <div class="student-subject-progress-value">{progress_value}%</div>
                </div>
                <div class="student-subject-progress-track">
                    <div class="student-subject-progress-fill" style="width:{progress_value}%;"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if stats:
            stat_cols = st.columns(len(stats), gap="small")
            for col, (_, label, value) in zip(stat_cols, stats):
                with col:
                    st.markdown(
                        f"""
                        <div class="student-subject-stat">
                            <div class="student-subject-stat-value">{html.escape(str(value))}</div>
                            <div class="student-subject-stat-label">{html.escape(str(label))}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        if footer_callback:
            footer_callback()
