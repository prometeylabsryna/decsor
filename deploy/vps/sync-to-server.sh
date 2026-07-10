#!/usr/bin/env bash
# Синхронізація проєкту з Mac на VPS (запускати ЛОКАЛЬНО)
#
#   bash deploy/vps/sync-to-server.sh
#   bash deploy/vps/sync-to-server.sh --update   # rsync + deploy_vps.sh update на сервері

set -o errexit
set -o pipefail

SERVER="${DEPLOY_SERVER:-root@178.20.157.42}"
REMOTE_DIR="${DEPLOY_REMOTE_DIR:-/var/www/itmcopy}"
LOCAL_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

RSYNC_EXCLUDES=(
  --exclude '.git'
  --exclude '.venv'
  --exclude '__pycache__'
  --exclude '*.pyc'
  --exclude '.env'
  --exclude 'media/'
  --exclude 'staticfiles/'
  --exclude 'logs/*.log'
  --exclude '.DS_Store'
)

echo "→ mkdir -p $REMOTE_DIR на сервері"
ssh "$SERVER" "mkdir -p '$REMOTE_DIR'"

echo "→ rsync $LOCAL_DIR → $SERVER:$REMOTE_DIR"
rsync -avz --delete "${RSYNC_EXCLUDES[@]}" "$LOCAL_DIR/" "$SERVER:$REMOTE_DIR/"

if [[ "${1:-}" == "--update" ]]; then
  echo "→ deploy_vps.sh update на сервері"
  ssh "$SERVER" "cd $REMOTE_DIR && bash scripts/deploy_vps.sh update"
fi

echo "✓ Синхронізацію завершено"
