"""
API route for audio transcription using the Faster Whisper model.

This module defines an endpoint that accepts an audio file upload (MP3),
saves it temporarily, and transcribes its content using a tiny Whisper model.
"""

from fastapi import APIRouter, HTTPException
from faster_whisper import WhisperModel
from pydantic import BaseModel

import os
import requests
import shutil
import tempfile

router = APIRouter(
    prefix="",
    tags=["form"]
)

# Load tiny model from Hugging Face
model = WhisperModel("guillaumekln/faster-whisper-tiny", compute_type="int8")

class AudioURL(BaseModel):
    filename: str

@router.post("/transcribe/")
async def transcribe(payload: AudioURL):
    """
    Endpoint to transcribe an audio file from a given URL.

    This function downloads an audio file specified by the filename in the payload
    from a configured remote server, temporarily saves it locally, and then uses
    a Whisper model to transcribe the audio into text.

    Args:
        payload (AudioURL): An object containing the filename of the audio file to transcribe.

    Returns:
        dict: A dictionary with a single key "transcription" containing the transcribed text.

    Raises:
        HTTPException: 
            - If the audio file download fails (status code != 200), raises a 400 error.
            - For any other errors during processing or transcription, raises a 500 error with the exception details.
    """
    try:
        # Download audio
        response = requests.get(url=os.getenv('DJANGO_CHAT_URL')+ f'{payload.filename}', stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download audio file")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            shutil.copyfileobj(response.raw, tmp)
            tmp_path = tmp.name

        # Run transcription using the Whisper model
        segments, _ = model.transcribe(tmp_path)
        text = " ".join([seg.text for seg in segments])

        return {"transcription": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
