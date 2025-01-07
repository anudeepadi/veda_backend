from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from models.schemas import Hymn, Verse
from services.hymn_service import get_all_hymns, get_hymn_by_id, get_hymn_verses
from utils.security import get_api_key
import os 
import jsonify
import requests

router = APIRouter()

@router.get("/hymns", response_model=List[Hymn])
async def get_hymns(mandala: Optional[int] = Query(None, description="Filter by Mandala number"),
                    api_key: str = Depends(get_api_key)):
    return get_all_hymns(mandala)

@router.get("/hymns/{mandala}/{hymn}", response_model=Hymn)
async def get_hymn(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
    hymn_data = get_hymn_by_id(mandala, hymn)
    if not hymn_data:
        raise HTTPException(status_code=404, detail="Hymn not found")
    return hymn_data

@router.get('/audio/<int:mandala>/<int:hymn>')
def get_audio(mandala, hymn):
    audio_path = f"data/audio_data/{mandala}/{hymn}.mp3"
    if os.path.exists(audio_path):
        return jsonify({
            "audio_url": f"{requests.host_url}static/audio/{mandala}/{hymn}.mp3"
        })
    else:
        return jsonify({"error": "Audio file not found"}), 404

# @router.get("/hymns/{mandala}/{hymn}/verses", response_model=List[Verse])
# async def get_hymn_verses(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     verses = get_hymn_verses(mandala, hymn)
#     if not verses:
#         raise HTTPException(status_code=404, detail="Hymn not found")
#     return verses