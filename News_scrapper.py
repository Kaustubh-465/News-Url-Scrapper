import requests
from bs4 import BeautifulSoup
import sys

def scrape_cnn(url, soup):
    title = soup.find('h1').get_text() if soup.find('h1') else "No title found"
    content = "\n".join([p.get_text() for p in soup.find_all('p')])
    return title, content

def scrape_nyt(url, soup):
    title = soup.find('h1').get_text() if soup.find('h1') else "No title found"
    # NYT often has article text in <section name="articleBody">
    article_body = soup.find_all('p')
    content = "\n".join([p.get_text() for p in article_body])
    return title, content

def scrape_wapo(url, soup):
    title = soup.find('h1').get_text() if soup.find('h1') else "No title found"
    paragraphs = soup.find_all('p')
    content = "\n".join([p.get_text() for p in paragraphs])
    return title, content

def scrape_reuters(url, soup):
    title = soup.find('h1').get_text() if soup.find('h1') else "No title found"
    paragraphs = soup.find_all('p')
    content = "\n".join([p.get_text() for p in paragraphs])
    return title, content

def scrape_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None, f"Error {response.status_code} fetching the page"

    soup = BeautifulSoup(response.text, 'lxml')

    # Decide which scraper to use
    if "cnn.com" in url:
        return scrape_cnn(url, soup)
    elif "nytimes.com" in url:
        return scrape_nyt(url, soup)
    elif "washingtonpost.com" in url:
        return scrape_wapo(url, soup)
    elif "reuters.com" in url:
        return scrape_reuters(url, soup)
    else:
        return None, "Website not supported yet."

# If running from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_news.py <article_url>")
        sys.exit(1)

    url = sys.argv[1]
    title, content = scrape_article(url)

    print("\n=== ARTICLE TITLE ===")
    print(title)
    print("\n=== ARTICLE CONTENT (first 500 chars) ===")
    print(content[:500], "...")
