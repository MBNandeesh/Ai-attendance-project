import streamlit as st
import time
import html
import numpy as np

from datetime import datetime, timezone

from PIL import Image

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout,
)
from src.ui.premium_ui import apply_premium_ui, auth_brand_panel
from src.ui.dialog_styles import apply_dialog_styles

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier,
    find_duplicate_face,
)

from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
    update_student_face_embeddings,
)

from src.components.dialog_enroll import enroll_dialog


@st.dialog("Add Face Samples")
def add_face_samples_dialog(student_id):
    apply_dialog_styles()
    st.write(
        "Add a few different face samples to improve recognition "
        "across distance, lighting, and small changes in angle."
    )

    sample_images = []
    col1, col2 = st.columns(2)

    with col1:
        photo1 = st.camera_input(
            "Sample 1",
            key=f"face_sample_1_{student_id}",
        )

    with col2:
        photo2 = st.camera_input(
            "Sample 2",
            key=f"face_sample_2_{student_id}",
        )

    photo3 = st.camera_input(
        "Sample 3",
        key=f"face_sample_3_{student_id}",
    )

    for photo in (photo1, photo2, photo3):
        if photo:
            sample_images.append(photo)

    if st.button(
        "Save Face Samples",
        type="primary",
        width="stretch",
        disabled=not sample_images,
        key=f"save_face_samples_{student_id}",
    ):
        new_embeddings = []

        with st.spinner("Processing face samples..."):
            for photo in sample_images:
                image_np = np.array(
                    Image.open(photo).convert("RGB")
                )

                encodings = get_face_embeddings(image_np)

                if not encodings:
                    st.error(
                        "One of the samples does not contain a face. "
                        "Please capture it again."
                    )
                    return

                if len(encodings) > 1:
                    st.error(
                        "One of the samples contains multiple faces. "
                        "Please capture only your face."
                    )
                    return

                new_embeddings.append(encodings[0].tolist())

            current_student = next(
                (
                    student
                    for student in get_all_students()
                    if student.get("student_id") == student_id
                ),
                None,
            )

            if not current_student:
                st.error("Student profile could not be found.")
                return

            existing_embedding = current_student.get("face_embedding")

            if existing_embedding is None:
                all_embeddings = new_embeddings
            else:
                existing_array = np.asarray(existing_embedding, dtype=float)

                if (
                    existing_array.ndim == 1
                    and existing_array.shape[0] == 128
                ):
                    all_embeddings = [existing_array.tolist()] + new_embeddings
                elif (
                    existing_array.ndim == 2
                    and existing_array.shape[1] == 128
                ):
                    all_embeddings = existing_array.tolist() + new_embeddings
                else:
                    st.error("Existing face data has an invalid format.")
                    return

            response = update_student_face_embeddings(
                student_id,
                all_embeddings,
            )

            if response:
                train_classifier()
                st.success(
                    f"Saved {len(new_embeddings)} new face sample(s)."
                )
                time.sleep(1)
                st.rerun()
            else:
                st.error("Could not save the new face samples.")


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    student_name = html.escape(str(student_data.get("name", "Student")))

    face_embedding = student_data.get("face_embedding")
    if face_embedding is None:
        face_sample_count = 0
    else:
        face_array = np.asarray(face_embedding)
        face_sample_count = 1 if face_array.ndim == 1 else len(face_array)

    with st.container(key="student-dashboard-shell"):
        with st.spinner("Loading your attendance workspace..."):
            subjects = get_student_subjects(student_id) or []
            logs = get_student_attendance(student_id) or []

        total_classes = len(
            {
                str(log.get("timestamp"))
                for log in logs
                if isinstance(log, dict) and log.get("timestamp")
            }
        )
        present_entries = sum(
            1
            for log in logs
            if isinstance(log, dict) and bool(log.get("is_present"))
        )
        attendance_rate = (
            round((present_entries / len(logs)) * 100)
            if logs
            else 0
        )

        parsed_log_times = []
        for log in logs:
            raw_timestamp = log.get("timestamp") if isinstance(log, dict) else None
            if not raw_timestamp:
                continue
            try:
                parsed = datetime.fromisoformat(
                    str(raw_timestamp).replace("Z", "+00:00")
                )
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                parsed_log_times.append(parsed)
            except (TypeError, ValueError):
                continue

        latest_update_text = (
            max(parsed_log_times).astimezone().strftime("%d %b %Y, %I:%M %p")
            if parsed_log_times
            else "No attendance sessions yet"
        )

        enrolled_count = len(
            [
                node
                for node in subjects
                if isinstance(node, dict)
                and isinstance(node.get("subjects"), dict)
            ]
        )

        header_dashboard()

        st.markdown(
            f"""
            <section class="student-welcome">
                <div>
                    <div class="student-eyebrow">STUDENT WORKSPACE</div>
                    <div class="student-welcome-title">Welcome back, {student_name}</div>
                    <div class="student-welcome-copy">
                        Stay on top of your attendance, subjects, and face profile.
                    </div>
                </div>
                <div>
                    <div class="student-status-pill">
                        <span class="student-status-dot"></span>
                        AI profile active
                    </div>
                    <div class="student-status-meta">
                        {face_sample_count} face sample{"s" if face_sample_count == 1 else "s"}
                        · Latest update: {latest_update_text}
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="student-stat-grid">
                <div class="student-stat-card">
                    <div class="student-stat-label">Enrolled Subjects</div>
                    <div class="student-stat-value">{enrolled_count}</div>
                    <div class="student-stat-note">Active courses</div>
                </div>
                <div class="student-stat-card">
                    <div class="student-stat-label">Classes Recorded</div>
                    <div class="student-stat-value">{total_classes}</div>
                    <div class="student-stat-note">Confirmed sessions</div>
                </div>
                <div class="student-stat-card">
                    <div class="student-stat-label">Present Marks</div>
                    <div class="student-stat-value">{present_entries}</div>
                    <div class="student-stat-note">Sessions marked present</div>
                </div>
                <div class="student-stat-card student-stat-card-accent">
                    <div class="student-stat-label">Attendance Rate</div>
                    <div class="student-stat-value">{attendance_rate}%</div>
                    <div class="student-stat-note">Across recorded sessions</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        action_left, action_right = st.columns(2, gap="small")
        with action_left:
            if st.button(
                "Enroll in Subject",
                type="primary",
                width="stretch",
                icon=":material/add_circle:",
                key="student_enroll_subject",
            ):
                enroll_dialog()

        with action_right:
            if st.button(
                "Add Face Samples",
                type="secondary",
                width="stretch",
                icon=":material/face:",
                key="student_add_face_samples",
            ):
                add_face_samples_dialog(student_id)

        st.markdown(
            """
            <div class="student-section-heading">
                <div>
                    <div class="student-section-kicker">YOUR ACADEMICS</div>
                    <div class="student-section-title">Enrolled Subjects</div>
                </div>
                <div class="student-section-copy">
                    Track each course at a glance. Attendance updates after a teacher confirms the session.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        stats_map = {}
        for log in logs:
            if not isinstance(log, dict) or log.get("subject_id") is None:
                continue

            subject_id = log["subject_id"]
            stats_map.setdefault(
                subject_id,
                {"total": 0, "attended": 0},
            )
            stats_map[subject_id]["total"] += 1
            if log.get("is_present"):
                stats_map[subject_id]["attended"] += 1

        valid_subjects = [
            node
            for node in subjects
            if isinstance(node, dict)
            and isinstance(node.get("subjects"), dict)
        ]

        if not valid_subjects:
            st.markdown(
                """
                <div class="student-empty-state">
                    <div class="student-empty-icon">+</div>
                    <div class="student-empty-title">No subjects enrolled yet</div>
                    <div class="student-empty-copy">
                        Use your teacher's subject code to add your first course.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            cols = st.columns(2, gap="large")

            for i, sub_node in enumerate(valid_subjects):
                sub = sub_node["subjects"]
                subject_id = sub.get("subject_id")
                if subject_id is None:
                    continue

                stats = stats_map.get(
                    subject_id,
                    {"total": 0, "attended": 0},
                )

                def unenroll_button(
                    subject_id=subject_id,
                    subject_name=sub.get("name", "this subject"),
                ):
                    if st.button(
                        "Unenroll from this course",
                        type="tertiary",
                        width="stretch",
                        icon=":material/delete_forever:",
                        key=f"unenroll_{student_id}_{subject_id}",
                    ):
                        try:
                            unenroll_student_to_subject(
                                student_id,
                                subject_id,
                            )
                            st.toast(
                                f"Unenrolled from {subject_name} successfully."
                            )
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Failed to unenroll: {exc}")

                with cols[i % 2]:
                    subject_card(
                        name=sub.get("name", "Unknown subject"),
                        code=sub.get("subject_code", "Unknown"),
                        section=sub.get("section", "-"),
                        stats=[
                            ("", "Classes", stats["total"]),
                            ("", "Present", stats["attended"]),
                        ],
                        progress=(
                            round((stats["attended"] / stats["total"]) * 100)
                            if stats["total"]
                            else 0
                        ),
                        footer_callback=unenroll_button,
                    )

    footer_dashboard()

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        apply_premium_ui()
        return

    with st.container(key="student-auth-layout"):
        col_left, col_right = st.columns(
            [1.08, 0.92],
            vertical_alignment="center",
            gap="large",
        )

        with col_left:
            st.markdown(auth_brand_panel("student"), unsafe_allow_html=True)

        with col_right:
            with st.container(border=True, key="student-auth-card"):
                if st.button(
                    "Back to Home",
                    type="tertiary",
                    key="student_login_back",
                    shortcut="control+backspace",
                    icon=":material/arrow_back:",
                ):
                    st.session_state["login_type"] = None
                    st.rerun()

                st.header("WELCOME BACK")
                st.markdown(
                    "<div style='color:#5E6A82;font-size:16px;font-weight:650;margin-bottom:1rem;'>"
                    "Login to AI Attendance · Continue with Face ID"
                    "</div>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    "<div style='font-size:14px;font-weight:850;color:#1A1B41;margin:.25rem 0 .45rem;'>"
                    "Live Face Recognition"
                    "</div>",
                    unsafe_allow_html=True,
                )

                show_registration = False
                photo_source = st.camera_input(
                    "Position your face in the center",
                    key="student_face_login_camera",
                )

                if photo_source:
                    img = np.array(Image.open(photo_source).convert("RGB"))

                    with st.spinner("AI is scanning..."):
                        detected, _, num_faces = predict_attendance(img)

                        if num_faces == 0:
                            st.warning(
                                "Face not found. Please position your face clearly."
                            )
                        elif num_faces > 1:
                            st.warning(
                                "Multiple faces found. Please capture only your face."
                            )
                        elif detected:
                            student_id = list(detected.keys())[0]
                            all_students = get_all_students() or []

                            student = next(
                                (
                                    student
                                    for student in all_students
                                    if student.get("student_id") == student_id
                                ),
                                None,
                            )

                            if student:
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = student
                                st.session_state.login_type = "student"
                                st.toast(f"Welcome back, {student['name']}!")
                                time.sleep(0.8)
                                st.rerun()
                            else:
                                st.error("Recognized student profile could not be loaded.")
                        else:
                            st.info(
                                "Face not recognized. You might be a new student."
                            )
                            show_registration = True

                if show_registration:
                    st.markdown(
                        "<div style='margin-top:1.1rem;padding-top:1rem;border-top:1px solid #E8EDF2;'>"
                        "<div style='font-size:22px;font-weight:900;color:#1A1B41;'>Register New Profile</div>"
                        "<div style='font-size:15px;color:#5E6A82;margin-top:4px;'>Create your profile after an unrecognized face.</div>"
                        "</div>",
                        unsafe_allow_html=True,
                    )

                    new_name = st.text_input(
                        "Enter your name",
                        placeholder="Your full name",
                        key="new_student_name",
                    )

                    st.subheader("Optional: Voice Enrollment")
                    st.info("Enroll your voice for voice-only attendance.")

                    audio_data = None
                    try:
                        audio_data = st.audio_input(
                            "Record a short phrase like "
                            "I am present, My name is Akash.",
                            key="new_student_voice",
                        )
                    except Exception as exc:
                        st.error(f"Audio input failed to load: {exc}")

                    if st.button(
                        "Create Account",
                        type="primary",
                        width="stretch",
                        key="create_student_account",
                    ):
                        if not new_name.strip():
                            st.warning("Please enter your name.")
                            return

                        if not photo_source:
                            st.warning("Please capture a photo first.")
                            return

                        with st.spinner("Creating profile..."):
                            img = np.array(
                                Image.open(photo_source).convert("RGB")
                            )
                            encodings = get_face_embeddings(img)

                            if not encodings:
                                st.error(
                                    "Could not detect a face. "
                                    "Please capture a clear photo of your face."
                                )
                                return

                            if len(encodings) > 1:
                                st.error(
                                    "Multiple faces detected. "
                                    "Please capture a photo containing only your face."
                                )
                                return

                            duplicate_student_id, duplicate_distance = find_duplicate_face(
                                encodings[0]
                            )

                            if duplicate_student_id is not None:
                                existing_students = get_all_students() or []
                                existing_student = next(
                                    (
                                        student
                                        for student in existing_students
                                        if student.get("student_id") == duplicate_student_id
                                    ),
                                    None,
                                )
                                existing_name = (
                                    existing_student.get("name", "an existing profile")
                                    if existing_student
                                    else "an existing profile"
                                )

                                st.warning(
                                    f"This face is already registered as {existing_name}. "
                                    "Use Face ID login instead of creating another profile."
                                )
                                return

                            # Store face embeddings in one canonical format:
                            # a list of 128-D samples, even when there is only one sample.
                            face_emb = [encodings[0].tolist()]
                            voice_emb = None

                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(
                                new_name.strip(),
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]
                                st.session_state.login_type = "student"
                                st.toast(
                                    f"Profile created successfully. Hi {new_name.strip()}!"
                                )
                                time.sleep(0.8)
                                st.rerun()
                            else:
                                st.error("Profile creation failed. Please try again.")

    footer_dashboard()
    apply_premium_ui()
