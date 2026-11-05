# ─────────────────────────────────────────────────────────────────────────────
# flappy-bob  —  Dockerfile
# Works on: macOS (Intel & Apple Silicon), Linux, Windows (via Podman/Docker)
#
# pygame-ce needs an X11 / Wayland display.
# On macOS → XQuartz; on Linux → host DISPLAY; on Windows → VcXsrv / WSLg
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

# System-level SDL2 + audio/video libs pygame-ce needs
RUN apt-get update && apt-get install -y --no-install-recommends \
        libsdl2-2.0-0 \
        libsdl2-image-2.0-0 \
        libsdl2-mixer-2.0-0 \
        libsdl2-ttf-2.0-0 \
        libsdl2-dev \
        libgl1 \
        libgles2 \
        libegl1 \
        x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# ── Dependency layer (cached unless pyproject.toml changes) ──────────────────
COPY pyproject.toml ./
RUN uv sync --no-dev

# ── Application layer ────────────────────────────────────────────────────────
COPY . .

ENV PYTHONUNBUFFERED=1
ENV SDL_VIDEODRIVER=x11

CMD ["uv", "run", "python", "main.py"]
