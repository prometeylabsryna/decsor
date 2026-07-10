#!/usr/bin/env bash
# Встановлення автоматичного імпорту новин ринку (локально та на хостингу).
#
# macOS (рекомендовано):
#   bash scripts/setup_market_news_cron.sh install-launchd
#
# Linux / VPS:
#   bash scripts/setup_market_news_cron.sh install
#
# FREEhost.UA / cPanel:
#   bash scripts/setup_market_news_cron.sh show-freehost

set -o errexit
set -o pipefail

source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

PROJECT_DIR="$(project_dir)"
CRON_MARKER="# itmCopy-market-news"
LAUNCHD_LABEL="com.itmcopy.market-news"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"
PLIST_TEMPLATE="$PROJECT_DIR/scripts/com.itmcopy.market-news.plist.template"
DEFAULT_SCHEDULE="0 */6 * * *"
DEFAULT_INTERVAL_SECONDS=21600

load_env_file "$PROJECT_DIR/.env"

SCHEDULE="${MARKET_NEWS_CRON_SCHEDULE:-$DEFAULT_SCHEDULE}"
LOG_DIR="${MARKET_NEWS_LOG_DIR:-$PROJECT_DIR/logs}"
FETCH_SCRIPT="$PROJECT_DIR/scripts/fetch_market_news.sh"

usage() {
  cat <<EOF
Використання: bash scripts/setup_market_news_cron.sh <команда>

Команди:
  install-launchd  macOS: LaunchAgent (кожні 6 год + при вході в систему)
  uninstall-launchd
  install          Linux/VPS: crontab
  uninstall        Прибрати crontab-завдання
  status           Поточний стан
  run-now          Одразу імпортувати новини
  show-freehost    Рядки cron / wget для панелі FREEhost.UA
  show-hosting     Alias для show-freehost

Змінні (.env):
  MARKET_NEWS_CRON_SCHEDULE   Розклад cron (Linux/хостинг)
  MARKET_NEWS_LOG_DIR         Каталог логів (logs)
  DJANGO_SETTINGS_MODULE      config.settings.dev або production
  PYTHON_BIN                  .venv/bin/python
EOF
}

prepare_paths() {
  ensure_log_dir "$LOG_DIR"
  chmod +x "$FETCH_SCRIPT"
}

cron_line() {
  printf '%s %s /bin/bash %s' "$SCHEDULE" "$CRON_MARKER" "$FETCH_SCRIPT"
}

hosting_cron_line() {
  printf '%s /bin/bash %s' "$SCHEDULE" "$FETCH_SCRIPT"
}

install_cron() {
  prepare_paths

  if crontab -l 2>/dev/null | grep -Fq "$CRON_MARKER"; then
    echo "Cron вже встановлено:"
    crontab -l | grep -F "$CRON_MARKER"
    return 0
  fi

  local tmp line
  tmp="$(mktemp)"
  line="$(cron_line)"
  trap 'rm -f "$tmp"' RETURN

  {
    crontab -l 2>/dev/null || true
    echo "$line"
  } > "$tmp"

  if ! crontab "$tmp"; then
    echo "Не вдалося встановити cron. На macOS використовуйте install-launchd." >&2
    return 1
  fi

  echo "Cron встановлено:"
  echo "  $line"
  echo "Лог: $LOG_DIR/fetch_news.log"
}

uninstall_cron() {
  if ! crontab -l 2>/dev/null | grep -Fq "$CRON_MARKER"; then
    echo "Cron для itmCopy не знайдено."
    return 0
  fi

  crontab -l | grep -Fv "$CRON_MARKER" | crontab -
  echo "Cron itmCopy-market-news видалено."
}

render_launchd_plist() {
  sed \
    -e "s|__FETCH_SCRIPT__|$FETCH_SCRIPT|g" \
    -e "s|__LOG_DIR__|$LOG_DIR|g" \
    -e "s|__PROJECT_DIR__|$PROJECT_DIR|g" \
    "$PLIST_TEMPLATE"
}

install_launchd() {
  prepare_paths
  mkdir -p "$HOME/Library/LaunchAgents"

  render_launchd_plist > "$LAUNCHD_PLIST"
  launchctl bootout "gui/$(id -u)/$LAUNCHD_LABEL" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$LAUNCHD_PLIST"
  launchctl enable "gui/$(id -u)/$LAUNCHD_LABEL"
  launchctl kickstart -k "gui/$(id -u)/$LAUNCHD_LABEL"

  echo "LaunchAgent встановлено:"
  echo "  $LAUNCHD_PLIST"
  echo "Інтервал: кожні $((DEFAULT_INTERVAL_SECONDS / 3600)) год + при завантаженні системи"
  echo "Лог: $LOG_DIR/fetch_news.log"
}

uninstall_launchd() {
  launchctl bootout "gui/$(id -u)/$LAUNCHD_LABEL" 2>/dev/null || true
  rm -f "$LAUNCHD_PLIST"
  echo "LaunchAgent $LAUNCHD_LABEL видалено."
}

status_cron() {
  echo "Проєкт:     $PROJECT_DIR"
  echo "Розклад:    $SCHEDULE (cron) / кожні 6 год (launchd)"
  echo "Скрипт:     $FETCH_SCRIPT"
  echo "Лог:        $LOG_DIR/fetch_news.log"
  echo "Settings:   ${DJANGO_SETTINGS_MODULE:-config.settings.dev}"
  echo "Python:     $(resolve_python_bin "$PROJECT_DIR")"
  echo ""

  if [[ "$(uname -s)" == "Darwin" ]] && [[ -f "$LAUNCHD_PLIST" ]]; then
    echo "LaunchAgent: встановлено ($LAUNCHD_PLIST)"
  else
    echo "LaunchAgent: не встановлено"
  fi

  if crontab -l 2>/dev/null | grep -Fq "$CRON_MARKER"; then
    echo "Cron:        встановлено"
    crontab -l | grep -F "$CRON_MARKER"
  else
    echo "Cron:        не встановлено"
  fi

  echo ""
  if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "macOS: bash scripts/setup_market_news_cron.sh install-launchd"
  else
    echo "Linux: bash scripts/setup_market_news_cron.sh install"
  fi
}

show_freehost() {
  prepare_paths
  local domain="${DEPLOY_DOMAIN:-yourdomain.com}"
  local token="${CRON_SECRET_TOKEN:-YOUR_CRON_SECRET}"

  cat <<EOF
FREEhost.UA → Планувальник CRON:

1) Командний рядок (SSH):
$(hosting_cron_line)

2) Метод wget (без Python у cron):
$SCHEDULE wget -q -O /dev/null "https://$domain/cron/fetch-market-news/?token=$token"

На сервері перед цим:
  1. bash scripts/deploy_freehost.sh install
  2. CRON_SECRET_TOKEN у .env (для wget)
  3. chmod +x scripts/fetch_market_news.sh
  4. mkdir -p $(printf '%q' "$LOG_DIR")

Лог CLI: $(printf '%q' "$LOG_DIR")/fetch_news.log
Детальніше: bash scripts/deploy_freehost.sh cron-info
EOF
}

show_hosting() {
  show_freehost
}

run_now() {
  bash "$FETCH_SCRIPT"
}

case "${1:-}" in
  install)
    install_cron
    ;;
  uninstall)
    uninstall_cron
    ;;
  install-launchd)
    install_launchd
    ;;
  uninstall-launchd)
    uninstall_launchd
    ;;
  status)
    status_cron
    ;;
  run-now)
    run_now
    ;;
  show-freehost|show-hosting)
    show_freehost
    ;;
  *)
    usage
    exit 1
    ;;
esac
