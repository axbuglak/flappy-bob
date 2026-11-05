#!/usr/bin/env python3
"""
bootstrap.py — one-shot setup for the flappy-bob workshop.

Assumptions
-----------
  • Python 3.11+ is already installed (the only hard requirement).
  • Podman is installed (used instead of Docker for the container workflow).
  • Internet access to download uv and Python packages.

What this script does
---------------------
  1. Detects the platform (macOS Intel / Apple Silicon, Linux, Windows/WSL).
  2. Installs `uv` (the fast Python package manager) if not already present.
  3. Runs `uv sync` to create a local .venv with pygame-ce + dev tools.
  4. Verifies the environment with a quick import check.
  5. Prints next-step instructions tailored to the platform.

Usage
-----
  python bootstrap.py
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# ─── Helpers ──────────────────────────────────────────────────────────────────


def info(msg: str) -> None:
    print(f"\033[36m[INFO]\033[0m  {msg}")


def ok(msg: str) -> None:
    print(f"\033[32m[ OK ]\033[0m  {msg}")


def warn(msg: str) -> None:
    print(f"\033[33m[WARN]\033[0m  {msg}")


def error(msg: str) -> None:
    print(f"\033[31m[ERR ]\033[0m  {msg}", file=sys.stderr)


def run(cmd: list[str], check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
    return subprocess.run(cmd, check=check, capture_output=capture, text=True)


# ─── Platform detection ───────────────────────────────────────────────────────


def detect_platform() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "darwin":
        return "macos-arm" if machine in ("arm64", "aarch64") else "macos-intel"
    if system == "linux":
        return "linux"
    if system == "windows" or "microsoft" in platform.release().lower():
        return "windows"
    return "unknown"


# ─── uv installation ──────────────────────────────────────────────────────────


def install_uv() -> None:
    if shutil.which("uv"):
        ok("uv already installed: " + shutil.which("uv"))  # type: ignore[arg-type]
        return

    info("Installing uv …")
    plat = detect_platform()

    if plat in ("macos-arm", "macos-intel", "linux"):
        run(["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"])
        # uv installs to ~/.local/bin — add to PATH for this process
        local_bin = Path.home() / ".local" / "bin"
        os.environ["PATH"] = str(local_bin) + os.pathsep + os.environ.get("PATH", "")
    elif plat == "windows":
        run(
            [
                "powershell",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                "irm https://astral.sh/uv/install.ps1 | iex",
            ]
        )
    else:
        error("Unknown platform — please install uv manually: https://docs.astral.sh/uv/")
        sys.exit(1)

    if shutil.which("uv"):
        ok("uv installed successfully.")
    else:
        error("uv not found on PATH after installation. Add ~/.local/bin to your PATH and re-run.")
        sys.exit(1)


# ─── Python version check ─────────────────────────────────────────────────────


def check_python() -> None:
    major, minor = sys.version_info[:2]
    if (major, minor) < (3, 11):
        error(f"Python 3.11+ required, found {major}.{minor}. Install a newer Python and retry.")
        sys.exit(1)
    ok(f"Python {major}.{minor} detected.")


# ─── Podman check ─────────────────────────────────────────────────────────────


def check_podman() -> None:
    if shutil.which("podman"):
        ok("Podman found: " + shutil.which("podman"))  # type: ignore[arg-type]
    else:
        warn("Podman not found on PATH. Container workflow (scripts/run.sh) won't work.")
        warn("Install Podman: https://podman.io/getting-started/installation")


# ─── uv sync ─────────────────────────────────────────────────────────────────


def sync_dependencies() -> None:
    info("Syncing Python dependencies with uv …")
    run(["uv", "sync"])
    ok("Dependencies installed into .venv/")


# ─── Smoke test ──────────────────────────────────────────────────────────────


def smoke_test() -> None:
    info("Running import smoke test …")
    result = run(
        ["uv", "run", "python", "-c", "import pygame; print(pygame.version.ver)"],
        capture=True,
        check=False,
    )
    if result.returncode == 0:
        ok(f"pygame-ce {result.stdout.strip()} imported successfully.")
    else:
        warn("pygame import failed — this is OK if you plan to use the Docker workflow.")
        warn(result.stderr.strip())


# ─── Platform-specific display hints ─────────────────────────────────────────

HINTS = {
    "macos-arm": (
        "macOS (Apple Silicon) detected.\n"
        "  • To run locally:    uv run python main.py\n"
        "  • To run in Docker:  ./scripts/run.sh\n"
        "    (Docker needs XQuartz: brew install --cask xquartz, then log out & back in)"
    ),
    "macos-intel": (
        "macOS (Intel) detected.\n"
        "  • To run locally:    uv run python main.py\n"
        "  • To run in Docker:  ./scripts/run.sh\n"
        "    (Docker needs XQuartz: brew install --cask xquartz, then log out & back in)"
    ),
    "linux": (
        "Linux detected.\n"
        "  • To run locally:    uv run python main.py\n"
        "  • To run in Docker:  ./scripts/run.sh"
    ),
    "windows": (
        "Windows detected.\n"
        "  • To run locally:    uv run python main.py\n"
        "  • To run in Docker:  .\\scripts\\run.bat\n"
        "    (Install VcXsrv for the X11 display: https://sourceforge.net/projects/vcxsrv/)"
    ),
}

# ─── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    print("\n🕹️  flappy-bob — bootstrap\n" + "─" * 42)
    check_python()
    check_podman()
    install_uv()
    sync_dependencies()
    smoke_test()

    plat = detect_platform()
    hint = HINTS.get(plat, "Platform unknown — see README.md for manual steps.")
    print(f"\n\033[32m✓ Setup complete!\033[0m\n\n{hint}\n")
    print("Start IBM Bob in this directory:  track-1\n")


if __name__ == "__main__":
    main()
