# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.responses import JSONResponse
# from services.hymn_service import get_hymn_by_id
# from services.nlp_service import analyze_sentiment, generate_word_frequency_chart
# from services.openai_service import analyze_hymn_themes, get_modern_interpretation, explain_hymn
# from utils.security import get_api_key

# router = APIRouter()

# @router.get("/thematic-analysis/{mandala}/{hymn}")
# async def analyze_hymn_themes_route(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = get_hymn_by_id(mandala, hymn)
#     if not hymn_data:
#         raise HTTPException(status_code=404, detail="Hymn not found")
#     analysis = await analyze_hymn_themes(hymn_data)
#     return JSONResponse(content={"hymn": hymn_data.dict(), "thematic_analysis": analysis})

# @router.get("/modern-interpretation/{mandala}/{hymn}")
# async def get_modern_interpretation_route(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = get_hymn_by_id(mandala, hymn)
#     if not hymn_data:
#         raise HTTPException(status_code=404, detail="Hymn not found")
#     interpretations = await get_modern_interpretation(hymn_data)
#     return JSONResponse(content={
#         "hymn": hymn_data.dict(), 
#         "modern_interpretations": [interpretation.dict() for interpretation in interpretations]
#     })

# @router.get("/explain/{mandala}/{hymn}")
# async def explain_hymn_route(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = get_hymn_by_id(mandala, hymn)
#     if not hymn_data:
#         raise HTTPException(status_code=404, detail="Hymn not found")
#     explanation = await explain_hymn(hymn_data)
#     return JSONResponse(content={"hymn": hymn_data.dict(), "explanation": explanation})

# @router.get("/sentiment/{mandala}/{hymn}")
# async def get_hymn_sentiment(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = get_hymn_by_id(mandala, hymn)
#     if not hymn_data:
#         raise HTTPException(status_code=404, detail="Hymn not found")
#     text = " ".join([verse.translation for verse in hymn_data.verses])
#     sentiment = analyze_sentiment(text)
#     return {"hymn": hymn_data.dict(), "sentiment": sentiment}

# @router.get("/visualize/word-frequency/{mandala}/{hymn}")
# async def visualize_word_frequency(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = get_hymn_by_id(mandala, hymn)
#     if not hymn_data:
#         raise HTTPException(status_code=404, detail="Hymn not found")
#     chart_data = generate_word_frequency_chart(hymn_data)
#     return JSONResponse(content={"hymn": hymn_data.dict(), "word_frequency_chart": chart_data})