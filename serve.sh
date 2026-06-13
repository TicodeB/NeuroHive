#!/usr/bin/env bash
# Leanta — one-command local preview of the static site.
# Usage:  ./serve.sh [port]      (default 8000)
# Then open:  http://localhost:<port>/v7/   (or /v4/ /v5/ /v6/)
set -euo pipefail
PORT="${1:-8000}"
cd "$(dirname "$0")"
echo "Leanta preview running →  http://localhost:${PORT}/"
echo "  mockups:  /v4/  /v5/  /v6/  /v7/"
echo "  (Ctrl-C to stop)"
python3 -m http.server "${PORT}"
