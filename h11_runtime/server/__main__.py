"""Launcher for the H11-AGI Conversational Reasoning Chat Server.

Run with:
    python -m h11_runtime.server
"""
from __future__ import annotations

import os
import sys

try:
    import uvicorn
except ImportError:
    print("uvicorn is required to run the H11-AGI server. Install with: pip install uvicorn")
    sys.exit(1)

def main() -> None:
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"================================================================")
    print(f"   H11-AGI Sovereign Conversational Reasoning Interface        ")
    print(f"   Target Domain: h11.network                                   ")
    print(f"   Serving locally at: http://localhost:{port}                 ")
    print(f"================================================================")
    uvicorn.run("h11_runtime.server.app:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()
