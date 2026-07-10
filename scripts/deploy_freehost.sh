#!/usr/bin/env bash
# Деплой на FREEhost.UA (віртуальний хостинг FreeBSD або VPS Linux).
#
# Перший деплой (SSH):
#   cp .env.example .env   # заповнити production-значення
#   bash scripts/deploy_freehost.sh install
#
# Оновлення після git pull:
#   bash scripts/deploy_freehost.sh update
#
# Push-to-deploy: див. deploy/git/post-receive.hook.template

set -o errexit
set -o pipefail

source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

PROJECT_DIR="$(project_dir)"
cd "$PROJECT_DIR"

load_env_file "$PROJECT_DIR/.env"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"
PYTHON_BIN="$(resolve_python_bin "$PROJECT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"
HTACCESS_TEMPLATE="$PROJECT_DIR/public/.htaccess.template"
HTACCESS_OUT="$PROJECT_DIR/public/.htaccess"
RESTART_FILE="$PROJECT_DIR/tmp/restart.txt"

usage() {
  cat <<EOF
Використання: bash scripts/deploy_freehost.sh <команда>

Команди:
  install     Перший деплой: venv, залежності, migrate, collectstatic, seed
  update      Оновлення: залежності, migrate, compilemessages, collectstatic, restart
  htaccess    Згенерувати public/.htaccess з шаблону
  restart     Перезапустити Passenger (touch tmp/restart.txt)
  check       django check --deploy
  cron-info   Показати рядки cron / wget для панелі FREEhost

Змінні (.env):
  DJANGO_SETTINGS_MODULE=config.settings.production
  DB_ENGINE=mysql              # рекомендовано для shared FREEhost
  DATABASE_URL=mysql://user:pass@localhost:3306/dbname
  ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, SECRET_KEY
  CRON_SECRET_TOKEN            # для wget-імпорту новин
EOF
}

ensure_venv() {
  if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    echo "→ Створення venv…"
    python3 -m venv "$VENV_DIR"
  fi
  PYTHON_BIN="$VENV_DIR/bin/python"
}

pip_install() {
  echo "→ Встановлення залежностей…"
  "$PYTHON_BIN" -m pip install --upgrade pip
  "$PYTHON_BIN" -m pip install -r "$PROJECT_DIR/requirements.txt"
}

generate_htaccess() {
  if [[ ! -f "$HTACCESS_TEMPLATE" ]]; then
    echo "Шаблон не знайдено: $HTACCESS_TEMPLATE" >&2
    return 1
  fi

  local python_path="${PYTHON_BIN:-$VENV_DIR/bin/python}"
  sed \
    -e "s|__PROJECT_DIR__|$PROJECT_DIR|g" \
    -e "s|__PYTHON_BIN__|$python_path|g" \
    "$HTACCESS_TEMPLATE" > "$HTACCESS_OUT"

  echo "✓ Згенеровано $HTACCESS_OUT"
  echo "  У панелі FREEhost вкажіть document root → public/"
}

restart_passenger() {
  mkdir -p "$PROJECT_DIR/tmp"
  touch "$RESTART_FILE"
  echo "✓ Passenger restart: $RESTART_FILE"
}

run_migrations() {
  echo "→ Міграції…"
  "$PYTHON_BIN" manage.py migrate --noinput
}

compile_locales() {
  echo "→ Компіляція перекладів…"
  bash "$PROJECT_DIR/scripts/compile_locales.sh"
}

collect_static() {
  echo "→ collectstatic…"
  "$PYTHON_BIN" manage.py collectstatic --noinput --clear
}

seed_if_empty() {
  if "$PYTHON_BIN" manage.py shell -c "from apps.core.models import SiteSettings; print(SiteSettings.objects.exists())" 2>/dev/null | grep -q True; then
    echo "→ Seed пропущено (дані вже є)"
    return 0
  fi
  echo "→ Початкове заповнення БД…"
  "$PYTHON_BIN" manage.py seed_db --with-market-news
}

django_check() {
  "$PYTHON_BIN" manage.py check --deploy
}

cmd_install() {
  ensure_venv
  pip_install
  mkdir -p "$PROJECT_DIR/logs" "$PROJECT_DIR/media" "$PROJECT_DIR/tmp"
  compile_locales
  run_migrations
  collect_static
  seed_if_empty
  generate_htaccess
  restart_passenger
  django_check
  echo ""
  echo "✓ Деплой завершено. Далі:"
  echo "  1. Панель FREEhost → document root = public/"
  echo "  2. bash scripts/setup_market_news_cron.sh show-freehost"
  echo "  3. Створити суперкористувача: $PYTHON_BIN manage.py createsuperuser"
}

cmd_update() {
  ensure_venv
  pip_install
  compile_locales
  run_migrations
  collect_static
  generate_htaccess
  restart_passenger
  django_check
  echo "✓ Оновлення завершено"
}

cron_info() {
  load_env_file "$PROJECT_DIR/.env"
  local domain="${DEPLOY_DOMAIN:-yourdomain.com}"
  local token="${CRON_SECRET_TOKEN:-YOUR_CRON_SECRET}"
  local schedule="${MARKET_NEWS_CRON_SCHEDULE:-0 */6 * * *}"

  cat <<EOF
FREEhost → Планувальник CRON:

1) Командний рядок (SSH, шаблон «Мінімальний»+):
   $schedule /bin/bash $PROJECT_DIR/scripts/fetch_market_news.sh

2) Метод wget (без Python у cron):
   $schedule wget -q -O /dev/null "https://$domain/cron/fetch-market-news/?token=$token"

Перед wget встановіть CRON_SECRET_TOKEN у .env і перезапустіть застосунок.
Лог CLI: $PROJECT_DIR/logs/fetch_news.log
EOF
}

case "${1:-}" in
  install) cmd_install ;;
  update) cmd_update ;;
  htaccess) ensure_venv; generate_htaccess ;;
  restart) restart_passenger ;;
  check) ensure_venv; django_check ;;
  cron-info) cron_info ;;
  *)
    usage
    exit 1
    ;;
esac
