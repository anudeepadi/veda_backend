# from fastapi import FastAPI, HTTPException, Query, Depends
# from fastapi.responses import FileResponse, JSONResponse
# from pydantic import BaseModel
# from typing import List, Optional, Dict
# import json
# from pathlib import Path
# import re
# from fastapi.middleware.cors import CORSMiddleware
# import os
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import matplotlib.pyplot as plt
# import io
# import base64
# from transformers import pipeline
# from fastapi.security import APIKeyHeader
# from starlette.status import HTTP_403_FORBIDDEN
# from dotenv import load_dotenv
# import openai
# import random

# openai.api_key = 'anything'  # Replace with your actual API key
# openai.base_url = "http://localhost:3040/v1/"  # Replace with your actual base URL


# # Load environment variables
# load_dotenv()

# app = FastAPI(title="Enhanced Rig Veda API", description="API for accessing Rig Veda data with AI and visualization features")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load JSON data
# def load_json_data(file_path: str):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)

# # Initialize data
# RIG_VEDA_DATA = load_json_data(r"C:\Users\anude\Projects\veda-backend\rig_veda_formatted_combined.json")

# # Base directory for audio files
# AUDIO_BASE_DIR = Path("C:/Users/anude/Projects/veda-backend/rv-audio/data")

# # Models
# class Verse(BaseModel):
#     number: int
#     sanskrit: str
#     transliteration: str
#     translation: str

# class Hymn(BaseModel):
#     mandala: int
#     hymn_number: int
#     title: str
#     verses: List[Verse]
#     audio_file: Optional[str]


# class SimilarityResult(BaseModel):
#     hymn: Hymn
#     similarity_score: float


# class ThematicAnalysis(BaseModel):
#     theme: str
#     description: str
#     relevant_verses: List[Verse]

# class ModernInterpretation(BaseModel):
#     original_verse: Verse
#     modern_interpretation: str

# class VedicQuiz(BaseModel):
#     question: str
#     options: List[str]
#     correct_answer: int

# async def call_openai_api(messages):
#     try:
#         response = await openai.ChatCompletion.acreate(
#             model="gpt-3.5-turbo",
#             messages=messages
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")

# # Helper functions
# def get_audio_file_path(mandala: int, hymn: int) -> Path:
#     return AUDIO_BASE_DIR / str(mandala) / f"{hymn}.mp3"

# def search_text(text: str, query: str) -> bool:
#     return re.search(query, text, re.IGNORECASE) is not None

# def format_file_path(path: Path) -> str:
#     return str(path).replace("\\", "/")

# # AI and NLP functions
# sentiment_analyzer = pipeline("sentiment-analysis")

# def analyze_sentiment(text: str) -> Dict[str, float]:
#     result = sentiment_analyzer(text)[0]
#     return {"label": result["label"], "score": result["score"]}

# def get_similar_hymns(query: str, top_n: int = 5) -> List[SimilarityResult]:
#     hymns = [hymn for mandala in RIG_VEDA_DATA['mandalas'] for hymn in mandala['hymns']]
#     corpus = [" ".join([verse['translation'] for verse in hymn['verses']]) for hymn in hymns]
    
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(corpus)
#     query_vector = vectorizer.transform([query])
    
#     cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
#     similar_indices = cosine_similarities.argsort()[-top_n:][::-1]
    
#     results = []
#     for idx in similar_indices:
#         hymn = hymns[idx]
#         results.append(SimilarityResult(
#             hymn=Hymn(
#                 mandala=hymn['mandala'],
#                 hymn_number=hymn['number'],
#                 title=hymn['title'],
#                 verses=[Verse(**v) for v in hymn['verses']],
#                 audio_file=format_file_path(get_audio_file_path(hymn['mandala'], hymn['number']))
#             ),
#             similarity_score=float(cosine_similarities[idx])
#         ))
    
#     return results

# # Update the generate_word_frequency_chart function to handle Hymn objects
# def generate_word_frequency_chart(hymn: Hymn) -> str:
#     text = " ".join([verse.translation for verse in hymn.verses])
#     words = re.findall(r'\w+', text.lower())
#     word_freq = {}
#     for word in words:
#         if word not in word_freq:
#             word_freq[word] = 1
#         else:
#             word_freq[word] += 1
    
