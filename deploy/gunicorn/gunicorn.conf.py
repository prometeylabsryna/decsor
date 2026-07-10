"""Gunicorn config for FREEhost VPS (Linux + ISPmanager / nginx)."""
import multiprocessing
import os

bind = os.getenv("GUNICORN_BIND", "127.0.0.1:8001")
workers = int(os.getenv("GUNICORN_WORKERS", max(2, multiprocessing.cpu_count() * 2 + 1)))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "120"))
keepalive = 5
wsgi_app = "config.wsgi:application"
accesslog = "-"
errorlog = "-"
capture_output = True
