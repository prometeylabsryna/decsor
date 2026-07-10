#!/usr/bin/env bash
# Одноразове налаштування VPS Ubuntu 24.04 (FREEhost dedicated 178.20.157.42)
# Запуск на сервері від root:
#   curl -sO .../bootstrap.sh && bash bootstrap.sh
# або після git clone:
#   bash /var/www/itmcopy/deploy/vps/bootstrap.sh

set -o errexit
set -o pipefail

APP_USER="${APP_USER:-deploy}"
APP_DIR="${APP_DIR:-/var/www/itmcopy}"
APP_GROUP="${APP_GROUP:-$APP_USER}"

echo "==> Оновлення системи"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get upgrade -y -qq

echo "==> Пакети: Python, PostgreSQL, nginx, certbot, git"
apt-get install -y -qq \
  python3 python3-venv python3-pip python3-dev \
  postgresql postgresql-contrib libpq-dev \
  nginx certbot python3-certbot-nginx \
  git rsync gettext \
  ufw fail2ban

echo "==> Користувач $APP_USER"
if ! id "$APP_USER" &>/dev/null; then
  useradd -m -s /bin/bash "$APP_USER"
fi

echo "==> Каталог застосунку $APP_DIR"
mkdir -p "$APP_DIR"
chown -R "$APP_USER:$APP_GROUP" "$APP_DIR"

echo "==> PostgreSQL"
if [[ -f "$APP_DIR/.env" ]]; then
  # shellcheck disable=SC1090
  source "$APP_DIR/.env"
fi
DB_NAME="${POSTGRES_DB:-itmcopy}"
DB_USER="${POSTGRES_USER:-itmcopy}"
DB_PASS="${POSTGRES_PASSWORD:-}"

if [[ -z "$DB_PASS" || "$DB_PASS" == CHANGE_ME* ]]; then
  DB_PASS="$(openssl rand -base64 24 | tr -d '/+=' | head -c 32)"
  echo "  Згенеровано пароль БД (збережіть у .env): $DB_PASS"
fi

sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1 \
  || sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1 \
  || sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "==> Firewall"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "==> nginx + systemd"
systemctl enable nginx
systemctl start nginx

cat <<EOF

✓ Bootstrap завершено.

Далі:
  1. Завантажте проєкт у $APP_DIR (git clone / rsync)
  2. cp deploy/vps/env.production.example $APP_DIR/.env
     POSTGRES_PASSWORD=$DB_PASS
  3. bash $APP_DIR/scripts/deploy_vps.sh install
  4. cp $APP_DIR/deploy/vps/nginx/http.conf /etc/nginx/sites-available/itmcopy
     ln -sf /etc/nginx/sites-available/itmcopy /etc/nginx/sites-enabled/itmcopy
     rm -f /etc/nginx/sites-enabled/default
     nginx -t && systemctl reload nginx
  5. DNS: A @ і www → 178.20.157.42
  6. SSL:
     certbot --nginx -d led-leader.com.ua -d www.led-leader.com.ua
     # у .env: CSRF_TRUSTED_ORIGINS=https://led-leader.com.ua,https://www.led-leader.com.ua
     # SECURE_SSL_REDIRECT=True && bash scripts/deploy_vps.sh update

EOF
