import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROJECTS_DIR = DATA_DIR / "projects"
UPLOADS_DIR = BASE_DIR / "meetings"
SUMMARIES_DIR = DATA_DIR / "generated_summaries"
DATABASE_DIR = DATA_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "app.db"
DATASET_DIR = BASE_DIR / "dataset"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:270m")
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "25"))
OLLAMA_RETRY_COUNT = int(os.getenv("OLLAMA_RETRY_COUNT", "2"))
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")


def ensure_directories() -> None:
    for path in [DATA_DIR, PROJECTS_DIR, UPLOADS_DIR, SUMMARIES_DIR, DATABASE_DIR]:
        path.mkdir(parents=True, exist_ok=True)
