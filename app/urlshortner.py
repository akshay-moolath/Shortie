import redis, os
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import URL
from urllib.parse import urlparse, urlunparse

REDIS_URL = os.getenv("REDIS_URL")
BASE_HOST = os.getenv("BASE_HOST", "http://127.0.0.1:8000").rstrip("/")
r = redis.from_url(REDIS_URL, decode_responses=True)

BASE = 62
CHARSET_DEFAULT = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Change this to a large random integer and keep it constant
SECRET_KEY = 1234567


def shortenurl(url: str, db: Session):
    url = normalize_url(url)

    key = f"long_url:{url}"
    cached = r.get(key)
    if cached:
        return cached

    existing = db.execute(
        select(URL).where(URL.original_url == url)
    ).scalar_one_or_none()

    if existing:
        short_url = f"{BASE_HOST}/{existing.short_code}"
        r.set(key, short_url)
        return short_url

    item = URL(original_url=url)
    db.add(item)
    db.commit()
    db.refresh(item)

    if item.id is None:
        raise RuntimeError("Failed to create URL record")

    # Obfuscate ID before encoding
    item.short_code = encode(item.id ^ SECRET_KEY)

    db.commit()

    short_url = f"{BASE_HOST}/{item.short_code}"

    r.set(key, short_url)
    r.set(f"code:{item.short_code}", url)

    return short_url


def redirect_to_original(short_code: str, db: Session):
    key = f"code:{short_code}"

    cached = r.get(key)
    if cached:
        return cached

    item = db.execute(
        select(URL).where(URL.short_code == short_code)
    ).scalar_one_or_none()

    if not item:
        return None

    r.set(key, item.original_url)

    return item.original_url


def encode(n, charset=CHARSET_DEFAULT):
    chs = []

    while n > 0:
        n, rem = divmod(n, BASE)
        chs.insert(0, charset[rem])

    if not chs:
        return "0"

    return "".join(chs)


def normalize_url(url: str):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    if netloc.startswith("www."):
        netloc = netloc[4:]

    path = parsed.path.rstrip("/")

    return urlunparse((scheme, netloc, path, "", "", ""))
