from dotenv import load_dotenv
import redis, os
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import URL 
from app.db import get_db
from app.db import SessionLocal



load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
r = redis.from_url(REDIS_URL, decode_responses=True)

BASE = 62
CHARSET_DEFAULT = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"



def shortenurl(url:str,db: Session):
    url = url.strip()
    key = f"long_url:{url}"
    cached = r.get(key)
    if cached:
         return cached
    item = URL(original_url=url)
    db.add(item)
    db.commit()
    db.refresh(item)  
    short_code = encode(item.id)
    item.short_code = short_code
    db.add(item)
    db.commit()

    short_url = f"http://localhost:8000/{short_code}"

    r.set(key, short_url)
    r.set(f"code:{short_code}", url)

    return short_url

def redirect_to_original(short_code: str,db: Session):
    key = f"code:{short_code}"
    cached = r.get(key)
    if cached:
        return cached
    item = db.execute(
        select(URL).where(URL.short_code == short_code)
    ).first()
    if not item:
        return None
    r.set(key, item.original_url)

    return item.original_url
    

def encode(n, charset=CHARSET_DEFAULT)  -> str:
        chs = []
        while n > 0:
            n, rem = divmod(n, BASE)
            chs.insert(0, charset[rem])

        if not chs:
            return "0"

        return "".join(chs)   


