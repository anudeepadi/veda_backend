import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
RIG_VEDA_DATA_PATH = os.getenv("RIG_VEDA_DATA_PATH")
AUDIO_BASE_DIR = os.getenv("AUDIO_BASE_DIR")