import os
import environ
from datetime import timedelta

env = environ.Env()
environ.Env.read_env()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key"  # Cambia esto por un valor seguro
    JWT_SECRET_KEY = (
        "your-jwt-secret-key"  # Cambia esto por un valor seguro si usas JWT
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
