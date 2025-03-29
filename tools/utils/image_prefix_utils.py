MIME_TYPE_TO_PREFIX = {
    "image/png": "data:image/png;base64",
    "image/jpeg": "data:image/jpeg;base64",
    "image/gif": "data:image/gif;base64",
    "image/webp": "data:image/webp;base64",
    "image/svg+xml": "data:image/svg+xml;base64"
}

PREFIX_TO_MIME_TYPE = {v: k for k, v in MIME_TYPE_TO_PREFIX.items()}
