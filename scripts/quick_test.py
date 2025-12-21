"""
Test rapido su una singola pagina prodotto
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scraper
import requests
from bs4 import BeautifulSoup

def quick_test():
    """Test rapido su homepage per trovare un prodotto reale"""
    base_url = "https://www.casadelprofumo.it"
    
    print("=" * 60)
    print("Test Rapido - Trovare un prodotto reale")
    print("=" * 60)
    
    # Prendi homepage
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    })
    
    try:
        response = session.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Trova un link prodotto reale
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'eau-de-parfum' in href.lower() or 'eau-de-toilette' in href.lower():
                if 'ml' in href.lower() or 'g' in href.lower():
                    if not href.startswith('http'):
                        href = base_url + href
                    
                    print(f"\n✅ Trovato prodotto di test: {href[:80]}...")
                    
                    # Testa lo scraper su questo prodotto
                    scraper_instance = scraper.CasaDelProfumoScraper()
                    product = scraper_instance.scrape_product_page(href)
                    
                    if product and product.get('price'):
                        print(f"\n✅ Scraping riuscito!")
                        print(f"   Nome: {product['name'][:60]}")
                        print(f"   Brand: {product.get('brand', 'N/A')}")
                        print(f"   Prezzo: €{product.get('price', 'N/A')}")
                        print(f"   URL: {product['url'][:80]}")
                        return True
                    else:
                        print(f"   ⚠️ Prodotto trovato ma prezzo non estratto")
                        if product:
                            print(f"   Nome: {product.get('name', 'N/A')}")
                        return False
                    
        print("\n❌ Nessun prodotto trovato nella homepage")
        return False
        
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        return False

if __name__ == "__main__":
    quick_test()
