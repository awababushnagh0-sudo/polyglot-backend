from fastapi import APIRouter
from app.api.endpoints import subtitles, audio, translate

api_router = APIRouter()
api_router.include_router(subtitles.router, prefix="/subtitles", tags=["Subtitles"])
api_router.include_router(audio.router, prefix="/audio", tags=["Audio"])
api_router.include_router(translate.router, prefix="/translate", tags=["Translate"])