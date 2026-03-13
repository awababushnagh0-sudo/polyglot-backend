from fastapi import FastAPI 
from app.api.endpoints import subtitles , audio

app = FastAPI(title="Polyglot API" , description="API for extracting subtitles and audio from YouTube videos" , version="1.0.0")

app.include_router(subtitles.router)
app.include_router(audio.router)