import json
import re

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def split_verses(text):
    return [verse.strip() for verse in re.split(r'\|\|', text) if verse.strip()]

def format_rig_veda_data(sanskrit_data, wikisource_data):
    formatted_data = {
        "name": "Rig Veda (Complete)",
        "mandalas": []
    }

    for sk_mandala, ws_mandala in zip(sanskrit_data['mandalas'], wikisource_data['mandalas']):
        formatted_mandala = {
            "number": sk_mandala['number'],
            "hymns": []
        }

        for sk_hymn, ws_hymn in zip(sk_mandala['hymns'], ws_mandala['hymns']):
            formatted_hymn = {
                "number": sk_hymn['number'],
                "title": sk_hymn['title'],
                "verses": []
            }

            sanskrit_verses = split_verses(sk_hymn['sanskrit'][0])
            english_transliteration = split_verses(sk_hymn['english'][0])
            english_translation = ws_hymn['verses']

            for i, (sanskrit, transliteration, translation) in enumerate(zip(sanskrit_verses, english_transliteration, english_translation), 1):
                formatted_verse = {
                    "number": i,
                    "sanskrit": sanskrit,
                    "transliteration": transliteration,
                    "translation": translation.split('. ', 1)[1] if '. ' in translation else translation
                }
                formatted_hymn['verses'].append(formatted_verse)

            formatted_mandala['hymns'].append(formatted_hymn)

        formatted_data['mandalas'].append(formatted_mandala)

    return formatted_data

def main():
    print("Loading Sanskrit data...")
    sanskrit_data = load_json_file('rig_veda_data.json')
    
    print("Loading Wikisource data...")
    wikisource_data = load_json_file('rig_veda_complete.json')
    
    print("Formatting and combining data...")
    formatted_data = format_rig_veda_data(sanskrit_data, wikisource_data)
    
    print("Saving formatted data...")
    with open('rig_veda_formatted_combined.json', 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)
    
    print("Formatting complete. Data saved to rig_veda_formatted_combined.json")
    
    # Print a summary of the formatted data
    print("\nSummary of formatted data:")
    total_hymns = 0
    total_verses = 0
    for mandala in formatted_data['mandalas']:
        hymn_count = len(mandala['hymns'])
        verse_count = sum(len(hymn['verses']) for hymn in mandala['hymns'])
        total_hymns += hymn_count
        total_verses += verse_count
        print(f"Mandala {mandala['number']}: {hymn_count} hymns, {verse_count} verses")
    print(f"Total: {total_hymns} hymns, {total_verses} verses")

if __name__ == "__main__":
    main()