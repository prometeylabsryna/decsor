"""Project package — PyMySQL shim for MySQL on shared hosting (FreeBSD / FREEhost)."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

if os.getenv("DB_ENGINE", "").strip().lower() in ("mysql", "mariadb"):
    import pymysql

    pymysql.install_as_MySQLdb()
