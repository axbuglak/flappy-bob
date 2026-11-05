@echo off
REM scripts\run.bat — Build the container image and launch the game on Windows
REM
REM Prerequisites:
REM   * Podman Desktop installed (https://podman-desktop.io/)
REM   * VcXsrv running with "Disable access control" checked
REM     Download: https://sourceforge.net/projects/vcxsrv/
REM
REM Usage:
REM   scripts\run.bat            (build + run)
REM   scripts\run.bat --no-build (skip rebuild)

setlocal EnableDelayedExpansion

set IMAGE_NAME=flappy-bob
set CONTAINER_NAME=flappy-bob-game
set NO_BUILD=0

for %%A in (%*) do (
  if "%%A"=="--no-build" set NO_BUILD=1
)

REM ── Detect VcXsrv / X server ───────────────────────────────────────────────
set DISPLAY_VAR=host.containers.internal:0.0
echo Platform: Windows
echo DISPLAY=%DISPLAY_VAR%

REM ── Remove stale container ─────────────────────────────────────────────────
podman rm -f %CONTAINER_NAME% 2>nul

REM ── Build ──────────────────────────────────────────────────────────────────
if %NO_BUILD%==0 (
  echo Building container image ...
  podman build -t %IMAGE_NAME% "%~dp0.."
  if !ERRORLEVEL! NEQ 0 (
    echo Build failed. Check the error above.
    exit /b 1
  )
  echo Image built: %IMAGE_NAME%
)

REM ── Run ────────────────────────────────────────────────────────────────────
echo Starting game ...
podman run --rm ^
  --name %CONTAINER_NAME% ^
  -e DISPLAY=%DISPLAY_VAR% ^
  -e SDL_VIDEODRIVER=x11 ^
  %IMAGE_NAME%
