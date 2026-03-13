from pydantic import BaseModel
from typing import List

class SubtitleSegment(BaseModel):
    start: float
    end: float
    text: str

class SubtitleRequest(BaseModel):
    segments: List[SubtitleSegment]
    target_lang: str = "ar"  