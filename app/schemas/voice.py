"""Voice and AI explanation schemas."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class VoiceTranscribeResponse(BaseModel):
    transcript: str
    confidence: float
    detected_language: str
    duration_seconds: Optional[float] = None


class VoiceSpeakRequest(BaseModel):
    text: str
    language: str = "hi"  # hi, en, hinglish
    voice_speed: float = 1.0


class VoiceSpeakResponse(BaseModel):
    audio_base64: Optional[str] = None
    audio_url: Optional[str] = None
    language: str
    status: str = "SYNTHESIZED"


class AIExplainRequest(BaseModel):
    scheme_id: str
    profile_id: str
    language: str = "hi"


class AIExplainResponse(BaseModel):
    scheme_id: str
    language: str
    decision: str
    plain_explanation: str
    key_points: List[str]
    next_steps: List[str]
    grounding_source: str
