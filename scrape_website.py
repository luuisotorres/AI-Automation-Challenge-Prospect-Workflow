import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def scrape_website_data(url):
    """
    This functions receives an URL as input and uses BeautifulSoup to scrape the website to extract
    titles, headers, and paragraphs.

    Args:
        url (str): The URL of the website to scrapte.
    
        Returs:
        A JSON file containing the scraped data
    """

    try:
        # Fecthing HTML content from the page
        response = requests.get(
            url, timeout=10, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        # Raise an error if there is any HTTP issues
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting elements

        data = {
            'url': url,
            'title': soup.title.string if soup.title else 'No title available',
            'headers': [header.get_text(strip=True) for header in soup.find_all('h1','h2', 'h3')],
            'paragraphs': [p.get_text(strip=True) for p in soup.find_all('p')],
            'links': [] 
        }

        # Collecting links
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if full_url.startswith(url):
                data['links'].append(full_url)

        # Saving data as a JSON file
        with open("scraped_data.json", 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        print(f"Scraped data saved to 'scraped_data.json'")
        return data

    # Handling errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}
    
if __name__ == "__main__":
    website_url = input("Enter the URL for the website:")
    scraped_data = scrape_website_data(website_url)
    print(json.dumps(scraped_data,
                     indent=4,
                     ensure_ascii=False))
