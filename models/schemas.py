from pydantic import BaseModel
from typing import List, Optional

class Verse(BaseModel):
    number: int
    sanskrit: str
    transliteration: str
    translation: str

class Hymn(BaseModel):
    mandala: int
    hymn_number: int
    title: str
    verses: List[Verse]
    audio_file: Optional[str] = None

class SimilarityResult(BaseModel):
    hymn: Hymn
    similarity_score: float

class ThematicAnalysis(BaseModel):
    theme: str
    description: str
    relevant_verses: List[Verse]

class ModernInterpretation(BaseModel):
    original_verse: Verse
    modern_interpretation: str

class VedicQuiz(BaseModel):
    question: str
    options: List[str]
    correct_answer: int

class BackgroundTask(BaseModel):
    id: str
    status: str
    result: Optional[dict] = None