#!/usr/bin/env bash
# Імпорт новин ринку з RSS (liga.net/telecom, itc.ua/mobilnaya-svyaz).
# Локально: bash scripts/fetch_market_news.sh
# На хостингу: той самий скрипт у cron (див. scripts/setup_market_news_cron.sh).

source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

PROJECT_DIR="$(project_dir)"
cd "$PROJECT_DIR"

load_env_file "$PROJECT_DIR/.env"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.dev}"

PYTHON_BIN="$(resolve_python_bin "$PROJECT_DIR")"
LOG_DIR="${MARKET_NEWS_LOG_DIR:-$PROJECT_DIR/logs}"
LOG_FILE="$LOG_DIR/fetch_news.log"

ensure_log_dir "$LOG_DIR"

{
  echo "=== $(date -u '+%Y-%m-%dT%H:%M:%SZ') fetch_market_news start ==="
  "$PYTHON_BIN" manage.py fetch_market_news
  echo "=== $(date -u '+%Y-%m-%dT%H:%M:%SZ') fetch_market_news done ==="
} 2>&1 | tee -a "$LOG_FILE"
