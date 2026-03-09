import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
    Mock function representing the LLM structurizer.
    In production, this passes 'article' to OpenAI/Anthropic to extract exact categorizations.
    """
    return {
        "id": str(int(datetime.now().timestamp())),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": article['title'],
        "description": f"{article['content'][:250]}...",
        "category": "Market Trend", 
        "company": "Scraped Source"
    }

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
