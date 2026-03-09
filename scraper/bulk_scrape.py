from duckduckgo_search import DDGS
from extractor import process_with_llm, append_to_dashboard
import time

def fetch_search_news():
    print("[*] Fetching live news from DuckDuckGo...")
    results = DDGS().news("RTD beverage cocktail launch", max_results=10)
    
    articles = []
    for r in results:
        articles.append({
            "title": r.get('title', ''),
            "content": r.get('body', ''),
            "url": r.get('url', '')
        })
    return articles[:5]

def main():
    articles = fetch_search_news()
    print(f"[*] Found {len(articles)} live snippets. Beginning pipeline...")
    for article in articles:
        print(f"\\n[*] Processing: {article['title']}")
        structured_data = process_with_llm(article)
        append_to_dashboard(structured_data)
        time.sleep(2)

if __name__ == "__main__":
    main()
