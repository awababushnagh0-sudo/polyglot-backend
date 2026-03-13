from app.services.youtube_service import ai_translate_segments as ai_traslate , Segments
from typing import List




class AiTranslateServices:
    @staticmethod
    def ai_translate_segments(segments: List[Segments] , lang: str = "eng"):
        return ai_traslate(segments , lang)
