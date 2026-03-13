from fastapi import FastAPI 
from app.api.router import api_router

app = FastAPI(title="Polyglot API" , description="API for extracting subtitles and audio from YouTube videos" , version="1.0.0")

app.include_router(api_router)