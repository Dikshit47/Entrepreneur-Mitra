"""Voice API routes for Speech-to-Text and Text-to-Speech."""
from fastapi import APIRouter, UploadFile, File, Form, Query
from app.schemas.voice import VoiceTranscribeResponse, VoiceSpeakRequest, VoiceSpeakResponse
from app.schemas.common import ApiResponse
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voice", tags=["Voice Engine"])


@router.post("/transcribe", response_model=ApiResponse[VoiceTranscribeResponse])
async def transcribe_audio_input(
    audio: UploadFile = File(...),
    language: str = Form("hi")
):
    """
    Transcribe spoken voice audio into text.
    Abstracted interface supporting IndicConformer, Whisper, or browser speech input.
    """
    audio_bytes = await audio.read()
    transcription = await VoiceService.transcribe_audio(audio_bytes, language=language)
    return ApiResponse.success_response(transcription)


@router.post("/speak", response_model=ApiResponse[VoiceSpeakResponse])
async def synthesize_speech_output(req: VoiceSpeakRequest):
    """
    Convert text into synthesized speech audio (TTS).
    Provides native Indian language pronunciation (Hindi, English, Hinglish).
    """
    synthesis = await VoiceService.synthesize_speech(req.text, language=req.language)
    return ApiResponse.success_response(synthesis)
