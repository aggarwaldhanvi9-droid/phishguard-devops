import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login", "verify", "update", "secure", "account",
    "banking", "confirm", "free", "bonus", "signin", "paypal", "amazon"
]

def extract_features(url: str) -> list[float]:
    parsed = urlparse(url if "://" in url else f"http://{url}")
    hostname = parsed.hostname or ""

    url_length = float(len(url))
    dot_count = float(url.count("."))
    hyphen_count = float(url.count("-"))
    at_symbol = 1.0 if "@" in url else 0.0
    digit_count = float(sum(c.isdigit() for c in url))
    is_https = 1.0 if parsed.scheme == "https" else 0.0
    has_ip = 1.0 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname) else 0.0
    keyword_hits = float(sum(word in url.lower() for word in SUSPICIOUS_WORDS))

    return [
        url_length,
        dot_count,
        hyphen_count,
        at_symbol,
        digit_count,
        is_https,
        has_ip,
        keyword_hits,
    ]