from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.services.youtube_service import trancribe_audio_to_json , download_audio

router = APIRouter()

@router.get("/subtitles", status_code=200 , description="Generate AI subtitles from YouTube using Whisper")
async def get_subtitles(url: str = Query(..., description="Youtube video URl")):
    try:
        audio_file = download_audio(url)
        subtitles = trancribe_audio_to_json(audio_file)
        return JSONResponse(content=subtitles)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio download failed: {str(e)}")

    


