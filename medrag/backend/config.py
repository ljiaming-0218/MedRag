from pathlib import Path
from os import environ
from dotenv import load_dotenv



BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


CHROMA_DIR = Path(environ["CHROMA_DIR"])
UPLOAD_DIR = Path(environ["UPLOAD_DIR"])
MONGODB_URI = environ.get("MONGODB_URI")
MONGODB_DB_NAME = environ.get("MONGODB_DB_NAME")
OPENROUTER_API_KEY = environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = environ.get("OPENROUTER_BASE_URL")
OPENROUTER_MODEL = environ.get("OPENROUTER_MODEL")