#     sorted_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
#     plt.figure(figsize=(10, 6))
#     plt.bar([word for word, freq in sorted_freq], [freq for word, freq in sorted_freq])
#     plt.title(f"Top 10 Word Frequencies in Hymn {hymn.mandala}.{hymn.hymn_number}")
#     plt.xlabel("Words")
#     plt.ylabel("Frequency")
#     plt.xticks(rotation=45)
    
#     img_buffer = io.BytesIO()
#     plt.savefig(img_buffer, format='png')
#     img_buffer.seek(0)
#     img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
#     return f"data:image/png;base64,{img_str}"


# # Security
# API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

# def get_api_key(api_key_header: str = Depends(API_KEY_HEADER)):
#     if api_key_header != os.getenv("API_KEY"):
#         raise HTTPException(
#             status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
#         )
#     return api_key_header

# # Routes
# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Enhanced Rig Veda API"}

# @app.get("/testopenaiapi")
# async def test_openai_api():
#     response = await call_openai_api([
#         {"role": "system", "content": "You are an expert in Vedic literature."},
#         {"role": "user", "content": "What is the significance of Agni in the Rig Veda?"}
#     ])
#     return {"response": response}

# @app.get("/hymns", response_model=List[Hymn])
# async def get_hymns(mandala: Optional[int] = Query(None, description="Filter by Mandala number"),
#                     api_key: str = Depends(get_api_key)):
#     hymns = []
#     for m in RIG_VEDA_DATA['mandalas']:
#         if mandala is None or m['number'] == mandala:
#             for h in m['hymns']:
#                 audio_path = get_audio_file_path(m['number'], h['number'])
#                 hymns.append(Hymn(
#                     mandala=m['number'],
#                     hymn_number=h['number'],
#                     title=h['title'],
#                     verses=[Verse(**v) for v in h['verses']],
#                     audio_file=format_file_path(audio_path) if audio_path.exists() else None
#                 ))
#     return hymns

# # get all verses from a hymn
# @app.get("/hymns/{mandala}/{hymn}/verses", response_model=List[Verse])
# async def get_hymn_verses(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     for m in RIG_VEDA_DATA['mandalas']:
#         if m['number'] == mandala:
#             for h in m['hymns']:
#                 if h['number'] == hymn:
#                     return [Verse(**v) for v in h['verses']]
#     raise HTTPException(status_code=404, detail="Hymn not found")

# @app.get("/hymns/{mandala}/{hymn}", response_model=Hymn)
# async def get_hymn(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     for m in RIG_VEDA_DATA['mandalas']:
#         if m['number'] == mandala:
#             for h in m['hymns']:
#                 if h['number'] == hymn:
#                     audio_path = get_audio_file_path(mandala, hymn)
#                     return Hymn(
#                         mandala=mandala,
#                         hymn_number=hymn,
#                         title=h['title'],
#                         verses=[Verse(**v) for v in h['verses']],  # Include all verses
#                         audio_file=format_file_path(audio_path) if audio_path.exists() else None
#                     )
#     raise HTTPException(status_code=404, detail="Hymn not found")

# # Fix the similar hymns route
# @app.get("/similar", response_model=List[SimilarityResult])
# async def get_similar_hymns_route(
#     query: str = Query(..., description="Search query"),
#     top_n: int = Query(5, ge=1, le=20),
#     api_key: str = Depends(get_api_key)
# ):
#     return get_similar_hymns(query, top_n)

