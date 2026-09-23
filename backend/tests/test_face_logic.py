import numpy as np

from app.ml.face import find_duplicate_face, identify_faces_single, normalize_embeddings


def _matrix(rows):
    return np.array(rows, dtype=float)


def test_normalize_single_vector():
    m = normalize_embeddings([0.1] * 128)
    assert m.shape == (1, 128)


def test_normalize_matrix():
    m = normalize_embeddings([[0.1] * 128, [0.2] * 128])
    assert m.shape == (2, 128)


def test_normalize_rejects_wrong_dims():
    assert normalize_embeddings([0.1] * 100).shape[0] == 0
    assert normalize_embeddings(None).shape[0] == 0


def test_identify_single_match():
    anchor = np.array([1.0] * 128)
    known = {1: _matrix([anchor]), 2: _matrix([[0.0] * 128])}
    # query close to student 1
    query = anchor + np.full(128, 0.01)
    assert identify_faces_single(query, known) == 1


def test_identify_rejects_far_query():
    anchor = np.array([1.0] * 128)
    known = {1: _matrix([anchor])}
    query = np.array([-1.0] * 128)  # distance ~ sqrt(4*128) >> threshold
    assert identify_faces_single(query, known) is None


def test_identify_requires_margin_over_second_best():
    """Ambiguous query (close to two students) must not match either."""
    anchor = np.array([1.0] * 128)
    known = {1: _matrix([anchor]), 2: _matrix([anchor + np.full(128, 0.02)])}
    query = anchor + np.full(128, 0.01)  # nearly equidistant
    assert identify_faces_single(query, known) is None


def test_identify_uses_best_of_multiple_samples():
    anchor = np.array([1.0] * 128)
    other = np.array([-1.0] * 128)
    known = {1: _matrix([other, anchor])}  # second sample is the good one
    query = anchor + np.full(128, 0.01)
    assert identify_faces_single(query, known) == 1


def test_duplicate_detection():
    anchor = np.array([1.0] * 128)
    known = {7: _matrix([anchor])}
    dup_id, dist = find_duplicate_face(anchor + np.full(128, 0.001), known)
    assert dup_id == 7
    assert dist is not None and dist < 0.1


def test_no_duplicate_for_distinct_face():
    anchor = np.array([1.0] * 128)
    other = np.array([-1.0] * 128)
    known = {7: _matrix([anchor])}
    dup_id, _ = find_duplicate_face(other, known)
    assert dup_id is None
