"""Helpers for decoding base64 image payloads from the frontend."""

import base64
import binascii
import io

import numpy as np
from PIL import Image


class ImageDecodeError(ValueError):
    pass


def decode_base64_image(data: str) -> np.ndarray:
    """Decode a base64 (optionally data-URL prefixed) image into an RGB numpy array."""
    if "," in data[:64]:  # strip data URL prefix like "data:image/jpeg;base64,"
        data = data.split(",", 1)[1]

    try:
        raw = base64.b64decode(data, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ImageDecodeError("Invalid base64 image data") from exc

    try:
        image = Image.open(io.BytesIO(raw))
        return np.array(image.convert("RGB"))
    except Exception as exc:
        raise ImageDecodeError("Could not read image file") from exc
