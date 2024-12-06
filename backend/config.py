import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://admin:admin@localhost/pgi2024"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Print the database configuration to verify
print(f"Database configuration: {Config.SQLALCHEMY_DATABASE_URI}")
