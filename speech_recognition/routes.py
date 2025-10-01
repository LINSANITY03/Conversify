"""
API route for audio transcription using the Faster Whisper model.

This module defines an endpoint that accepts an audio file upload (MP3),
saves it temporarily, and transcribes its content using a tiny Whisper model.
"""

from fastapi import FastAPI, UploadFile, File, APIRouter
from faster_whisper import WhisperModel

import tempfile
import shutil

router = APIRouter(
    prefix="",
    tags=["form"]
)

# Load tiny model from Hugging Face
model = WhisperModel("guillaumekln/faster-whisper-tiny", compute_type="int8")

@router.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    """
    Transcribe an uploaded audio file using the Whisper model.

    Args:
        file (UploadFile): The uploaded audio file (expected in MP3 format).

    Returns:
        dict: A dictionary containing the transcribed text.
    """

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Run transcription using the Whisper model
    segments, _ = model.transcribe(tmp_path)
    text = " ".join([seg.text for seg in segments])

    return {"transcription": text}
