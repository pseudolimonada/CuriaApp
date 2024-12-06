import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

APP_PORT = os.getenv("APP_PORT", 4000)
APP_URL = os.getenv("APP_URL", "http://127.0.0.1")
SECRET_KEY = os.getenv("SECRET_KEY", "copilot_made_me_laugh")


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"postgresql://{os.getenv("DB_USER")}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Print the database configuration to verify
print(f"Database configuration: {Config.SQLALCHEMY_DATABASE_URI}")
