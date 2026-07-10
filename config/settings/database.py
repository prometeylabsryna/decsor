"""Database configuration for dev and production (PostgreSQL / MySQL)."""
import os

import dj_database_url


def _mysql_options() -> dict:
    return {
        "charset": "utf8mb4",
        "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
    }


def build_databases() -> dict:
    """
    Resolve DATABASES from env.

  Priority:
    1. DATABASE_URL (mysql://… or postgresql://…)
    2. DB_ENGINE + DB_* variables
    """
    database_url = os.getenv("DATABASE_URL", "").strip()
    if database_url:
        cfg = dj_database_url.parse(database_url, conn_max_age=600)
        if cfg.get("ENGINE", "").endswith("mysql"):
            cfg.setdefault("OPTIONS", {}).update(_mysql_options())
        return {"default": cfg}

    engine = os.getenv("DB_ENGINE", "postgresql").strip().lower()
    if engine in ("mysql", "mariadb"):
        return {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.getenv("DB_NAME", "itmcopy"),
                "USER": os.getenv("DB_USER", ""),
                "PASSWORD": os.getenv("DB_PASSWORD", ""),
                "HOST": os.getenv("DB_HOST", "localhost"),
                "PORT": os.getenv("DB_PORT", "3306"),
                "OPTIONS": _mysql_options(),
                "CONN_MAX_AGE": 600,
            }
        }

    return {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "ltm_db"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
            "CONN_MAX_AGE": 600,
        }
    }
