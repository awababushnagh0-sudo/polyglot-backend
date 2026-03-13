from app.services.youtube_service import trancribe_audio_to_json as audio_to_json

class SubtitleServices:
    @staticmethod
    def transcribe_audio_to_json(audio_path: str):
        return audio_to_json(audio_path)