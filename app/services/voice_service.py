"""Voice processing abstraction for Speech-to-Text and Text-to-Speech."""
from abc import ABC, abstractmethod
from typing import Optional
from app.schemas.voice import VoiceTranscribeResponse, VoiceSpeakResponse


class VoiceProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, language: str = "hi") -> VoiceTranscribeResponse:
        pass

    @abstractmethod
    async def synthesize(self, text: str, language: str = "hi") -> VoiceSpeakResponse:
        pass


class MockVoiceProvider(VoiceProvider):
    """
    Mock/Browser-compatible Voice Provider.
    Ensures that voice endpoints function reliably during offline hackathon demos
    and work seamlessly with browser Web Speech API fallbacks.
    """
    async def transcribe(self, audio_bytes: bytes, language: str = "hi") -> VoiceTranscribeResponse:
        return VoiceTranscribeResponse(
            transcript="Mujhe silai ka business shuru karne ke liye 3 lakh ka loan chahiye.",
            confidence=0.96,
            detected_language=language,
            duration_seconds=3.2
        )

    async def synthesize(self, text: str, language: str = "hi") -> VoiceSpeakResponse:
        # Returns simulated audio payload / web speech instructions
        return VoiceSpeakResponse(
            audio_base64="UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=",
            audio_url=None,
            language=language,
            status="SYNTHESIZED"
        )


class VoiceService:
    _provider: VoiceProvider = MockVoiceProvider()

    @classmethod
    def set_provider(cls, provider: VoiceProvider):
        cls._provider = provider

    @classmethod
    async def transcribe_audio(cls, audio_bytes: bytes, language: str = "hi") -> VoiceTranscribeResponse:
        return await cls._provider.transcribe(audio_bytes, language)

    @classmethod
    async def synthesize_speech(cls, text: str, language: str = "hi") -> VoiceSpeakResponse:
        return await cls._provider.synthesize(text, language)
