from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from services.openai_service import generate_vedic_quiz, compare_hymns, generate_meditation, ask_question
from utils.security import get_api_key
from services.openai_service import call_openai_api

router = APIRouter()

@router.get("/vedic-quiz")
async def generate_vedic_quiz_route(num_questions: int = Query(5, ge=1, le=10)):
    try:
        # Generate the quiz synchronously
        result = await generate_vedic_quiz(num_questions)
        return {"status": "completed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@router.get("/comparative-analysis")
async def compare_hymns_route(mandala1: int, hymn1: int, mandala2: int, hymn2: int):
    try:
        # Compare the hymns synchronously
        result = await compare_hymns(mandala1, hymn1, mandala2, hymn2)
        return {"status": "completed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing hymns: {str(e)}")

@router.get("/generate-meditation")
async def generate_meditation_route(hymn: int):
    try:
        # Generate meditation synchronously
        result = await generate_meditation(hymn)
        return {"status": "completed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating meditation: {str(e)}")

@router.get("/ask-question")
async def ask_question_route(question: str):
    try:
        # Ask a question synchronously
        answer = await ask_question(question)
        return JSONResponse(content={"question": question, "answer": answer})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting answer: {str(e)}")

@router.get("/test-openai-connection")
async def test_openai_connection():
    try:
        # Test the OpenAI connection synchronously
        response = await call_openai_api([{"role": "user", "content": "Hello"}])
        return {"status": "success", "message": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
