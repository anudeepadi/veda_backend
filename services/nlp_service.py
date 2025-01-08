import google.generativeai as genai
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import json
import asyncio

load_dotenv()

class NLPService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    async def analyze_verse(self, verse: Dict) -> Dict:
        """Analyze a verse using Gemini AI"""
        try:
            # Create prompt with JSON structure as a string, not an f-string
            json_structure = '''
            {
                "themes": ["theme1", "theme2"],
                "symbolism": ["symbol1 and meaning", "symbol2 and meaning"],
                "cultural_context": "detailed cultural explanation",
                "philosophical_insights": ["insight1", "insight2"],
                "modern_relevance": "explanation of relevance today",
                "key_concepts": ["concept1", "concept2"]
            }
            '''
            
            prompt = (
                f"Analyze this Vedic verse:\n"
                f"Sanskrit: {verse.get('sanskrit', '')}\n"
                f"Translation: {verse.get('translation', '')}\n\n"
                f"Provide an analysis in JSON format matching this structure:\n"
                f"{json_structure}\n"
                f"Keep the analysis focused on the actual content of the verse."
            )
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            response_text = response.text.strip()
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            try:
                analysis = json.loads(response_text)
                return {
                    "themes": analysis.get("themes", []),
                    "symbolism": analysis.get("symbolism", []),
                    "cultural_context": analysis.get("cultural_context", ""),
                    "philosophical_insights": analysis.get("philosophical_insights", []),
                    "modern_relevance": analysis.get("modern_relevance", ""),
                    "key_concepts": analysis.get("key_concepts", [])
                }
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                return {
                    "themes": ["Understanding nature and divinity"],
                    "symbolism": ["Natural elements and their divine significance"],
                    "cultural_context": "Vedic hymn exploring the relationship between natural and divine forces",
                    "philosophical_insights": ["Unity of natural and divine realms"],
                    "modern_relevance": "Understanding our connection with nature and the divine",
                    "key_concepts": ["Divine manifestation in nature"]
                }
                
        except Exception as e:
            print(f"Error in analyze_verse: {str(e)}")
            return {
                "themes": ["Vedic wisdom"],
                "symbolism": ["Divine elements"],
                "cultural_context": "Ancient Vedic text",
                "philosophical_insights": ["Spiritual understanding"],
                "modern_relevance": "Timeless wisdom",
                "key_concepts": ["Spirituality"]
            }

    async def get_recommendations(self, current_verse: Dict, verses: List[Dict]) -> List[Dict]:
        """Get verse recommendations based on current verse"""
        try:
            verse_descriptions = []
            for i, v in enumerate(verses[:5]):
                desc = (
                    f"Verse {i+1}:\n"
                    f"Sanskrit: {v.get('sanskrit', '')}\n"
                    f"Translation: {v.get('translation', '')}"
                )
                verse_descriptions.append(desc)
            
            current_desc = (
                f"Current verse:\n"
                f"Sanskrit: {current_verse.get('sanskrit', '')}\n"
                f"Translation: {current_verse.get('translation', '')}"
            )
            
            prompt = (
                f"Find verses similar to this verse:\n\n"
                f"{current_desc}\n\n"
                f"From these verses:\n\n"
                f"{chr(10).join(verse_descriptions)}\n\n"
                f"Analyze their connections and provide output in this JSON format:\n"
                f'[{{"verse_index": 0, "similarity": 85, "reason": "explanation"}}]\n'
                f"Include only verses with similarity > 50."
            )
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            try:
                matches = json.loads(response.text)
                return [
                    {
                        "verse": verses[match["verse_index"]],
                        "similarity": match.get("similarity", 0),
                        "reason": match.get("reason", "Related verse")
                    }
                    for match in matches
                    if match.get("verse_index", -1) < len(verses)
                ]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing recommendations: {str(e)}")
                return []
                
        except Exception as e:
            print(f"Error in get_recommendations: {str(e)}")
            return []

    async def semantic_search(self, query: str, verses: List[Dict]) -> List[Dict]:
        """Search verses semantically based on query"""
        try:
            verse_descriptions = []
            for i, v in enumerate(verses[:5]):
                desc = (
                    f"Verse {i+1}:\n"
                    f"Sanskrit: {v.get('sanskrit', '')}\n"
                    f"Translation: {v.get('translation', '')}"
                )
                verse_descriptions.append(desc)
            
            prompt = (
                f"Find verses that match this query:\n"
                f"{query}\n\n"
                f"From these verses:\n"
                f"{chr(10).join(verse_descriptions)}\n\n"
                f"Provide matches in JSON format:\n"
                f'[{{"verse_index": 0, "relevance": 85, "explanation": "reason for match"}}]\n'
                f"Include only verses with relevance > 50."
            )
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            try:
                matches = json.loads(response.text)
                return [
                    {
                        "verse": verses[match["verse_index"]],
                        "relevance": match.get("relevance", 0),
                        "explanation": match.get("explanation", "Matching verse")
                    }
                    for match in matches
                    if match.get("verse_index", -1) < len(verses)
                ]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing search results: {str(e)}")
                return []
                
        except Exception as e:
            print(f"Error in semantic_search: {str(e)}")
            return []

    async def thematic_analysis(self, verses: List[Dict]) -> Dict:
        """Analyze themes across multiple verses"""
        try:
            verse_descriptions = []
            for i, v in enumerate(verses[:5]):
                desc = (
                    f"Verse {i+1}:\n"
                    f"Sanskrit: {v.get('sanskrit', '')}\n"
                    f"Translation: {v.get('translation', '')}"
                )
                verse_descriptions.append(desc)
            
            json_structure = '''
            {
                "major_themes": ["theme1", "theme2"],
                "interconnections": ["connection1", "connection2"],
                "progression": ["point1", "point2"],
                "overall_message": "summary message",
                "cultural_significance": "significance explanation"
            }
            '''
            
            prompt = (
                f"Analyze these Vedic verses for common themes:\n\n"
                f"{chr(10).join(verse_descriptions)}\n\n"
                f"Provide analysis in this JSON format:\n"
                f"{json_structure}"
            )
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            try:
                return json.loads(response.text)
            except json.JSONDecodeError as e:
                print(f"Error parsing thematic analysis: {str(e)}")
                return {
                    "major_themes": ["Spiritual wisdom"],
                    "interconnections": ["Divine unity"],
                    "progression": ["Spiritual growth"],
                    "overall_message": "Connection with divine",
                    "cultural_significance": "Vedic spiritual tradition"
                }
                
        except Exception as e:
            print(f"Error in thematic_analysis: {str(e)}")
            return {
                "major_themes": ["Vedic teachings"],
                "interconnections": ["Spiritual connections"],
                "progression": ["Divine understanding"],
                "overall_message": "Spiritual wisdom",
                "cultural_significance": "Vedic tradition"
            }