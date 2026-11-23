import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET = os.getenv("JWT_SECRET")
    ENC_KEY = os.getenv("ENC_KEY")

    LAB_IP = os.getenv("LAB_IP", "127.0.0.1")
    COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"