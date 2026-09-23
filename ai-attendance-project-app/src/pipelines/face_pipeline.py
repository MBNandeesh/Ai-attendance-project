import dlib
import numpy as np
import face_recognition_models
import streamlit as st

from src.database.db import get_all_students


FACE_DETECTOR_UPSAMPLE = 2
FACE_DETECTOR_FALLBACK_UPSAMPLE = 3
FACE_MATCH_THRESHOLD = 0.55
FACE_MATCH_MARGIN = 0.10
FACE_DUPLICATE_THRESHOLD = 0.40
FACE_DESCRIPTOR_JITTERS = 3
FACE_MIN_WIDTH_RATIO = 0.04
FACE_MIN_HEIGHT_RATIO = 0.04


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def _rectangle_iou(rect_a, rect_b):
    left = max(rect_a.left(), rect_b.left())
    top = max(rect_a.top(), rect_b.top())
    right = min(rect_a.right(), rect_b.right())
    bottom = min(rect_a.bottom(), rect_b.bottom())

    intersection_width = max(0, right - left + 1)
    intersection_height = max(0, bottom - top + 1)
    intersection_area = intersection_width * intersection_height

    area_a = max(0, rect_a.right() - rect_a.left() + 1) * max(
        0, rect_a.bottom() - rect_a.top() + 1
    )
    area_b = max(0, rect_b.right() - rect_b.left() + 1) * max(
        0, rect_b.bottom() - rect_b.top() + 1
    )

    union_area = area_a + area_b - intersection_area

    if union_area == 0:
        return 0.0

    return intersection_area / union_area


def _merge_face_rectangles(rectangles):
    merged = []

    rectangles = sorted(
        rectangles,
        key=lambda rect: rect.width() * rect.height(),
        reverse=True
    )

    for rectangle in rectangles:
        duplicate = any(
            _rectangle_iou(rectangle, existing) >= 0.50
            for existing in merged
        )

        if not duplicate:
            merged.append(rectangle)

    return merged


def _detect_face_rectangles(image_np):
    detector, _, _ = load_dlib_models()

    image_height, image_width = image_np.shape[:2]

    rectangles = list(
        detector(image_np, FACE_DETECTOR_UPSAMPLE)
    )

    fallback_rectangles = list(
        detector(image_np, FACE_DETECTOR_FALLBACK_UPSAMPLE)
    )

    rectangles.extend(fallback_rectangles)

    flipped = np.ascontiguousarray(np.fliplr(image_np))

    flipped_rectangles = detector(
        flipped,
        FACE_DETECTOR_UPSAMPLE
    )

    for rectangle in flipped_rectangles:
        mapped_left = image_width - 1 - rectangle.right()
        mapped_right = image_width - 1 - rectangle.left()

        rectangles.append(
            dlib.rectangle(
                mapped_left,
                rectangle.top(),
                mapped_right,
                rectangle.bottom()
            )
        )

    rectangles = _merge_face_rectangles(rectangles)
    rectangles.sort(key=lambda rect: (rect.left(), rect.top()))

    valid_rectangles = []

    minimum_width = max(32, int(image_width * FACE_MIN_WIDTH_RATIO))
    minimum_height = max(32, int(image_height * FACE_MIN_HEIGHT_RATIO))

    for rectangle in rectangles:
        left = max(0, rectangle.left())
        top = max(0, rectangle.top())
        right = min(image_width - 1, rectangle.right())
        bottom = min(image_height - 1, rectangle.bottom())

        if right <= left or bottom <= top:
            continue

        face_width = right - left + 1
        face_height = bottom - top + 1

        # Very small detections do not contain enough facial detail for
        # reliable recognition, so ignore them instead of guessing.
        if face_width < minimum_width or face_height < minimum_height:
            continue

        valid_rectangles.append(
            dlib.rectangle(left, top, right, bottom)
        )

    return valid_rectangles


def get_face_embeddings(image_np):
    _, sp, facerec = load_dlib_models()

    faces = _detect_face_rectangles(image_np)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)

        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            FACE_DESCRIPTOR_JITTERS
        )

        encodings.append(np.array(face_descriptor))

    return encodings


def _normalize_student_embeddings(embedding):
    """Return one or more 128-D embeddings from database JSON."""
    if embedding is None:
        return []

    array = np.asarray(embedding, dtype=float)

    if array.ndim == 1:
        if array.shape[0] != 128:
            return []
        return [array]

    if array.ndim == 2 and array.shape[1] == 128:
        return [row for row in array]

    return []


def get_trained_model():
    """
    Load the current face database on every recognition call.

    Face profiles can be created/updated while the app is running, so caching
    this database snapshot can make newly enrolled students invisible until a
    full cache refresh.
    """
    student_db = get_all_students() or []

    if not student_db:
        return None

    student_embeddings = {}

    for student in student_db:
        embedding = student.get("face_embedding")
        student_id = student.get("student_id")

        if embedding is None or student_id is None:
            continue

        embeddings = _normalize_student_embeddings(embedding)

        if embeddings:
            student_embeddings[int(student_id)] = embeddings

    if not student_embeddings:
        return None

    return {
        "student_embeddings": student_embeddings,
        "all_students": sorted(student_embeddings.keys())
    }


def train_classifier():
    """
    Compatibility hook for registration/face-sample flows.

    The student embedding database is intentionally not cached, so the next
    recognition call automatically sees the latest Supabase data.
    """
    return bool(get_trained_model())


def find_duplicate_face(new_embedding, threshold=FACE_DUPLICATE_THRESHOLD):
    """
    Check whether a newly captured face is already represented in the DB.

    Returns (student_id, distance) for the closest existing student when the
    distance is below the duplicate threshold; otherwise returns (None, best_distance).
    """
    if new_embedding is None:
        return None, None

    query = np.asarray(new_embedding, dtype=float)

    if query.shape != (128,):
        return None, None

    best_student_id = None
    best_distance = float("inf")

    for student in get_all_students() or []:
        student_id = student.get("student_id")
        if student_id is None:
            continue

        for stored_embedding in _normalize_student_embeddings(
            student.get("face_embedding")
        ):
            distance = float(np.linalg.norm(stored_embedding - query))

            if distance < best_distance:
                best_distance = distance
                best_student_id = int(student_id)

    if best_student_id is not None and best_distance <= threshold:
        return best_student_id, best_distance

    return None, best_distance


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_student = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)

    student_embeddings = model_data["student_embeddings"]
    all_students = model_data["all_students"]

    for encoding in encodings:

        student_distances = []

        for student_id, embeddings in student_embeddings.items():
            best_student_distance = min(
                float(np.linalg.norm(embedding - encoding))
                for embedding in embeddings
            )

            student_distances.append(
                (student_id, best_student_distance)
            )

        if not student_distances:
            continue

        student_distances.sort(key=lambda item: item[1])

        best_student_id, best_distance = student_distances[0]

        if len(student_distances) >= 2:
            second_best_distance = student_distances[1][1]
            match_margin = second_best_distance - best_distance
        else:
            match_margin = float("inf")

        is_good_distance = best_distance <= FACE_MATCH_THRESHOLD
        is_clear_match = match_margin >= FACE_MATCH_MARGIN

        if is_good_distance and is_clear_match:
            detected_student[best_student_id] = True

    return detected_student, all_students, len(encodings)
