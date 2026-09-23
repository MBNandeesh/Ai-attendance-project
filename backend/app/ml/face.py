"""Face recognition pipeline (ported from the Streamlit prototype).

Key improvements over v1:
- Vectorized distance computation (numpy matrix ops instead of per-student loops)
- Embeddings stored per student as JSON lists of 128-D vectors
- Same proven detection strategy: multi-upsample + flipped-frame pass + IOU merge
"""

import dlib
import face_recognition_models
import numpy as np

# Tunables (same values proven in the Streamlit prototype)
FACE_DETECTOR_UPSAMPLE = 2
FACE_DETECTOR_FALLBACK_UPSAMPLE = 3
FACE_MATCH_THRESHOLD = 0.55
FACE_MATCH_MARGIN = 0.10
FACE_DUPLICATE_THRESHOLD = 0.40
FACE_DESCRIPTOR_JITTERS = 3
FACE_MIN_WIDTH_RATIO = 0.04
FACE_MIN_HEIGHT_RATIO = 0.04
IOU_MERGE_THRESHOLD = 0.50

_models = None


def _get_models():
    """Load dlib models once per process."""
    global _models
    if _models is None:
        detector = dlib.get_frontal_face_detector()
        sp = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
        facerec = dlib.face_recognition_model_v1(
            face_recognition_models.face_recognition_model_location()
        )
        _models = (detector, sp, facerec)
    return _models


def _rectangle_iou(rect_a, rect_b) -> float:
    left = max(rect_a.left(), rect_b.left())
    top = max(rect_a.top(), rect_b.top())
    right = min(rect_a.right(), rect_b.right())
    bottom = min(rect_a.bottom(), rect_b.bottom())

    inter_w = max(0, right - left + 1)
    inter_h = max(0, bottom - top + 1)
    inter_area = inter_w * inter_h

    area_a = max(0, rect_a.right() - rect_a.left() + 1) * max(0, rect_a.bottom() - rect_a.top() + 1)
    area_b = max(0, rect_b.right() - rect_b.left() + 1) * max(0, rect_b.bottom() - rect_b.top() + 1)
    union = area_a + area_b - inter_area
    return inter_area / union if union else 0.0


def _merge_face_rectangles(rectangles):
    merged = []
    for rect in sorted(rectangles, key=lambda r: r.width() * r.height(), reverse=True):
        if not any(_rectangle_iou(rect, existing) >= IOU_MERGE_THRESHOLD for existing in merged):
            merged.append(rect)
    return merged


def detect_face_rectangles(image_np: np.ndarray):
    """Multi-pass detection: 2x upsample, 3x fallback, and flipped frame."""
    detector, _, _ = _get_models()
    image_height, image_width = image_np.shape[:2]

    rectangles = list(detector(image_np, FACE_DETECTOR_UPSAMPLE))
    rectangles.extend(detector(image_np, FACE_DETECTOR_FALLBACK_UPSAMPLE))

    flipped = np.ascontiguousarray(np.fliplr(image_np))
    for rect in detector(flipped, FACE_DETECTOR_UPSAMPLE):
        rectangles.append(
            dlib.rectangle(
                image_width - 1 - rect.right(),
                rect.top(),
                image_width - 1 - rect.left(),
                rect.bottom(),
            )
        )

    rectangles = _merge_face_rectangles(rectangles)
    rectangles.sort(key=lambda r: (r.left(), r.top()))

    min_w = max(32, int(image_width * FACE_MIN_WIDTH_RATIO))
    min_h = max(32, int(image_height * FACE_MIN_HEIGHT_RATIO))

    valid = []
    for rect in rectangles:
        left, top = max(0, rect.left()), max(0, rect.top())
        right, bottom = min(image_width - 1, rect.right()), min(image_height - 1, rect.bottom())
        if right <= left or bottom <= top:
            continue
        if (right - left + 1) < min_w or (bottom - top + 1) < min_h:
            continue  # too small to recognize reliably
        valid.append(dlib.rectangle(left, top, right, bottom))
    return valid


def get_face_embeddings(image_np: np.ndarray) -> list[np.ndarray]:
    """Detect faces in an image and return a 128-D descriptor per face."""
    _, sp, facerec = _get_models()

    encodings = []
    for face in detect_face_rectangles(image_np):
        shape = sp(image_np, face)
        descriptor = facerec.compute_face_descriptor(image_np, shape, FACE_DESCRIPTOR_JITTERS)
        encodings.append(np.array(descriptor))
    return encodings


def normalize_embeddings(raw) -> np.ndarray:
    """Convert stored JSON (list of 128-D lists, or a single list) to an (N, 128) matrix."""
    if raw is None:
        return np.empty((0, 128))
    arr = np.asarray(raw, dtype=float)
    if arr.ndim == 1 and arr.shape[0] == 128:
        return arr.reshape(1, 128)
    if arr.ndim == 2 and arr.shape[1] == 128:
        return arr
    return np.empty((0, 128))


def identify_faces(
    image_np: np.ndarray,
    known: dict[int, np.ndarray],
) -> list[dict]:
    """
    Recognize faces in an image against known embeddings.

    known: {student_id: (N_i, 128) matrix of that student's samples}
    Returns a list of {student_id, distance} for confident matches.
    """
    encodings = get_face_embeddings(image_np)
    results = []

    for encoding in encodings:
        best_id, best_dist, second_dist = None, float("inf"), float("inf")

        for student_id, matrix in known.items():
            distances = np.linalg.norm(matrix - encoding, axis=1)
            d = float(distances.min())
            if d < best_dist:
                second_dist = best_dist
                best_dist, best_id = d, student_id
            elif d < second_dist:
                second_dist = d

        if best_id is None:
            continue

        margin = second_dist - best_dist if second_dist != float("inf") else float("inf")
        if best_dist <= FACE_MATCH_THRESHOLD and margin >= FACE_MATCH_MARGIN:
            results.append({"student_id": best_id, "distance": best_dist})

    return results


def identify_faces_single(encoding: np.ndarray, known: dict[int, np.ndarray]) -> int | None:
    """Match one encoding against known embeddings; return the student_id or None.

    Requires both a good absolute distance AND a clear margin over the
    second-best candidate, exactly like the prototype's double check.
    """
    best_id, best_dist, second_dist = None, float("inf"), float("inf")

    for student_id, matrix in known.items():
        distances = np.linalg.norm(matrix - encoding, axis=1)
        d = float(distances.min())
        if d < best_dist:
            second_dist = best_dist
            best_dist, best_id = d, student_id
        elif d < second_dist:
            second_dist = d

    if best_id is None:
        return None

    margin = second_dist - best_dist if second_dist != float("inf") else float("inf")
    if best_dist <= FACE_MATCH_THRESHOLD and margin >= FACE_MATCH_MARGIN:
        return best_id
    return None


def find_duplicate_face(
    query: np.ndarray,
    known: dict[int, np.ndarray],
) -> tuple[int | None, float | None]:
    """Return (student_id, distance) of the closest existing profile within duplicate threshold."""
    if query is None or query.shape != (128,):
        return None, None

    best_id, best_dist = None, float("inf")
    for student_id, matrix in known.items():
        distances = np.linalg.norm(matrix - query, axis=1)
        d = float(distances.min())
        if d < best_dist:
            best_dist, best_id = d, student_id

    if best_id is not None and best_dist <= FACE_DUPLICATE_THRESHOLD:
        return best_id, best_dist
    return None, (best_dist if best_dist != float("inf") else None)
