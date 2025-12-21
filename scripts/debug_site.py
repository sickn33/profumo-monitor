"""
Script per analizzare la struttura del sito casadelprofumo.it
"""
import requests
from bs4 import BeautifulSoup
import re

def analyze_site():
    """Analizza la struttura del sito"""
    base_url = "https://www.casadelprofumo.it"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept-Language': 'it-IT,it;q=0.9',
    })
    
    print("=" * 60)
    print("Analisi struttura sito casadelprofumo.it")
    print("=" * 60)
    
    # Test homepage
    print("\n1. Test homepage...")
    try:
        response = session.get(base_url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            # Cerca link a profumi
            perfume_links = soup.find_all('a', href=re.compile(r'profum', re.I))
            print(f"   Trovati {len(perfume_links)} link contenenti 'profum'")
            if perfume_links:
                print("   Esempi di link:")
                for link in perfume_links[:5]:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)[:50]
                    print(f"     - {href[:60]}... -> {text}")
    except Exception as e:
        print(f"   Errore: {e}")
    
    # Test pagina profumi donna
    print("\n2. Test pagina profumi donna...")
    test_urls = [
        f"{base_url}/profumi/profumi-da-donna/",
        f"{base_url}/profumi/",
        f"{base_url}/",
    ]
    
    for url in test_urls:
        try:
            print(f"\n   Testando: {url}")
            response = session.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Cerca prodotti
                # Prova vari pattern
                product_links = []
                
                # Pattern 1: link con href contenente pattern comuni
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if any(keyword in href.lower() for keyword in [
                        'eau-de-parfum', 'eau-de-toilette', 'parfum', 
                        'edp', 'edt', '/p/', '/product/'
                    ]):
                        full_url = href if href.startswith('http') else f"{base_url}{href}"
                        if full_url not in product_links:
                            product_links.append(full_url)
                
                print(f"   Trovati {len(product_links)} possibili link prodotti")
                if product_links:
                    print("   Esempi:")
                    for link in product_links[:3]:
                        print(f"     - {link[:80]}")
                
                # Pattern 2: cerca elementi con classi prodotto
                product_divs = soup.find_all(['div', 'article'], class_=re.compile(
                    r'product|item|card', re.I
                ))
                print(f"   Trovati {len(product_divs)} elementi con classi 'product/item/card'")
                
        except Exception as e:
            print(f"   Errore: {e}")
    
    # Test una pagina prodotto specifica (se trovata)
    print("\n3. Test pagina prodotto specifica...")
    # Prova con un URL comune
    test_product_url = f"{base_url}/profumi/profumi-da-donna/clinique-aromatics-elixir-eau-de-parfum-donna-100-ml"
    try:
        response = session.get(test_product_url, timeout=10)
        print(f"   URL: {test_product_url[:60]}...")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Cerca prezzo
            price_texts = soup.find_all(string=re.compile(r'[\d.,]+\s*€', re.I))
            print(f"   Trovati {len(price_texts)} testi con prezzo")
            for text in price_texts[:3]:
                print(f"     - {text.strip()[:50]}")
            
            # Cerca nome prodotto
            h1 = soup.find('h1')
            if h1:
                print(f"   Nome prodotto: {h1.get_text(strip=True)[:60]}")
    except Exception as e:
        print(f"   Errore: {e}")

if __name__ == "__main__":
    analyze_site()
