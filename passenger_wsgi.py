"""
Entry point for Passenger / FREEhost shared hosting.

Панель: корінь застосунку = каталог проєкту, startup file = passenger_wsgi.py,
entry point = application.

Після змін: touch tmp/restart.txt
"""
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, ".venv")

# Використати Python з віртуального середовища (якщо є)
INTERP = os.path.join(VENV_DIR, "bin", "python")
if os.path.isfile(INTERP) and sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
