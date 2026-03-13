from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.services.audio_services import youtube_download_audio 

router = APIRouter()    

@router.get("/audio", status_code=200)
def get_audio(url: str, lang: str = Query("en", description="Language code for the audio (default: 'en')")):
    try:
        audio_path = youtube_download_audio(url, lang)
        return FileResponse(audio_path, media_type="audio/mpeg", filename=audio_path.split("/")[-1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))