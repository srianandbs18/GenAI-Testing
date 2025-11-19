"""
Experience API package.

This package hosts the FastAPI layer that faces client applications.
It intentionally decouples transport concerns from the Google ADK
integration layer so we can return mock responses today and plug in
the real assistant later without touching the HTTP/websocket surface.
"""

