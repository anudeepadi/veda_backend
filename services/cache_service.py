from functools import lru_cache
from typing import Dict, List, Optional
import json
import os
from pathlib import Path

class VedaCache:
    def __init__(self):
        self._mandala_cache: Dict = {}
        self._verse_cache: Dict = {}
        self._load_data()

    def _load_data(self):
        data_path = Path(__file__).parent.parent / 'data' / 'rig_veda_formatted_combined.json'
        with open(data_path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)
            self._process_data()

    def _process_data(self):
        for mandala in self._data:
            mandala_id = mandala['id']
            self._mandala_cache[mandala_id] = mandala
            
            for hymn in mandala['hymns']:
                for verse in hymn['verses']:
                    key = f"{mandala_id}_{hymn['id']}_{verse['id']}"
                    self._verse_cache[key] = verse

    @lru_cache(maxsize=128)
    def get_mandala(self, mandala_id: int) -> Optional[Dict]:
        return self._mandala_cache.get(mandala_id)

    @lru_cache(maxsize=1024)
    def get_verse(self, mandala_id: int, hymn_id: int, verse_id: int) -> Optional[Dict]:
        key = f"{mandala_id}_{hymn_id}_{verse_id}"
        return self._verse_cache.get(key)

    def search_verses(self, query: str) -> List[Dict]:
        query = query.lower()
        results = []
        
        for verse_key, verse in self._verse_cache.items():
            if (query in verse['text'].lower() or 
                query in verse['translation'].lower()):
                mandala_id, hymn_id, verse_id = map(int, verse_key.split('_'))
                results.append({
                    'mandala_id': mandala_id,
                    'hymn_id': hymn_id,
                    'verse_id': verse_id,
                    'verse': verse
                })
        
        return results[:100]  # Limit results

veda_cache = VedaCache()