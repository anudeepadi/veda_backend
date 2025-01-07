from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Verse(BaseModel):
    number: int
    sanskrit: str
    transliteration: Optional[str] = None
    translation: str
    commentary: Optional[str] = None

class Hymn(BaseModel):
    number: int
    title: str
    verses: List[Verse]

class Mandala(BaseModel):
    number: int
    hymns: List[Hymn]

# Load data from JSON file
def load_hymn_data():
    try:
        with open(r"C:\Users\Adi\Projects\vedam\veda-backend\data\rig_veda_formatted_combined.json", "r", encoding="utf-8") as f:
            logger.info("Successfully loaded hymn data from file.")
            return json.load(f)
    except FileNotFoundError:
        logger.error("Hymn data file not found.")
        return {"mandalas": []}

hymn_data = load_hymn_data()

@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to Veda Explorer API"}

@app.get("/api/hymns")
async def get_hymns():
    logger.info("Fetching all hymns.")
    hymns = [hymn for mandala in hymn_data["mandalas"] for hymn in mandala["hymns"]]
    return {"hymns": hymns}

@app.get("/api/hymns/{mandala}")
async def get_hymns_by_mandala(mandala: int):
    logger.info(f"Fetching hymns for Mandala {mandala}.")
    mandala_data = next((m for m in hymn_data["mandalas"] if m["number"] == mandala), None)
    if not mandala_data:
        logger.warning(f"No hymns found for Mandala {mandala}.")
        raise HTTPException(status_code=404, detail=f"No hymns found for Mandala {mandala}")
    return {"hymns": mandala_data["hymns"]}

@app.get("/api/hymns/{mandala}/{hymn}")
async def get_hymn(mandala: int, hymn: int):
    if not hymn_data.get("mandalas"):
        logger.warning("No hymn data available.")
        raise HTTPException(status_code=500, detail="Hymn data is not available.")
    logger.info(f"Fetching Hymn {hymn} from Mandala {mandala}.")
    mandala_data = next((m for m in hymn_data["mandalas"] if m["number"] == mandala), None)
    if not mandala_data:
        logger.warning(f"No hymns found for Mandala {mandala}.")
        raise HTTPException(status_code=404, detail=f"No hymns found for Mandala {mandala}")
    hymn_entry = next((h for h in mandala_data["hymns"] if h["number"] == hymn), None)
    if not hymn_entry:
        logger.warning(f"Hymn {hymn} not found in Mandala {mandala}.")
        raise HTTPException(status_code=404, detail=f"Hymn {hymn} not found in Mandala {mandala}")
    return hymn_entry

@app.get("/api/search")
async def search_hymns(query: str):
    logger.info(f"Searching hymns with query: {query}")
    results = []
    query = query.lower()
    for mandala in hymn_data["mandalas"]:
        for hymn in mandala["hymns"]:
            for verse in hymn["verses"]:
                if (query in verse["sanskrit"].lower() or 
                    query in verse["translation"].lower() or 
                    (verse.get("transliteration") and query in verse["transliteration"].lower())):
                    results.append({
                        "mandala": mandala["number"],
                        "hymn_number": hymn["number"],
                        "verse_number": verse["number"],
                        "verse": verse
                    })
    if not results:
        logger.info("No results found for search query.")
    return {"results": results}
