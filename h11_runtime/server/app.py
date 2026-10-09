"""FastAPI / Starlette Production ASGI Server for H11-AGI Chat & Reasoning.

Provides:
- `GET  /`              ──► Production Single Page Chat Application
- `POST /api/chat`      ──► REST Reasoning Endpoint
- `WS   /ws/chat`       ──► Full-Duplex Real-Time Streaming WebSocket
- `GET  /api/health`    ──► Health and Telemetry Status
- `GET  /api/clusters`  ──► Cognitive Manifolds and Agent Rosters
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, JSONResponse
    from pydantic import BaseModel, Field

    _fastapi_available = True
except ImportError:
    _fastapi_available = False

from .chat_engine import ChatResponse, ConversationalReasoner
from .config import get_settings

settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

if _fastapi_available:
    app = FastAPI(
        title="H11-AGI Multi-Agent Operating System",
        description="Interface for the governed 1,000 Multi-Agent Artificial General Intelligence Operating System",
        version="4.0.1",
    )
    app.state.settings = settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app = None  # type: ignore[assignment]

STATIC_DIR = Path(__file__).parent / "static"
reasoner: Optional[ConversationalReasoner] = None


class ChatRequest(BaseModel):
    query: str = Field(..., description="User query or problem statement to reason over.")
    conversation_id: Optional[str] = Field(None, description="Optional conversation session ID.")


@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    if request.method in {"POST", "PUT", "PATCH"}:
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                size = int(content_length)
            except ValueError:
                size = 0
            if size > settings.body_size_limit_bytes:
                return JSONResponse(
                    status_code=413,
                    content={
                        "detail": (
                            f"Request body exceeds the configured maximum of {settings.body_size_limit_bytes} bytes."
                        )
                    },
                )
    return await call_next(request)


@app.on_event("startup")
async def startup_event() -> None:
    global reasoner
    logger.info("Initializing H11-AGI Conversational Reasoner...")
    try:
        reasoner = ConversationalReasoner()
        await reasoner.initialize()
        logger.info("H11-AGI Conversational Reasoner online and ready.")
    except Exception:
        logger.exception("H11-AGI startup failed")
        raise


@app.get("/healthz")
async def healthz() -> Dict[str, Any]:
    return {
        "status": "ok",
        "service": "h11-agi",
        "environment": settings.env,
    }


@app.get("/readyz")
async def readyz() -> Dict[str, Any]:
    if reasoner is None:
        return JSONResponse(status_code=503, content={"status": "not_ready", "reason": "reasoner_not_initialized"})
    return {"status": "ready", "service": "h11-agi"}


@app.get("/", response_class=HTMLResponse)
async def get_index() -> HTMLResponse:
    """Serves the main Chat Single Page Application."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse(
        content="""
        <html>
            <head><title>H11-AGI</title></head>
            <body style='font-family:sans-serif;background:#0f172a;color:#fff;padding:40px;'>
                <h1>H11-AGI 1,000 Multi-Agent AGI Operating System</h1>
                <p>Chat engine running. Connect via <code>/ws/chat</code> or <code>POST /api/chat</code>.</p>
            </body>
        </html>
        """
    )


@app.post("/api/chat")
async def post_chat(req: ChatRequest) -> Dict[str, Any]:
    """Synchronous REST endpoint for reasoning queries."""
    global reasoner
    if reasoner is None:
        reasoner = ConversationalReasoner()
        await reasoner.initialize()

    try:
        resp: ChatResponse = await reasoner.reason(req.query, conversation_id=req.conversation_id)
        return {
            "query": resp.query,
            "response": resp.response_text,
            "active_manifold": resp.active_manifold,
            "manifold_affinity": resp.manifold_affinity,
            "activated_agents": resp.activated_agents,
            "retrieved_sources": resp.retrieved_sources,
            "merkle_root": resp.merkle_root,
            "align_verified": resp.align_verified,
            "action_licensed": resp.action_licensed,
            "audit_head": resp.audit_head,
            "case_id": resp.case_id,
            "execution_time_ms": resp.execution_time_ms,
            "reasoning_provider": resp.reasoning_provider,
            "reasoning_trace": [
                {"phase": step.phase, "title": step.title, "detail": step.detail}
                for step in resp.reasoning_trace
            ],
        }
    except Exception as exc:
        logger.exception("Error during reasoning:")
        raise HTTPException(status_code=500, detail=str(exc))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket) -> None:
    """Full-duplex WebSocket endpoint streaming reasoning steps & answers."""
    global reasoner
    await websocket.accept()
    if reasoner is None:
        reasoner = ConversationalReasoner()
        await reasoner.initialize()

    try:
        while True:
            raw_data = await websocket.receive_text()
            payload = json.loads(raw_data)
            query = payload.get("query", "").strip()
            conv_id = payload.get("conversation_id")

            if not query:
                await websocket.send_json({"type": "error", "message": "Query cannot be empty."})
                continue

            async for step in reasoner.stream_reason(query, conversation_id=conv_id):
                await websocket.send_json(step)

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected.")
    except Exception as exc:
        logger.exception("WebSocket stream error:")
        try:
            await websocket.send_json({"type": "error", "message": str(exc)})
        except Exception:
            pass


@app.get("/api/health")
async def get_health() -> Dict[str, Any]:
    """Returns server health and telemetry across all 1,000 agents and LSE v3.0."""
    global reasoner
    if reasoner is None:
        reasoner = ConversationalReasoner()
        await reasoner.initialize()

    telemetry = reasoner.agi.get_system_telemetry()
    return {
        "status": "HEALTHY",
        "system": "H11-AGI 1,000 Multi-Agent Artificial General Intelligence Operating System",
        "domain": "h11.network",
        "environment": settings.env,
        "telemetry": telemetry,
    }


@app.get("/api/clusters")
async def get_clusters() -> Dict[str, Any]:
    """Returns all 8 cognitive manifolds and their indexed agent counts."""
    global reasoner
    if reasoner is None:
        reasoner = ConversationalReasoner()
        await reasoner.initialize()

    if reasoner.agi.cluster_engine:
        return reasoner.agi.cluster_engine.get_cluster_stats()
    return {"status": "clustering_disabled"}
