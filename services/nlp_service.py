# from typing import List, Dict
# from models.schemas import Hymn, SimilarityResult
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import matplotlib.pyplot as plt
# import io
# import base64
# from transformers import pipeline
# import re
# from data.veda_data import RIG_VEDA_DATA

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