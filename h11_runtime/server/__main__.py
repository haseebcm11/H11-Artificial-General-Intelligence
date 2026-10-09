from __future__ import annotations

import logging
import os
import sys

import uvicorn

from .config import get_settings


logger = logging.getLogger("h11_runtime.server")


def main() -> None:
    settings = get_settings()
    port = settings.port
    host = settings.host
    log_level = settings.log_level.lower()

    print("================================================================")
    print("   H11-AGI Sovereign Conversational Reasoning Interface        ")
    print(f"   Environment: {settings.env:<30}")
    print(f"   Target Domain: h11.network                                   ")
    print(f"   Serving locally at: http://{host}:{port}                 ")
    print("================================================================")

    uvicorn.run(
        "h11_runtime.server.app:app",
        host=host,
        port=port,
        reload=settings.debug,
        log_level=log_level,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
        sys.exit(0)
