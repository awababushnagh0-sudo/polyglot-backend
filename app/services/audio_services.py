from app.services.youtube_service import download_audio as youtube_download_audio

class AudioServices:
    @staticmethod
    def download_audio(url: str, lang: str = "en") -> str:
        return youtube_download_audio(url, lang)