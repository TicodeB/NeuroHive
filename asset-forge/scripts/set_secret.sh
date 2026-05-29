#!/usr/bin/env bash
# ASSET-FORGE — secure secret capture.
#
# Captures a secret (default: OPENROUTER_API_KEY) WITHOUT echoing it to the
# screen, WITHOUT printing it to chat, and WITHOUT committing it to git.
# It writes to asset-forge/.env, which is git-ignored (see repo .gitignore).
#
# IMPORTANT: run this in YOUR OWN terminal. The value is read with `read -rs`
# (silent), so it never appears on screen and is never sent to the assistant.
#
# Usage:
#   bash asset-forge/scripts/set_secret.sh                  # OPENROUTER_API_KEY
#   bash asset-forge/scripts/set_secret.sh OPENROUTER_MODEL # a named key/value
#
# Preferred alternative (no file at all): set OPENROUTER_API_KEY as a secret /
# environment variable in your Claude Code on the web environment settings.
set -euo pipefail

KEY_NAME="${1:-OPENROUTER_API_KEY}"
ENV_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.env"

printf 'Paste value for %s (input hidden, then press Enter): ' "$KEY_NAME" >&2
read -rs SECRET_VALUE
printf '\n' >&2

if [[ -z "${SECRET_VALUE}" ]]; then
  printf 'No value entered — aborting, nothing written.\n' >&2
  exit 1
fi

touch "$ENV_FILE"
chmod 600 "$ENV_FILE"
# Replace any existing line for this key, then append the new one.
if grep -q "^${KEY_NAME}=" "$ENV_FILE" 2>/dev/null; then
  grep -v "^${KEY_NAME}=" "$ENV_FILE" > "${ENV_FILE}.tmp" && mv "${ENV_FILE}.tmp" "$ENV_FILE"
  chmod 600 "$ENV_FILE"
fi
printf '%s=%s\n' "$KEY_NAME" "$SECRET_VALUE" >> "$ENV_FILE"
unset SECRET_VALUE

printf '\xe2\x9c\x93 Saved %s to %s (git-ignored, chmod 600). Value was not displayed.\n' "$KEY_NAME" "$ENV_FILE" >&2
