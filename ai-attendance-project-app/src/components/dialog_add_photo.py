import hashlib
from src.ui.dialog_styles import apply_dialog_styles

import streamlit as st
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    apply_dialog_styles()
    st.write("Add classroom photos to scan for attendance.")

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "attendance_image_keys" not in st.session_state:
        st.session_state.attendance_image_keys = set()

    if "attendance_input_version" not in st.session_state:
        st.session_state.attendance_input_version = 0

    input_version = st.session_state.attendance_input_version

    tab_camera, tab_upload = st.columns(2)

    with tab_camera:
        camera_type = (
            "primary"
            if st.session_state.photo_tab == "camera"
            else "tertiary"
        )
        if st.button(
            "Camera",
            type=camera_type,
            width="stretch",
            key="photo_tab_camera",
        ):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with tab_upload:
        upload_type = (
            "primary"
            if st.session_state.photo_tab == "upload"
            else "tertiary"
        )
        if st.button(
            "Upload photos",
            type=upload_type,
            width="stretch",
            key="photo_tab_upload",
        ):
            st.session_state.photo_tab = "upload"
            st.rerun()

    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input(
            "Take Snapshot",
            key=f"dialog_cam_{input_version}",
        )

        if cam_photo:
            photo_bytes = cam_photo.getvalue()
            photo_key = hashlib.sha256(photo_bytes).hexdigest()

            if photo_key not in st.session_state.attendance_image_keys:
                st.session_state.attendance_images.append(
                    Image.open(cam_photo).convert("RGB")
                )
                st.session_state.attendance_image_keys.add(photo_key)
                st.session_state.attendance_input_version += 1
                st.toast("Photo captured.")
                st.rerun()

    else:
        uploaded_files = st.file_uploader(
            "Choose image files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key=f"dialog_upload_{input_version}",
        )

        if uploaded_files:
            added_count = 0

            for uploaded_file in uploaded_files:
                photo_bytes = uploaded_file.getvalue()
                photo_key = hashlib.sha256(photo_bytes).hexdigest()

                if photo_key in st.session_state.attendance_image_keys:
                    continue

                st.session_state.attendance_images.append(
                    Image.open(uploaded_file).convert("RGB")
                )
                st.session_state.attendance_image_keys.add(photo_key)
                added_count += 1

            if added_count:
                st.session_state.attendance_input_version += 1
                st.toast(f"Added {added_count} photo(s).")
                st.rerun()

    st.divider()

    if st.button(
        "Done",
        type="primary",
        width="stretch",
        key="photo_dialog_done",
    ):
        st.rerun()
