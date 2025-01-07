from typing import List, Optional
from models.schemas import Hymn, Verse
from utils.data_loader import RIG_VEDA_DATA
from utils.file_utils import get_audio_file_path, format_file_path
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

AUDIO_BASE_DIR = Path(r"C:\Users\anude\Projects\vedam\veda-backend\rv-audio\audio_data")

def get_all_hymns(mandala: Optional[int] = None) -> List[Hymn]:
    try:
        hymns = []
        for m in RIG_VEDA_DATA['mandalas']:
            if mandala is None or m['number'] == mandala:
                for h in m['hymns']:
                    audio_file = get_audio_file_path(m['number'], h['number'])
                    hymns.append(Hymn(
                        mandala=m['number'],
                        hymn_number=h['number'],
                        title=h['title'],
                        verses=[Verse(**v) for v in h['verses']],
                        audio_file=audio_file
                    ))
        return hymns
    except Exception as e:
        logger.error(f"Error in get_all_hymns: {str(e)}")
        raise

def get_hymn_by_id(mandala: int, hymn: int) -> Optional[Hymn]:
    try:
        for m in RIG_VEDA_DATA['mandalas']:
            if m['number'] == mandala:
                for h in m['hymns']:
                    if h['number'] == hymn:
                        verses = [Verse(**v) for v in h['verses']]
                        audio_file = get_audio_file_path(mandala, hymn)
                        return Hymn(
                            mandala=mandala,
                            hymn_number=hymn,
                            title=f"Rig Veda Mandala {mandala} Hymn {hymn}",
                            verses=verses,
                            audio_file=audio_file
                        )
        logger.warning(f"Hymn not found: Mandala {mandala}, Hymn {hymn}")
        return None
    except Exception as e:
        logger.error(f"Error in get_hymn_by_id: {str(e)}")
        raise
    
def get_audio_file_path(mandala: int, hymn: int) -> Optional[str]:
    audio_path = AUDIO_BASE_DIR / str(mandala) / f"{hymn}.mp3"
    return format_file_path(str(audio_path)) if audio_path.exists() else None

def get_hymn_verses(mandala: int, hymn: int) -> Optional[List[Verse]]:
    hymn_data = get_hymn_by_id(mandala, hymn)
    return hymn_data.verses if hymn_data else None

def search_hymns(query: str, search_sanskrit: bool, search_transliteration: bool, search_translation: bool) -> List[Hymn]:
    results = []
    for m in RIG_VEDA_DATA['mandalas']:
        for h in m['hymns']:
            hymn_matches = False
            matching_verses = []
            for v in h['verses']:
                verse_matches = (
                    (search_sanskrit and query.lower() in v['sanskrit'].lower()) or
                    (search_transliteration and query.lower() in v['transliteration'].lower()) or
                    (search_translation and query.lower() in v['translation'].lower())
                )
                if verse_matches:
                    hymn_matches = True
                    matching_verses.append(Verse(**v))
            if hymn_matches:
                audio_file = get_audio_file_path(m['number'], h['number'])
                results.append(Hymn(
                    mandala=m['number'],
                    hymn_number=h['number'],
                    title=h['title'],
                    verses=matching_verses,
                    audio_file=format_file_path(str(audio_file)) if audio_file.exists() else None
                ))
    return results