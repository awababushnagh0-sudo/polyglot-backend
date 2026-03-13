from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from app.services.ai_translate_services import AiTranslateServices
from app.schemas.subtitle import SubtitleRequest

router = APIRouter()


@router.post("/translate", status_code=200)
def translate(subtitle_request: SubtitleRequest):
    try:
        translated_segments =  AiTranslateServices.ai_translate_segments(subtitle_request.segments, subtitle_request.target_lang)
        segments_list = json.loads(translated_segments.text)

        return {"segments": segments_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
