#!/usr/bin/env bash
# Деплой на VPS Ubuntu (gunicorn + nginx + PostgreSQL)
# Сервер: 178.20.157.42
#
# Перший раз (після bootstrap.sh):
#   bash scripts/deploy_vps.sh install
#
# Оновлення:
#   bash scripts/deploy_vps.sh update

set -o errexit
set -o pipefail

source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

PROJECT_DIR="$(project_dir)"
cd "$PROJECT_DIR"

load_env_file "$PROJECT_DIR/.env"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"
PYTHON_BIN="$(resolve_python_bin "$PROJECT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"
APP_USER="${APP_USER:-deploy}"

usage() {
  cat <<EOF
Використання: bash scripts/deploy_vps.sh <команда>

Команди:
  install       venv, pip, migrate, collectstatic, seed, systemd, nginx hint
  update        pip, migrate, compilemessages, collectstatic, restart gunicorn
  restart       systemctl restart itmcopy
  status        gunicorn + nginx + timer status
  check         django check --deploy
  enable-cron   systemd timer для fetch_market_news

Шлях на сервері: /var/www/itmcopy
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
  echo "→ Залежності…"
  "$PYTHON_BIN" -m pip install --upgrade pip
  "$PYTHON_BIN" -m pip install -r "$PROJECT_DIR/requirements.txt"
}

run_migrations() {
  echo "→ Міграції…"
  "$PYTHON_BIN" manage.py migrate --noinput
}

compile_locales() {
  echo "→ Переклади…"
  bash "$PROJECT_DIR/scripts/compile_locales.sh"
}

collect_static() {
  echo "→ collectstatic…"
  "$PYTHON_BIN" manage.py collectstatic --noinput --clear
}

seed_if_empty() {
  if "$PYTHON_BIN" manage.py shell -c "from apps.core.models import SiteSettings; print(SiteSettings.objects.exists())" 2>/dev/null | grep -q True; then
    echo "→ Seed пропущено"
    return 0
  fi
  echo "→ Seed БД…"
  "$PYTHON_BIN" manage.py seed_db --with-market-news
}

django_check() {
  "$PYTHON_BIN" manage.py check --deploy
}

install_systemd() {
  if [[ "$(id -u)" -ne 0 ]]; then
    echo "→ systemd: потрібен root (sudo bash scripts/deploy_vps.sh install)"
    return 0
  fi
  cp "$PROJECT_DIR/deploy/vps/systemd/itmcopy.service" /etc/systemd/system/
  cp "$PROJECT_DIR/deploy/vps/systemd/itmcopy-cron.service" /etc/systemd/system/
  cp "$PROJECT_DIR/deploy/vps/systemd/itmcopy-cron.timer" /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable itmcopy.service
  systemctl restart itmcopy.service
  systemctl enable itmcopy-cron.timer
  systemctl start itmcopy-cron.timer
  echo "✓ systemd: itmcopy + itmcopy-cron.timer"
}

install_nginx() {
  if [[ "$(id -u)" -ne 0 ]]; then
    return 0
  fi
  cp "$PROJECT_DIR/deploy/vps/nginx/http.conf" /etc/nginx/sites-available/itmcopy
  ln -sf /etc/nginx/sites-available/itmcopy /etc/nginx/sites-enabled/itmcopy
  rm -f /etc/nginx/sites-enabled/default
  nginx -t
  systemctl reload nginx
  echo "✓ nginx: sites-enabled/itmcopy"
}

fix_permissions() {
  if [[ "$(id -u)" -ne 0 ]]; then
    return 0
  fi
  chown -R "$APP_USER:$APP_USER" "$PROJECT_DIR"
  chmod +x "$PROJECT_DIR/scripts/"*.sh
}

cmd_install() {
  ensure_venv
  pip_install
  mkdir -p "$PROJECT_DIR/logs" "$PROJECT_DIR/media" "$PROJECT_DIR/tmp"
  compile_locales
  run_migrations
  collect_static
  seed_if_empty
  django_check
  fix_permissions
  install_systemd
  install_nginx
  echo ""
  echo "✓ VPS deploy готовий"
  echo "  curl -sf http://127.0.0.1/healthz/"
  echo "  curl -sf http://led-leader.com.ua/healthz/"
  echo "  createsuperuser: sudo -u $APP_USER $VENV_DIR/bin/python manage.py createsuperuser"
}

cmd_update() {
  ensure_venv
  pip_install
  compile_locales
  run_migrations
  collect_static
  django_check
  if [[ "$(id -u)" -eq 0 ]]; then
    systemctl restart itmcopy.service
    echo "✓ gunicorn перезапущено"
  else
    echo "→ Перезапуск: sudo systemctl restart itmcopy"
  fi
}

cmd_restart() {
  systemctl restart itmcopy.service
}

cmd_status() {
  systemctl status itmcopy.service --no-pager || true
  systemctl status itmcopy-cron.timer --no-pager || true
  systemctl list-timers itmcopy-cron.timer --no-pager || true
}

cmd_enable_cron() {
  if [[ "$(id -u)" -ne 0 ]]; then
    echo "Потрібен sudo" >&2
    exit 1
  fi
  install_systemd
}

case "${1:-}" in
  install) cmd_install ;;
  update) cmd_update ;;
  restart) cmd_restart ;;
  status) cmd_status ;;
  check) ensure_venv; django_check ;;
  enable-cron) cmd_enable_cron ;;
  *)
    usage
    exit 1
    ;;
esac
