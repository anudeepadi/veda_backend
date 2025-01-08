from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from services.nlp_service import NLPService

router = APIRouter()
nlp_service = NLPService()

class VerseAnalysisRequest(BaseModel):
    sanskrit: str
    translation: str

class SearchRequest(BaseModel):
    query: str
    verses: List[dict]

class RecommendationRequest(BaseModel):
    current_verse: dict
    verses: List[dict]

class ThematicAnalysisRequest(BaseModel):
    verses: List[dict]

@router.post("/analyze-verse")
async def analyze_verse(request: VerseAnalysisRequest):
    """Analyze a single verse using NLP"""
    try:
        analysis = await nlp_service.analyze_verse({
            "sanskrit": request.sanskrit,
            "translation": request.translation
        })
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/semantic-search")
async def semantic_search(request: SearchRequest):
    """Perform semantic search across verses"""
    try:
        results = await nlp_service.semantic_search(request.query, request.verses)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get-recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get verse recommendations"""
    try:
        recommendations = await nlp_service.get_recommendations(
            request.current_verse, request.verses
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/thematic-analysis")
async def thematic_analysis(request: ThematicAnalysisRequest):
    """Perform thematic analysis on verses"""
    try:
        analysis = await nlp_service.thematic_analysis(request.verses)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))