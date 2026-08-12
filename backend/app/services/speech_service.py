from typing import Optional

class SpeechToTextService:
    """
    Service abstraction for Speech-To-Text processing.
    For MVP free-tier architecture, transcription is handled via Browser Native Web Speech API
    (SpeechRecognition) on the frontend client at $0.00 cost.
    """
    @classmethod
    def transcribe(cls, audio_payload: Optional[bytes] = None) -> str:
        # Fallback server-side transcription interface
        return ""

class TextToSpeechService:
    """
    Service abstraction for Text-To-Speech generation.
    For MVP free-tier architecture, synthesis is handled via Browser Native Web Speech API
    (SpeechSynthesis) on the frontend client at $0.00 cost.
    """
    @classmethod
    def synthesize(cls, text: str) -> dict:
        return {
            "text": text,
            "engine": "browser_web_speech_api",
            "cost_usd": 0.0
        }
