import subprocess
from pathlib import Path
from faster_whisper import WhisperModel
from fastapi import HTTPException
from typing import Optional

AUDIO_DIR = Path("media/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def _extract_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    return url.split("/")[-1]


def _build_command(url: str, client: str, skip_hls: bool, cookies_file: Optional[str] = None) -> list:
    fmt = (
        "bestaudio[protocol!=m3u8][protocol!=m3u8_native]/bestaudio/best"
        if skip_hls
        else "bestaudio/best"
    )
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "-f", fmt,
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "192K",
        "--extractor-args", f"youtube:player_client={client}",
        "-o", str(AUDIO_DIR / "%(id)s.%(ext)s"),
    ]

    # Prefer a cookies.txt file (more stable than live browser extraction)
    if cookies_file and Path(cookies_file).exists():
        cmd += ["--cookies", cookies_file]
    # Only fall back to live browser cookies if no file exists
    # (live extraction often fails with stale/rotated cookies)

    cmd.append(url)
    return cmd



_STRATEGIES = [
    ("mweb",         True),   # Mobile web — currently most reliable
    ("mweb",         False),
    ("ios",          True),   # iOS client — exempt from SABR
    ("ios",          False),
    ("mediaconnect", True),   # Apple TV / AirPlay client
    ("mediaconnect", False),
    ("web_creator",  True),
    ("android_vr",   True),   # VR client — often overlooked by blocks
]

# Path to a cookies.txt exported from your browser (Netscape format).
# Export using the "Get cookies.txt LOCALLY" Chrome extension.
# Place this file in your project root, or set to None to skip.
COOKIES_FILE = "cookies.txt"


def download_audio(url: str, lang: str = "en") -> str:
    video_id = _extract_video_id(url)
    audio_file = AUDIO_DIR / f"{video_id}.mp3"

    if audio_file.exists() and audio_file.stat().st_size > 0:
        return str(audio_file)

    # Clean up empty leftover from a previous failed attempt
    if audio_file.exists():
        audio_file.unlink()

    last_error = "No strategies attempted."

    for client, skip_hls in _STRATEGIES:
        command = _build_command(url, client, skip_hls, COOKIES_FILE)
        print(f"[yt-dlp] Trying client={client!r}, skip_hls={skip_hls}")
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            last_error = e.stderr.strip() if e.stderr else "Unknown yt-dlp error"
            print(f"[yt-dlp] Failed ({client}): {last_error[-300:]}")

            # Hard stop — video is genuinely unavailable/private
            if "Video unavailable" in last_error or "Private video" in last_error:
                raise HTTPException(status_code=404, detail="Video is unavailable or private.")

            # Clean empty file before next attempt
            if audio_file.exists() and audio_file.stat().st_size == 0:
                audio_file.unlink()
            continue

        if audio_file.exists() and audio_file.stat().st_size > 0:
            print(f"[yt-dlp] Success with client={client!r}, skip_hls={skip_hls}")
            return str(audio_file)

        # yt-dlp exited 0 but produced nothing — treat as failure
        if audio_file.exists():
            audio_file.unlink()

    raise HTTPException(
        status_code=500,
        detail=f"All download strategies failed. Last error:\n{last_error[-400:]}",
    )




MODEL = WhisperModel("base")


def trancribe_audio_to_json(audio_path: str):
    audio_file = Path(audio_path)
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    segments, info = MODEL.transcribe(str(audio_file), beam_size=5)

    try:
        audio_file.unlink()
    except Exception:
        pass

    return [
        {"start": seg.start, "end": seg.end, "text": seg.text.strip()}
        for seg in segments
    ]