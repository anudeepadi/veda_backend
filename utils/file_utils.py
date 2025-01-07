from pathlib import Path
from config import AUDIO_BASE_DIR

def get_audio_file_path(mandala: int, hymn: int) -> Path:
    audio_path = Path(AUDIO_BASE_DIR) / str(mandala) / f"{hymn}.mp3"
    print(f"Constructed audio path: {audio_path}")  # Add this line for debugging
    return audio_path

def format_file_path(path: Path) -> str:
    return str(path).replace("\\", "/") 