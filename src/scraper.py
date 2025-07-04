# src/scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import os

def run_scraper():
    """
    Navigates all pages of books.toscrape.com, extracts information
    from each book, and saves it to a CSV file securely.
    """
    print("Starting the web scraping process...")

    url_base = 'http://books.toscrape.com/catalogue/'
    current_url = urljoin(url_base, 'page-1.html')
    book_data = []
    page_num = 1

    while current_url:
        print(f"Scraping page {page_num}: {current_url}")
        try:
            response = requests.get(current_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error accessing the page: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        books_on_page = soup.find_all('article', class_='product_pod')

        for book in books_on_page:
            title = "Not available"
            price = 0.0
            rating_num = 0

            h3_tag = book.find('h3')
            if h3_tag and (a_tag := h3_tag.find('a')) and a_tag.get('title'):
                title = a_tag['title']

            p_price_tag = book.find('p', class_='price_color')
            if p_price_tag and p_price_tag.text:
                try:
                    price = float(p_price_tag.text.replace('£', ''))
                except (ValueError, TypeError):
                    price = 0.0

            p_rating_tag = book.find('p', class_='star-rating')
            if p_rating_tag and p_rating_tag.get('class'):
                rating_text = p_rating_tag['class'][1]
                ratings_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
                rating_num = ratings_map.get(rating_text, 0)
            
            book_data.append({'titulo': title, 'precio': price, 'calificacion': rating_num})

        next_button = soup.find('li', class_='next')
        if next_button and (a_next := next_button.find('a')) and a_next.get('href'):
            next_link = str(a_next['href'])
            current_url = urljoin(url_base, next_link)
            page_num += 1
        else:
            current_url = None

    print("\nScraping completed.")
    
    if not book_data:
        print("No data was extracted. Exiting.")
        return

    df = pd.DataFrame(book_data)
    if not os.path.exists('data'):
        os.makedirs('data')
        
    save_path = os.path.join('data', 'biblioteca_completa.csv')
    df.to_csv(save_path, index=False)
    print(f"{len(df)} books were saved to '{save_path}'.")

if __name__ == '__main__':
    run_scraper()