# @app.get("/search", response_model=List[Hymn])
# async def search_hymns(
#     query: str = Query(..., description="Search query"),
#     search_sanskrit: bool = Query(False, description="Search in Sanskrit text"),
#     search_transliteration: bool = Query(False, description="Search in transliteration"),
#     search_translation: bool = Query(True, description="Search in translation"),
#     api_key: str = Depends(get_api_key)
# ):
#     results = []
#     for m in RIG_VEDA_DATA['mandalas']:
#         for h in m['hymns']:
#             hymn_matches = False
#             matching_verses = []
#             for v in h['verses']:
#                 verse_matches = (
#                     (search_sanskrit and search_text(v['sanskrit'], query)) or
#                     (search_transliteration and search_text(v['transliteration'], query)) or
#                     (search_translation and search_text(v['translation'], query))
#                 )
#                 if verse_matches:
#                     hymn_matches = True
#                     matching_verses.append(Verse(**v))
#             if hymn_matches:
#                 audio_path = get_audio_file_path(m['number'], h['number'])
#                 results.append(Hymn(
#                     mandala=m['number'],
#                     hymn_number=h['number'],
#                     title=h['title'],
#                     verses=matching_verses,
#                     audio_file=format_file_path(audio_path) if audio_path.exists() else None
#                 ))
#     return results

# @app.get("/modern-interpretation/{mandala}/{hymn}")
# async def get_modern_interpretation(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = await get_hymn(mandala, hymn, api_key)
#     modern_interpretations = []
    
#     for verse in hymn_data.verses:
#         if verse is None or verse.translation is None:
#             continue  # Skip verses that are None or have no translation
#         prompt = f"Provide a modern interpretation or application of the following Rig Veda verse:\n\n{verse.translation}"
        
#         interpretation = await call_openai_api([
#             {"role": "system", "content": "You are an expert in connecting ancient wisdom to modern life."},
#             {"role": "user", "content": prompt}
#         ])
        
#         modern_interpretations.append(ModernInterpretation(original_verse=verse, modern_interpretation=interpretation))
    
#     return JSONResponse(content={"hymn": hymn_data.dict(), "modern_interpretations": [m.dict() for m in modern_interpretations]})

# @app.get("/thematic-analysis/{mandala}/{hymn}")
# async def analyze_hymn_themes(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = await get_hymn(mandala, hymn, api_key)
#     if not hymn_data or not hymn_data.verses:
#         raise HTTPException(status_code=404, detail="Hymn not found or has no verses")
    
#     hymn_text = "\n".join([verse.translation for verse in hymn_data.verses if verse and verse.translation])
    
#     if not hymn_text:
#         raise HTTPException(status_code=404, detail="No translations found for this hymn")
    
#     prompt = f"Analyze the following Rig Veda hymn and identify its main themes. For each theme, provide a brief description and list the most relevant verses:\n\n{hymn_text}"
    
#     response = await call_openai_api([
#         {"role": "system", "content": "You are an expert in Vedic literature analysis."},
#         {"role": "user", "content": prompt}
#     ])
    
#     return JSONResponse(content={"hymn": hymn_data.dict(), "thematic_analysis": response})

# @app.get("/explain/{mandala}/{hymn}")
# async def explain_hymn(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     try:
#         hymn_data = await get_hymn(mandala, hymn, api_key)
        
#         if not hymn_data or not hymn_data.verses:
#             raise HTTPException(status_code=404, detail="Hymn not found or has no verses")
        
#         hymn_text = f"Rig Veda Hymn {mandala}.{hymn}\n\n"
#         hymn_text += f"Title: {hymn_data.title}\n\n"
#         for verse in hymn_data.verses:
#             if verse and verse.translation:
#                 hymn_text += f"Verse {verse.number}:\n"
#                 hymn_text += f"Sanskrit: {verse.sanskrit}\n"
#                 hymn_text += f"Transliteration: {verse.transliteration}\n"
#                 hymn_text += f"Translation: {verse.translation}\n\n"
        
#         prompt = f"Please explain the following hymn from the Rig Veda, including its context, meaning, and significance:\n\n{hymn_text}"
        
#         explanation = await call_openai_api([
#             {"role": "system", "content": "You are a knowledgeable expert on Vedic literature, especially the Rig Veda."},
#             {"role": "user", "content": prompt},
#         ])
        
#         return JSONResponse(content={"hymn": hymn_data.dict(), "explanation": explanation})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.get("/vedic-quiz")
# async def generate_vedic_quiz(num_questions: int = Query(5, ge=1, le=10), api_key: str = Depends(get_api_key)):
#     all_verses = [verse for mandala in RIG_VEDA_DATA['mandalas'] for hymn in mandala['hymns'] for verse in hymn['verses']]
#     selected_verses = random.sample(all_verses, num_questions)
    
