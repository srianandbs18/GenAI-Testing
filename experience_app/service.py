from __future__ import annotations

import asyncio
import base64
import tempfile
import os
import time
import pyttsx3
from typing import AsyncGenerator, Dict, Literal, Optional

from pydantic import BaseModel, Field


class ExperienceResponse(BaseModel):
    """Represents a single payload returned to the experience client."""

    session_id: str
    mime_type: Literal["text/plain", "audio/pcm"]
    data: str
    metadata: Dict[str, str] = Field(default_factory=dict)


class AssistantService:
    """Abstract interface for any assistant implementation."""

    async def handle_text(
        self, session_id: str, text: str, response_modality: Literal["text", "audio"]
    ) -> ExperienceResponse:  # pragma: no cover - interface only
        raise NotImplementedError

    async def handle_audio(
        self, session_id: str, audio_base64: str, response_modality: Literal["text", "audio"]
    ) -> ExperienceResponse:  # pragma: no cover - interface only
        raise NotImplementedError

    def stream(
        self,
        session_id: str,
        mime_type: Literal["text/plain", "audio/pcm"],
        data: str,
        response_modality: Literal["text", "audio"],
    ) -> AsyncGenerator[ExperienceResponse, None]:  # pragma: no cover - interface only
        raise NotImplementedError


class DummyAssistantService(AssistantService):
    """Temporary assistant that echoes inputs in the requested modality."""

    def __init__(self) -> None:
        self._latency_s = 0.15
        # Initialize TTS engine (lazy init in method might be safer for threading, but let's try global first or per-call)
        # pyttsx3 is not always thread-safe. We'll use a helper to run it in a separate process or just lock it.
        # For simplicity in this demo, we'll init it inside the generation method or use a simple lock if needed.
        pass

    def _generate_tts_audio(self, text: str) -> str:
        """Generate TTS audio for the given text and return base64 PCM/WAV."""
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf:
            temp_filename = tf.name
        
        try:
            engine = pyttsx3.init()
            # Configure voice if needed (optional)
            # voices = engine.getProperty('voices')
            # engine.setProperty('voice', voices[1].id) # Try female voice if available
            
            engine.save_to_file(text, temp_filename)
            engine.runAndWait()
            
            # Read the file back
            with open(temp_filename, "rb") as f:
                audio_data = f.read()
                
            return base64.b64encode(audio_data).decode("ascii")
        except Exception as e:
            print(f"TTS Error: {e}")
            return ""
        finally:
            if os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                except:
                    pass

    async def handle_text(
        self, session_id: str, text: str, response_modality: Literal["text", "audio"]
    ) -> ExperienceResponse:
        if response_modality == "text":
            # Return a friendly echo response
            payload = f"You said: {text}. This is a dummy response from the Experience API."
            mime_type = "text/plain"
        else:
            payload = self._get_audio_response(text)
            mime_type = "audio/pcm"
        return ExperienceResponse(
            session_id=session_id,
            mime_type=mime_type,
            data=payload,
            metadata=self._metadata(source="text"),
        )

    async def handle_audio(
        self, session_id: str, audio_base64: str, response_modality: Literal["text", "audio"]
    ) -> ExperienceResponse:
        if response_modality == "audio":
            payload = audio_base64  # Echo the audio data
            mime_type = "audio/pcm"
        else:
            # Pretend we transcribed the audio bytes.
            transcript = "[dummy-transcript] audio length={} bytes".format(
                len(base64.b64decode(audio_base64))
            )
            payload = self._format_text(transcript)
            mime_type = "text/plain"
        return ExperienceResponse(
            session_id=session_id,
            mime_type=mime_type,
            data=payload,
            metadata=self._metadata(source="audio"),
        )

    async def _yield_chunks(
        self, session_id: str, chunk_text: str, response_modality: Literal["text", "audio"]
    ) -> AsyncGenerator[ExperienceResponse, None]:
        parts = chunk_text.split()
        for index, token in enumerate(parts, start=1):
            await asyncio.sleep(self._latency_s)
            if response_modality == "text":
                payload = self._format_text(token)
                mime_type = "text/plain"
            else:
                # For streaming, we just send the full audio in the first chunk for now
                # as we are using static files. In a real system, this would be chunked.
                if index == 1:
                    payload = self._get_audio_response(chunk_text)
                    mime_type = "audio/pcm"
                else:
                    continue # Skip subsequent chunks for audio to avoid repeating the file
            yield ExperienceResponse(
                session_id=session_id,
                mime_type=mime_type,
                data=payload,
                metadata=self._metadata(source="stream", chunk=index, total=len(parts)),
            )

    async def stream(
        self,
        session_id: str,
        mime_type: Literal["text/plain", "audio/pcm"],
        data: str,
        response_modality: Literal["text", "audio"],
    ) -> AsyncGenerator[ExperienceResponse, None]:
        """Simulate a streaming response suitable for websocket clients."""

        if mime_type == "text/plain":
            # Echo the user's text with a simple response
            response_text = f"I heard you say: {data}"
        else:
            decoded = base64.b64decode(data)
            response_text = f"I received {len(decoded)} bytes of audio."
        
        # 1. Yield Text Response
        yield ExperienceResponse(
            session_id=session_id,
            mime_type="text/plain",
            data=response_text,
            metadata=self._metadata(source="stream", type="transcript"),
        )
        
        # 2. Yield Audio Response (TTS)
        # We always generate audio now, as requested ("text should be speaked out")
        audio_base64 = self._generate_tts_audio(response_text)
        if audio_base64:
            yield ExperienceResponse(
                session_id=session_id,
                mime_type="audio/pcm",
                data=audio_base64,
                metadata=self._metadata(source="stream", type="tts"),
            )

    def _format_text(self, text: str) -> str:
        # Return clean text without prefix for better UX
        return text

    def _synthesize_audio_bytes(self, text: str) -> str:
        # Generate simple PCM audio: a sine wave tone
        # 16-bit PCM, 24kHz sample rate, 0.5 seconds
        import struct
        import math
        
        sample_rate = 24000
        duration = 0.5  # seconds
        frequency = 440  # A4 note
        num_samples = int(sample_rate * duration)
        
        # Generate sine wave
        audio_data = bytearray()
        for i in range(num_samples):
            # Generate sine wave sample
            sample = math.sin(2 * math.pi * frequency * i / sample_rate)
            # Convert to 16-bit PCM
            pcm_sample = int(sample * 32767)
            # Pack as little-endian 16-bit integer
            audio_data.extend(struct.pack('<h', pcm_sample))
        
        # Encode to base64
        return base64.b64encode(bytes(audio_data)).decode("ascii")

    def _metadata(self, source: str, **extra: Optional[int]) -> Dict[str, str]:
        metadata: Dict[str, str] = {
            "source": source,
            "timestamp": str(time.time()),
        }
        for key, value in extra.items():
            if value is not None:
                metadata[key] = str(value)
        return metadata

