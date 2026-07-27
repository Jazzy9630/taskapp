"""
Vercel serverless entrypoint.
Vercel's Python runtime auto-detects an ASGI app named `app` in this file
and wraps it as a serverless function. We just re-export the real app.
"""
from main import app  # noqa: F401
