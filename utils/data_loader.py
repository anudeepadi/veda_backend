import json
from config import RIG_VEDA_DATA_PATH

def load_json_data(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

RIG_VEDA_DATA = load_json_data(RIG_VEDA_DATA_PATH)