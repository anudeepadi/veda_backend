import json 

def load_data():
    with open(r'data\rig_veda_formatted_combined.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

RIG_VEDA_DATA = load_data()