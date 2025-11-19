from __future__ import annotations

import asyncio
import base64
import time
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

    async def handle_text(
        self, session_id: str, text: str, response_modality: Literal["text", "audio"]
    ) -> ExperienceResponse:
        if response_modality == "text":
            # Return a friendly echo response
            payload = f"You said: {text}. This is a dummy response from the Experience API."
            mime_type = "text/plain"
        else:
            payload = self._synthesize_audio_bytes(text)
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
                payload = self._synthesize_audio_bytes(token)
                mime_type = "audio/pcm"
            yield ExperienceResponse(
                session_id=session_id,
                mime_type=mime_type,
                data=payload,
                metadata=self._metadata(source="stream", chunk=index, total=len(parts)),
            )

    def stream(
        self,
        session_id: str,
        mime_type: Literal["text/plain", "audio/pcm"],
        data: str,
        response_modality: Literal["text", "audio"],
    ) -> AsyncGenerator[ExperienceResponse, None]:
        """Simulate a streaming response suitable for websocket clients."""

        if mime_type == "text/plain":
            # Echo the user's text with a simple response
            chunk_text = f"I received: {data}. This is a dummy response. When connected to Google ADK, you'll get real AI responses here."
        else:
            decoded = base64.b64decode(data)
            chunk_text = f"I received {len(decoded)} bytes of audio. This is a dummy response."
        return self._yield_chunks(session_id, chunk_text, response_modality)

    def _format_text(self, text: str) -> str:
        # Return clean text without prefix for better UX
        return text

    def _synthesize_audio_bytes(self, text: str) -> str:
        # Generate simple PCM audio: a sine wave tone
        # 16-bit PCM, 24kHz sample rate, 0.5 seconds
        import struct
        import math
        
        sample_rate = 240
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

