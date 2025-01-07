import json
import re
from pydub import AudioSegment
import numpy as np

def prepare_mantra_healing_dataset():
    with open(r'C:\Users\anude\Projects\vedam\veda-backend\data\rig_veda_formatted_combined.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    mantra_data = []

    for mandala in data['mandalas']:
        for hymn in mandala['hymns']:
            for verse in hymn['verses']:
                # Simplified mantra extraction (actual implementation would be more complex)
                mantras = re.findall(r'\b[A-Z]+\b', verse['transliteration'])
                if mantras:
                    audio_file = f"audio_data/{mandala['number']}/{hymn['number']}.mp3"
                    try:
                        audio = AudioSegment.from_mp3(audio_file)
                        # Extract audio features (simplified)
                        audio_array = np.array(audio.get_array_of_samples())
                        frequency = np.abs(np.fft.fft(audio_array)[:len(audio_array)//2])
                        dominant_freq = np.argmax(frequency)
                        
                        mantra_data.append({
                            'mantra': mantras[0],
                            'sanskrit': verse['sanskrit'],
                            'translation': verse['translation'],
                            'dominant_frequency': float(dominant_freq),
                            'audio_length': len(audio),
                            'mandala': mandala['number'],
                            'hymn': hymn['number'],
                            'verse': verse['number']
                        })
                    except FileNotFoundError:
                        print(f"Audio file not found: {audio_file}")

    with open('mantra_healing_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(mantra_data, f, ensure_ascii=False, indent=2)

    print("Mantra sound healing dataset prepared. Check 'mantra_healing_dataset.json' for results.")

if __name__ == "__main__":
    prepare_mantra_healing_dataset()