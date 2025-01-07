from openai import OpenAI
from models.schemas import Hymn, ModernInterpretation, VedicQuiz
from typing import List
import random
import json
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key="pk-fkPTgNVpLNzgJYBZmdtoKgsREyrfybcwKxPItgmdQHGMtGyZ",
    # Change the API base URL to the local interference API
    base_url="https://api.pawan.krd/pai-001/v1",  
)

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

async def call_openai_api(messages):
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model="pai-001-light",
                messages=messages
            )
            logger.info(f"OpenAI API response: {response}")
            
            if hasattr(response, 'choices') and response.choices and hasattr(response.choices[0], 'message'):
                return response.choices[0].message.content
            else:
                logger.warning(f"Unexpected response structure: {response}")
                if attempt < MAX_RETRIES - 1:
                    logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                    await asyncio.sleep(RETRY_DELAY)
                    continue
                else:
                    raise Exception("Max retries reached. Unexpected API response format.")
        except Exception as e:
            logger.error(f"Error in OpenAI API call (attempt {attempt + 1}): {str(e)}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                raise Exception(f"Max retries reached. Error calling OpenAI API: {str(e)}")
            
async def get_modern_interpretation(hymn: Hymn) -> List[ModernInterpretation]:
    interpretations = []
    for verse in hymn.verses:
        try:
            prompt = f"Provide a modern interpretation or application of the following Rig Veda verse:\n\n{verse.translation}"
            interpretation = await call_openai_api([
                {"role": "user", "content": "You are an expert in connecting ancient wisdom to modern life."},
                {"role": "user", "content": prompt}
            ])
            interpretations.append(ModernInterpretation(original_verse=verse, modern_interpretation=interpretation))
        except Exception as e:
            logger.error(f"Error interpreting verse {verse.number}: {str(e)}")
            interpretations.append(ModernInterpretation(
                original_verse=verse, 
                modern_interpretation="Unable to generate interpretation due to an error."
            ))
    return interpretations

async def analyze_hymn_themes(hymn: Hymn) -> str:
    hymn_text = "\n".join([verse.translation for verse in hymn.verses])
    prompt = f"Analyze the following Rig Veda hymn and identify its main themes. For each theme, provide a brief description and list the most relevant verses:\n\n{hymn_text}"
    
    return await call_openai_api([
        {"role": "user", "content": "You are an expert in Vedic literature analysis."},
        {"role": "user", "content": prompt}
    ])

async def explain_hymn(hymn: Hymn) -> str:
    hymn_text = f"Rig Veda Hymn {hymn.mandala}.{hymn.hymn_number}\n\n"
    hymn_text += f"Title: {hymn.title}\n\n"
    for verse in hymn.verses:
        hymn_text += f"Verse {verse.number}:\n"
        hymn_text += f"Sanskrit: {verse.sanskrit}\n"
        hymn_text += f"Transliteration: {verse.transliteration}\n"
        hymn_text += f"Translation: {verse.translation}\n\n"
    
    prompt = f"Please explain the following hymn from the Rig Veda, including its context, meaning, and significance:\n\n{hymn_text}"
    
    return await call_openai_api([
        {"role": "user", "content": "You are a knowledgeable expert on Vedic literature, especially the Rig Veda."},
        {"role": "user", "content": prompt},
    ])

async def generate_vedic_quiz(num_questions: int) -> List[VedicQuiz]:
    with open(r'C:\Users\Adi\Projects\vedam\veda-backend\data\rig_veda_formatted_combined.json') as f:
        RIG_VEDA_DATA = json.load(f)
    all_verses = [verse for mandala in RIG_VEDA_DATA['mandalas'] for hymn in mandala['hymns'] for verse in hymn['verses']]
    selected_verses = random.sample(all_verses, num_questions)
    
    quiz_questions = []
    for verse in selected_verses:
        prompt = f"Create a multiple-choice question based on this Rig Veda verse:\n\n{verse['translation']}\n\nProvide four options and indicate the correct answer."
        
        response = await call_openai_api([
            {"role": "user", "content": "You are an expert in creating educational quizzes about Vedic literature."},
            {"role": "user", "content": prompt}
        ])
        
        # Parse the response to create a VedicQuiz object
        # This is a simplified version and might need more sophisticated parsing
        lines = response.split('\n')
        question = lines[0]
        options = lines[1:5]
        correct_answer = int(lines[5].split()[-1]) - 1  # Assuming the correct answer is given as "Correct answer: X"
        
        quiz_questions.append(VedicQuiz(
            question=question,
            options=options,
            correct_answer=correct_answer
        ))
    
    return quiz_questions

async def compare_hymns(hymn1: Hymn, hymn2: Hymn) -> str:
    hymn_text1 = "\n".join([verse.translation for verse in hymn1.verses])
    hymn_text2 = "\n".join([verse.translation for verse in hymn2.verses])
    
    prompt = f"Compare and contrast the following two Rig Veda hymns:\n\nHymn 1:\n{hymn_text1}\n\nHymn 2:\n{hymn_text2}\n\nAnalyze their themes, style, and significance."
    
    return await call_openai_api([
        {"role": "user", "content": "You are an expert in comparative analysis of Vedic literature."},
        {"role": "user", "content": prompt}
    ])

async def generate_meditation(hymn: Hymn) -> str:
    hymn_text = "\n".join([verse.translation for verse in hymn.verses])
    prompt = f"Create a guided meditation based on the following Rig Veda hymn:\n\n{hymn_text}\n\nInclude calming instructions, visualizations, and reflections to enhance inner peace and spiritual connection."
    
    return await call_openai_api([
        {"role": "user", "content": "You are an experienced meditation guide with a focus on ancient wisdom."},
        {"role": "user", "content": prompt}
    ])

async def ask_question(question: str) -> str:
    prompt = f"Answer the following question about the Rig Veda:\n\n{question}"
    
    return await call_openai_api([
        {"role": "user", "content": "You are an expert on the Rig Veda and Vedic literature."},
        {"role": "user", "content": prompt}
    ])
