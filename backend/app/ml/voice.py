"""Voice speaker-recognition pipeline (ported from the Streamlit prototype).

librosa/resemblyzer are imported lazily so the module (and its pure-numpy
matching logic) loads even without the heavy ML deps installed.
"""

import io
import json

import numpy as np

VOICE_MATCH_THRESHOLD = 0.65
MIN_SEGMENT_SECONDS = 0.5
VAD_TOP_DB = 30

_encoder = None


class MLDependencyError(RuntimeError):
    """Raised when voice ML is used without its heavy dependencies installed."""


def _lazy_import_voice():
    try:
        import librosa
        from resemblyzer import VoiceEncoder, preprocess_wav

        return librosa, VoiceEncoder, preprocess_wav
    except ImportError as exc:
        raise MLDependencyError(
            "Voice dependencies are not installed. Run: pip install -e '.[ml]'"
        ) from exc


def _get_encoder():
    global _encoder
    if _encoder is None:
        _, VoiceEncoder, _ = _lazy_import_voice()
        _encoder = VoiceEncoder()
    return _encoder


def embed_audio_bytes(audio_bytes: bytes) -> np.ndarray | None:
    """Embed a single utterance from raw audio bytes (any librosa-readable format)."""
    try:
        librosa, _, preprocess_wav = _lazy_import_voice()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        return _get_encoder().embed_utterance(wav)
    except MLDependencyError:
        raise
    except Exception:
        return None


def normalize_voice_embeddings(raw) -> np.ndarray:
    """Convert stored JSON (list or list-of-lists) to an (N, D) matrix."""
    if raw is None:
        return np.empty((0, 256))
    try:
        arr = np.asarray(json.loads(raw) if isinstance(raw, str) else raw, dtype=float)
    except (ValueError, TypeError):
        return np.empty((0, 256))
    if arr.ndim == 1:
        return arr.reshape(1, -1)
    return arr if arr.ndim == 2 else np.empty((0, 256))


def identify_speaker(
    query: np.ndarray,
    known: dict[int, np.ndarray],
    threshold: float = VOICE_MATCH_THRESHOLD,
) -> tuple[int | None, float]:
    """Best cosine-similarity match above threshold. Returns (student_id, score)."""
    if query is None or not known:
        return None, 0.0

    best_id, best_score = None, -1.0
    for student_id, matrix in known.items():
        sims = matrix @ query  # cosine similarity (embeddings are L2-normalized)
        s = float(sims.max())
        if s > best_score:
            best_score, best_id = s, student_id

    return (best_id, best_score) if best_score >= threshold else (None, best_score)


def process_bulk_audio(
    audio_bytes: bytes,
    known: dict[int, np.ndarray],
    threshold: float = VOICE_MATCH_THRESHOLD,
) -> dict[int, float]:
    """
    Split classroom audio into speech segments and identify speakers.

    Returns {student_id: best_similarity} for everyone identified.
    """
    try:
        librosa, _, preprocess_wav = _lazy_import_voice()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
    except MLDependencyError:
        raise
    except Exception:
        return {}

    encoder = _get_encoder()
    segments = librosa.effects.split(audio, top_db=VAD_TOP_DB)

    identified: dict[int, float] = {}
    for start, end in segments:
        if (end - start) < sr * MIN_SEGMENT_SECONDS:
            continue

        try:
            wav = preprocess_wav(audio[start:end])
            embedding = encoder.embed_utterance(wav)
        except Exception:
            continue

        sid, score = identify_speaker(embedding, known, threshold)
        if sid is not None and score > identified.get(sid, -1.0):
            identified[sid] = score

    return identified
