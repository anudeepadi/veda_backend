import requests
from bs4 import BeautifulSoup
import json
import re
import logging
import unicodedata
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://www.gatewayforindia.com/vedas/rigveda"

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def is_devanagari(char):
    return unicodedata.name(char).startswith('DEVANAGARI')

def separate_text(content):
    sanskrit_verses = []
    english_verses = []
    current_sanskrit = ""
    current_english = ""

    for line in content:
        if any(is_devanagari(char) for char in line):
            if current_sanskrit:
                current_sanskrit += " "
            current_sanskrit += line
        elif line.startswith('aghni') or re.match(r'^[a-z]', line):
            if current_english:
                current_english += " "
            current_english += line
        elif current_sanskrit and current_english:
            sanskrit_verses.append(current_sanskrit)
            english_verses.append(current_english)
            current_sanskrit = ""
            current_english = ""

    if current_sanskrit and current_english:
        sanskrit_verses.append(current_sanskrit)
        english_verses.append(current_english)

    return sanskrit_verses, english_verses

def scrape_hymn(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        center_tag = soup.find('center')
        if not center_tag:
            logging.warning(f"No 'center' tag found in {url}")
            return None

        hymn_title = center_tag.find('h3')
        if not hymn_title:
            logging.warning(f"No 'h3' tag found in {url}")
            return None

        hymn_title_text = hymn_title.text.strip()
        hymn_number_match = re.search(r'Hymn (\d+)', hymn_title_text)
        if not hymn_number_match:
            logging.warning(f"Could not extract hymn number from title: {hymn_title_text}")
            return None

        hymn_number = hymn_number_match.group(1)

        content = []
        for element in center_tag.find_all_next(string=True):
            text = clean_text(element)
            if text and 'Next: Hymn' not in text:
                content.append(text)

        sanskrit_verses, english_verses = separate_text(content)

        return {
            'number': int(hymn_number),
            'title': hymn_title_text,
            'sanskrit': sanskrit_verses,
            'english': english_verses
        }

    except Exception as e:
        logging.error(f"Error scraping hymn {url}: {str(e)}")
        return None

def scrape_mandala(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        hymns = []
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('rigveda') and link['href'].endswith('.shtml'):
                hymn_url = f"{BASE_URL}/{link['href']}"
                logging.info(f"Scraping hymn: {hymn_url}")
                hymn_data = scrape_hymn(hymn_url)
                if hymn_data:
                    hymns.append(hymn_data)
                time.sleep(1)  # Be respectful to the server

        return hymns

    except Exception as e:
        logging.error(f"Error scraping mandala {url}: {str(e)}")
        return None

def scrape_rig_veda():
    rig_veda_data = {
        'name': 'Rig Veda',
        'mandalas': []
    }

    index_url = f"{BASE_URL}/index.shtml"
    try:
        response = requests.get(index_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a', href=True):
            if link['href'].startswith('rigveda') and link['href'].endswith('.shtml'):
                mandala_url = f"{BASE_URL}/{link['href']}"
                logging.info(f"Scraping mandala: {mandala_url}")
                hymns = scrape_mandala(mandala_url)
                if hymns:
                    mandala_number = int(re.search(r'rigveda(\d+)', link['href']).group(1))
                    rig_veda_data['mandalas'].append({
                        'number': mandala_number,
                        'hymns': hymns
                    })
                time.sleep(2)  # Be respectful to the server

        return rig_veda_data

    except Exception as e:
        logging.error(f"Error scraping Rig Veda: {str(e)}")
        return None

if __name__ == "__main__":
    rig_veda_data = scrape_rig_veda()
    if rig_veda_data:
        with open('rig_veda_data.json', 'w', encoding='utf-8') as f:
            json.dump(rig_veda_data, f, ensure_ascii=False, indent=2)
        logging.info("Rig Veda data successfully scraped and saved to rig_veda_data.json")
    else:
        logging.error("Failed to scrape Rig Veda data")