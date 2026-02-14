import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

#Directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / 'uploads'
VECTOR_STORE_DIR  = BASE_DIR / 'vector_store'

#Create directories 
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

#settings
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN','')
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
