import requests
from bs4 import BeautifulSoup
import json
import re
import time
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://en.wikisource.org"

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_hymn(hymn_url):
    try:
        response = requests.get(hymn_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('h1', id='firstHeading').text.strip()
        hymn_number = re.search(r'Hymn (\d+)', title).group(1)
        
        verses = soup.find_all('div', class_='verse')
        if not verses:
            return None
        
        verse_text = verses[0].find('pre').get_text(strip=True)
        individual_verses = re.split(r'\n(?=\d+\.)', verse_text)
        formatted_verses = [clean_text(verse) for verse in individual_verses if verse.strip()]
        
        return {
            'number': int(hymn_number),
            'title': title,
            'verses': formatted_verses
        }
    except Exception as e:
        logging.error(f"Error extracting hymn from {hymn_url}: {str(e)}")
        return None

def hymns_extract(mandala_link):
    try:
        response = requests.get(mandala_link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        hymns = []
        hymn_links = soup.select('div.mw-parser-output ul li a')
        
        for link in tqdm(hymn_links, desc="Extracting hymns", unit="hymn"):
            if 'Hymn' in link.text:
                hymn_url = BASE_URL + link['href']
                hymn_data = extract_hymn(hymn_url)
                if hymn_data:
                    hymns.append(hymn_data)
                time.sleep(1)  # Be respectful to the server
        
        return hymns
    except Exception as e:
        logging.error(f"Error extracting hymns from {mandala_link}: {str(e)}")
        return []

if __name__ == "__main__":
    rig_veda_data = {
        'name': 'Rig Veda (Complete)',
        'mandalas': []
    }
    
    for mandala_number in tqdm(range(1, 11), desc="Processing Mandalas", unit="mandala"):
        mandala_link = f"{BASE_URL}/wiki/The_Rig_Veda/Mandala_{mandala_number}"
        logging.info(f"Scraping Mandala {mandala_number}")
        
        mandala_data = {
            'number': mandala_number,
            'hymns': hymns_extract(mandala_link)
        }
        
        rig_veda_data['mandalas'].append(mandala_data)
        
        time.sleep(2)  # Add a delay between mandalas
    
    with open('rig_veda_complete.json', 'w', encoding='utf-8') as f:
        json.dump(rig_veda_data, f, ensure_ascii=False, indent=2)
    
    logging.info("Scraping completed. Data saved to rig_veda_complete.json")
    
    # Print a summary of the scraped data
    print("\nSummary of scraped data:")
    total_hymns = 0
    for mandala in rig_veda_data['mandalas']:
        hymn_count = len(mandala['hymns'])
        total_hymns += hymn_count
        print(f"Mandala {mandala['number']}: {hymn_count} hymns scraped")
    print(f"Total hymns scraped: {total_hymns}")