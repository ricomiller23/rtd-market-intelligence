import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

class RTDEntry(BaseModel):
    title: str
    description: str
    category: Literal['Spirits-Based', 'Wine-Based', 'Energy Hybrid', 'Cider-Based', 'Market Trend']
    company: str

DASHBOARD_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'src', 'data', 'rtd_scan.json')

def scrape_article(url):
    """Fetches the URL and extracts text using BeautifulSoup."""
    try:
        # Standard headers to avoid blocks from basic sites
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else 'No Title'
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        return {
            "title": title.strip(),
            "content": text.strip()
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}", file=sys.stderr)
        return None

def process_with_llm(article):
    """
    Uses OpenAI to extract structured categorization from the scraped text.
    """
    try:
        client = OpenAI() # Requires OPENAI_API_KEY environment variable
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert beverage industry analyst extracting structured intelligence."},
                {"role": "user", "content": prompt}
            ],
            response_format=RTDEntry,
        )
        
        result = completion.choices[0].message.parsed
        return {
            "id": str(int(datetime.now().timestamp())),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": result.title,
            "description": result.description,
            "category": result.category,
            "company": result.company
        }
    except Exception as e:
        print(f"Error calling OpenAI API or missing key: {e}. Falling back to heuristic extraction...", file=sys.stderr)
        
        # Heuristic Fallback Extraction
        text = (article['title'] + " " + article['content']).lower()
        category = "Spirits-Based"
        if "wine" in text or "spritz" in text or "sangria" in text:
            category = "Wine-Based"
        elif "energy" in text or "caffeine" in text or "guarana" in text:
            category = "Energy Hybrid"
        elif "cider" in text or "apple" in text:
            category = "Cider-Based"
            
        return dict(
            id=str(int(datetime.now().timestamp())),
            date=datetime.now().strftime("%Y-%m-%d"),
            title=article['title'],
            description=f"{article['content'][:250]}...",
            category=category,
            company="Unknown"
        )

def append_to_dashboard(new_entry):
    """Appends to the Next.js JSON datastore."""
    try:
        with open(DASHBOARD_DATA_PATH, 'r') as f:
            data = json.load(f)
            
        data.insert(0, new_entry) # Put new entry at the top
        
        with open(DASHBOARD_DATA_PATH, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"\\n\\033[92mSuccess:\\033[0m Inserted '{new_entry['title']}' into dashboard!")
    except Exception as e:
        print(f"Error appending to DB: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <industry_news_url>")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"[*] Scraping {url}...")
    
    article = scrape_article(url)
    
    if not article:
        print("Failed to retrieve content.")
        sys.exit(1)
        
    structured_data = process_with_llm(article)
    print(f"[*] Evaluated Intelligence Payload:")
    print(json.dumps(structured_data, indent=2))
    
    append_to_dashboard(structured_data)

if __name__ == "__main__":
    main()
