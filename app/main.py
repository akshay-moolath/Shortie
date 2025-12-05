from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse,RedirectResponse
from app.db import Base, engine
from sqlalchemy.orm import Session
from app.db import get_db
from app.routers.urlshortner import shortenurl, redirect_to_original
from fastapi.staticfiles import StaticFiles
from app.schemas import URLRequest



app =  FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)


@app.post("/shorten")
def shorten(request_data: URLRequest, db: Session = Depends(get_db)):
    return shortenurl(request_data.url, db)

@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    original = redirect_to_original(short_code, db)
    return RedirectResponse(original)

@app.get("/")# connecting static pages to url/endpoint
def home():
    return FileResponse("static/index.html")

@app.get("/favicon.ico")#added to remove favicon error
def favicon():
    return ""
