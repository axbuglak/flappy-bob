#!/usr/bin/env bash
# scripts/run.sh — Build the container image and launch the game
#
# Prerequisites:
#   • Podman installed
#   • On macOS: XQuartz running  (brew install --cask xquartz)
#   • On Linux: DISPLAY set (usually automatic in a desktop session)
#
# Usage:
#   ./scripts/run.sh            # build + run
#   ./scripts/run.sh --no-build # skip rebuild (faster on re-runs)

set -euo pipefail

IMAGE_NAME="flappy-bob"
CONTAINER_NAME="flappy-bob-game"
NO_BUILD=false

# ── Parse args ─────────────────────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --no-build) NO_BUILD=true ;;
    *) echo "Unknown argument: $arg" && exit 1 ;;
  esac
done

# ── Detect platform ────────────────────────────────────────────────────────
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "🖥  Platform: $OS / $ARCH"

# ── X11 display setup ──────────────────────────────────────────────────────
if [[ "$OS" == "Darwin" ]]; then
  # macOS: require XQuartz
  if ! pgrep -x Xquartz &>/dev/null; then
    echo "⚠️  XQuartz is not running."
    echo "   Start it with:  open -a XQuartz"
    echo "   Then re-run this script."
    exit 1
  fi
  # Allow connections from localhost
  xhost +localhost 2>/dev/null || true
  DISPLAY_VAR="host.containers.internal:0"
else
  # Linux: use the current DISPLAY
  DISPLAY_VAR="${DISPLAY:-:0}"
  # Allow container to connect to X server
  xhost +local:podman 2>/dev/null || xhost +local: 2>/dev/null || true
fi

echo "📺  DISPLAY=$DISPLAY_VAR"

# ── Remove stale container ──────────────────────────────────────────────────
podman rm -f "$CONTAINER_NAME" 2>/dev/null || true

# ── Build ───────────────────────────────────────────────────────────────────
if [[ "$NO_BUILD" == false ]]; then
  echo "🔨  Building container image …"
  podman build \
    --platform "linux/$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')" \
    -t "$IMAGE_NAME" \
    "$(dirname "$0")/.."
  echo "✅  Image built: $IMAGE_NAME"
fi

# ── Run ─────────────────────────────────────────────────────────────────────
echo "🚀  Starting game …"
podman run --rm \
  --name "$CONTAINER_NAME" \
  -e DISPLAY="$DISPLAY_VAR" \
  -e SDL_VIDEODRIVER=x11 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  "$IMAGE_NAME"
