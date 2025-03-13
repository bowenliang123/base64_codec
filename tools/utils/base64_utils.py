import base64
from functools import lru_cache

LRU_CACHE_SIZE = 128


@lru_cache(maxsize=LRU_CACHE_SIZE)
def encode_to_base64(plain_text: str, urlsafe_enabled: bool) -> str:
    plain_text_bytes = plain_text.encode("utf-8")
    if urlsafe_enabled:
        base64_encoded_bytes = base64.urlsafe_b64encode(plain_text_bytes)
    else:
        base64_encoded_bytes = base64.b64encode(plain_text_bytes)
    return base64_encoded_bytes.decode("utf-8")


@lru_cache(maxsize=LRU_CACHE_SIZE)
def decode_from_base64(encoded_text: str, urlsafe_enabled: bool) -> str:
    encoded_text_bytes = encoded_text.encode("utf-8")
    if urlsafe_enabled:
        decoded_bytes = base64.urlsafe_b64decode(encoded_text_bytes)
    else:
        decoded_bytes = base64.b64decode(encoded_text_bytes)
    return decoded_bytes.decode("utf-8")
