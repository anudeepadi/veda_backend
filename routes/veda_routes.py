from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import json
import os

router = APIRouter()

def load_veda_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, '..', 'data', 'rig_veda_formatted_combined.json')
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading veda data: {e}")
        return None

@router.get("/api/veda/all")
async def get_all_veda_data():
    data = load_veda_data()
    if not data:
        raise HTTPException(status_code=500, detail="Error loading veda data")
    return JSONResponse(content=data)

@router.get("/api/veda/mandala/{mandala_id}")
async def get_mandala(mandala_id: int):
    data = load_veda_data()
    if not data:
        raise HTTPException(status_code=500, detail="Error loading veda data")
    
    mandala = next((m for m in data if m["id"] == mandala_id), None)
    if not mandala:
        raise HTTPException(status_code=404, detail=f"Mandala {mandala_id} not found")
    
    return JSONResponse(content=mandala)

@router.get("/api/veda/search")
async def search_verses(query: str):
    data = load_veda_data()
    if not data:
        raise HTTPException(status_code=500, detail="Error loading veda data")
    
    results = []
    for mandala in data:
        for hymn in mandala["hymns"]:
            for verse in hymn["verses"]:
                if query.lower() in verse["text"].lower() or query.lower() in verse["translation"].lower():
                    results.append({
                        "mandala_id": mandala["id"],
                        "hymn_id": hymn["id"],
                        "verse": verse
                    })
    
    return JSONResponse(content=results)