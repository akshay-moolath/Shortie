from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse,RedirectResponse
from app.db import Base, engine
from app.routers.urlshortner  import router as url_router
from sqlalchemy.orm import Session
from app.db import get_db
from app.routers.urlshortner import shortenurl, redirect_to_original


app =  FastAPI()

app.include_router(url_router, prefix="/urlshortner")


Base.metadata.create_all(bind=engine)


@app.post("/shorten")
def shorten(url: str, db: Session = Depends(get_db)):
    return shortenurl(url, db)

@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    original = redirect_to_original(short_code, db)
    return RedirectResponse(original)

@app.get("/")# connecting static pages to url/endpoint
def home():
    return FileResponse("static/index.html")

@app.get("/urlshortner")
def home():
    pass
