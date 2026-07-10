#!/usr/bin/env bash
# Компілює gettext-переклади (.po → .mo) перед деплоєм або після оновлення locale/.
set -o errexit
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

ROOT="$(project_dir)"
PYTHON_BIN="$(resolve_python_bin "$ROOT")"

cd "$ROOT"
"$PYTHON_BIN" manage.py compilemessages
echo "✓ Locale files compiled"