#     quiz_questions = []
#     for verse in selected_verses:
#         prompt = f"Create a multiple-choice question based on this Rig Veda verse:\n\n{verse['translation']}\n\nProvide four options and indicate the correct answer."
        
#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are an expert in creating educational quizzes about Vedic literature."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
        
#         # Parse the response to create a VedicQuiz object
#         # (This would require some text processing logic)

#     return JSONResponse(content={"quiz_questions": [q.dict() for q in quiz_questions]})



# @app.get("/comparative-analysis")
# async def compare_hymns(mandala1: int, hymn1: int, mandala2: int, hymn2: int, api_key: str = Depends(get_api_key)):
#     hymn_data1 = await get_hymn(mandala1, hymn1, api_key)
#     hymn_data2 = await get_hymn(mandala2, hymn2, api_key)
    
#     hymn_text1 = "\n".join([verse.translation for verse in hymn_data1.verses])
#     hymn_text2 = "\n".join([verse.translation for verse in hymn_data2.verses])
    
#     prompt = f"Compare and contrast the following two Rig Veda hymns:\n\nHymn 1:\n{hymn_text1}\n\nHymn 2:\n{hymn_text2}\n\nAnalyze their themes, style, and significance."
    
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an expert in comparative analysis of Vedic literature."},
#             {"role": "user", "content": prompt}
#         ]
#     )
    
#     analysis = response.choices[0].message.content
    
#     return JSONResponse(content={"hymn1": hymn_data1.dict(), "hymn2": hymn_data2.dict(), "comparative_analysis": analysis})

# @app.get("/generate-meditation")
# async def generate_meditation(mandala: int, hymn: int, duration: int = Query(10, ge=5, le=30), api_key: str = Depends(get_api_key)):
#     hymn_data = await get_hymn(mandala, hymn, api_key)
#     hymn_text = "\n".join([verse.translation for verse in hymn_data.verses])
    
#     prompt = f"Create a guided meditation script based on the following Rig Veda hymn. The meditation should last approximately {duration} minutes:\n\n{hymn_text}"
    
#     meditation_script = await call_openai_api([
#         {"role": "system", "content": "You are an expert in creating guided meditations based on ancient wisdom."},
#         {"role": "user", "content": prompt}
#     ])
    
#     return JSONResponse(content={"hymn": hymn_data.dict(), "meditation_script": meditation_script})

# @app.get("/ask-question")
# async def ask_question(question: str, api_key: str = Depends(get_api_key)):
#     prompt = f"Answer the following question about the Rig Veda:\n\n{question}"
    
#     answer = await call_openai_api([
#         {"role": "system", "content": "You are an expert on the Rig Veda and Vedic literature."},
#         {"role": "user", "content": prompt}
#     ])
    
#     return JSONResponse(content={"question": question, "answer": answer})

# @app.get("/sentiment/{mandala}/{hymn}")
# async def get_hymn_sentiment(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = await get_hymn(mandala, hymn, api_key)
#     text = " ".join([verse.translation for verse in hymn_data.verses])
#     sentiment = analyze_sentiment(text)
#     return {"hymn": hymn_data, "sentiment": sentiment}

# # Fix the word frequency visualization route
# @app.get("/visualize/word-frequency/{mandala}/{hymn}")
# async def visualize_word_frequency(mandala: int, hymn: int, api_key: str = Depends(get_api_key)):
#     hymn_data = await get_hymn(mandala, hymn, api_key)
#     chart_data = generate_word_frequency_chart(hymn_data)
#     return JSONResponse(content={"hymn": hymn_data.dict(), "word_frequency_chart": chart_data})

# @app.get("/audio/{mandala}/{hymn}")
# async def get_audio(mandala: int, hymn: int):
#     audio_path = get_audio_file_path(mandala, hymn)
#     if audio_path:
#         return FileResponse(audio_path, media_type="audio/mpeg")
#     raise HTTPException(status_code=404, detail="Audio file not found")

# @app.get("/test-openai-connection")
# async def test_openai_connection():
#     try:
#         response = await call_openai_api([{"role": "user", "content": "Hello"}])
#         return {"status": "success", "message": response}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)