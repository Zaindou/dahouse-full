import os
from dotenv import load_dotenv
from datetime import timedelta

env_file = ".env.dev" if os.environ.get("FLASK_ENV") == "development" else ".env"

print(f"Cargando configuración desde {env_file}")  # Depuración
load_dotenv(env_file)


class Config:
    # DATABASE CONFIG
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,          # Número de conexiones activas en el pool
        "max_overflow": 5,        # Conexiones extra permitidas
        "pool_recycle": 1800,     # Recicla conexiones cada 30 min
        "pool_pre_ping": True,    # Detecta conexiones cerradas y las reabre
        "pool_timeout": 10,       # Espera hasta 10 seg antes de fallar en obtener conexión
        "connect_args": {"connect_timeout": 30}  # Espera hasta 30 seg al conectar
    }

    # JWT CONFIG
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "default-secret-key"
    )  # Cambia esto por un valor seguro
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    # MAIL CONFIG
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"

    # SMS Configuración
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

    # NOMINA API
    NOMINA_API_URL = os.getenv("NOMINA_API_URL", "")
