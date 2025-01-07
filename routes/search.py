from fastapi import APIRouter, Depends, Query
from typing import List
from models.schemas import Hymn
from services.hymn_service import search_hymns
from utils.security import get_api_key

router = APIRouter()

@router.get("/search", response_model=List[Hymn])
async def search_hymns_route(
    query: str = Query(..., description="Search query"),
    search_sanskrit: bool = Query(False, description="Search in Sanskrit text"),
    search_transliteration: bool = Query(False, description="Search in transliteration"),
    search_translation: bool = Query(True, description="Search in translation"),
    api_key: str = Depends(get_api_key)
):
    return search_hymns(query, search_sanskrit, search_transliteration, search_translation)

