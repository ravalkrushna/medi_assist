from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
