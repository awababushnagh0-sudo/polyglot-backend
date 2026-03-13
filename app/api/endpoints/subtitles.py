from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
# from app.services.youtube_service import trancribe_audio_to_json , download_audio
from app.services.subtitle_services import SubtitleServices
from app.services.audio_services import AudioServices


router = APIRouter()

@router.get("/subtitles", status_code=200 , description="Generate AI subtitles from YouTube using Whisper")
async def get_subtitles(url: str = Query(..., description="Youtube video URl")):
    try:
        audio_file = AudioServices.download_audio(url)
        subtitles = SubtitleServices.transcribe_audio_to_json(audio_file)
        return JSONResponse(content=subtitles)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio download failed: {str(e)}")

    


