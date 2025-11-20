import json
import sys
from pathlib import Path
from typing import Literal

# Add parent directory to path so we can import experience_app modules
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from experience_app.service import DummyAssistantService, ExperienceResponse


class TextRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    response_modality: Literal["text", "audio"] = "text"


class AudioRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    audio_base64: str = Field(..., min_length=1, description="Base64-encoded PCM data")
    response_modality: Literal["text", "audio"] = "text"


app = FastAPI(
    title="Experience API",
    version="0.1.0",
    description="FastAPI layer that faces clients and proxies to Google ADK.",
)

assistant_service = DummyAssistantService()

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Serve the playground UI."""
    html_path = STATIC_DIR / "index.html"
    if not html_path.exists():
        return JSONResponse(
            {"error": f"HTML file not found at {html_path}"}, 
            status_code=500
        )
    return FileResponse(html_path, media_type="text/html")

@app.get("/health")
async def health():
    """Health check endpoint."""
    return JSONResponse({"status": "ok", "static_dir": str(STATIC_DIR)})

@app.get("/test/ws")
async def test_websocket():
    """Simple WebSocket test endpoint - sends test messages."""
    return JSONResponse({
        "message": "WebSocket test endpoint",
        "instructions": "Connect to /experience/ws/{session_id}?response_modality=audio to test audio",
        "test_url": "/experience/ws/test-session?response_modality=audio"
    })


def _response_payload(response: ExperienceResponse) -> dict:
    return {
        "session_id": response.session_id,
        "mime_type": response.mime_type,
        "data": response.data,
        "metadata": response.metadata,
    }


@app.post("/experience/v1/messages:text")
async def send_text_message(payload: TextRequest):
    response = await assistant_service.handle_text(
        session_id=payload.session_id,
        text=payload.text,
        response_modality=payload.response_modality,
    )
    return JSONResponse(_response_payload(response))


@app.post("/experience/v1/messages:audio")
async def send_audio_message(payload: AudioRequest):
    response = await assistant_service.handle_audio(
        session_id=payload.session_id,
        audio_base64=payload.audio_base64,
        response_modality=payload.response_modality,
    )
    return JSONResponse(_response_payload(response))


@app.websocket("/experience/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, response_modality: str = "text"):
    await websocket.accept()
    print(f"WebSocket connected: session_id={session_id}, response_modality={response_modality}")
    normalized_modality: Literal["text", "audio"] = "audio" if response_modality == "audio" else "text"
    
    # Send a welcome message to confirm connection
    try:
        welcome = ExperienceResponse(
            session_id=session_id,
            mime_type="text/plain",
            data="Connected successfully!",
            metadata={"source": "system", "type": "connection"}
        )
        await websocket.send_text(json.dumps(_response_payload(welcome)))
    except Exception as e:
        print(f"Error sending welcome message: {e}")
    
    try:
        while True:
            raw_message = await websocket.receive_text()
            message = json.loads(raw_message)
            mime_type: str = message.get("mime_type", "text/plain")
            data: str = message.get("data", "")
            # Extract response_modality if present, otherwise use the connection-level default
            msg_modality = message.get("response_modality", normalized_modality)
            print(f"Received message: mime_type={mime_type}, modality={msg_modality}, data_length={len(data)}")
            
            stream = assistant_service.stream(
                session_id=session_id,
                mime_type="audio/pcm" if mime_type == "audio/pcm" else "text/plain",
                data=data,
                response_modality=msg_modality,
            )
            async for chunk in stream:
                await websocket.send_text(json.dumps(_response_payload(chunk)))
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: session_id={session_id}")
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f"WebSocket error for session {session_id}: {exc}")
        import traceback
        traceback.print_exc()
        try:
            await websocket.send_text(
                json.dumps(
                    {
                        "session_id": session_id,
                        "mime_type": "text/plain",
                        "data": f"[error] {exc}",
                        "metadata": {"source": "experience", "level": "error"},
                    }
                )
            )
        except:
            pass
    finally:
        try:
            await websocket.close()
            print(f"WebSocket closed: session_id={session_id}")
        except:
            pass

