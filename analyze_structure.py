"""
Script per analizzare in dettaglio la struttura del sito
"""
import requests
from bs4 import BeautifulSoup
import re

def deep_analyze():
    """Analisi approfondita della struttura"""
    base_url = "https://www.casadelprofumo.it"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept-Language': 'it-IT,it;q=0.9',
    })
    
    print("=" * 80)
    print("ANALISI APPROFONDITA STRUTTURA SITO")
    print("=" * 80)
    
    # Analizza homepage
    print("\n1. HOMEPAGE - Analisi link prodotti")
    try:
        response = session.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Cerca tutti i link
        all_links = soup.find_all('a', href=True)
        product_links = []
        category_links = []
        
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Link prodotto
            if any(x in href.lower() for x in ['ml', 'g']) and any(x in href.lower() for x in ['eau-de-parfum', 'eau-de-toilette', 'parfum']):
                if href not in [p['href'] for p in product_links]:
                    product_links.append({'href': href, 'text': text[:50]})
            
            # Link categoria
            if any(x in href.lower() for x in ['eau-de-parfum', 'eau-de-toilette', 'colonia']) and href.endswith('/'):
                if href not in [c['href'] for c in category_links]:
                    category_links.append({'href': href, 'text': text[:50]})
        
        print(f"   Trovati {len(product_links)} link prodotti diretti")
        print(f"   Trovati {len(category_links)} link categorie")
        
        if product_links:
            print("\n   Esempi prodotti:")
            for p in product_links[:3]:
                print(f"     - {p['href'][:70]}")
        
        if category_links:
            print("\n   Categorie trovate:")
            for c in category_links[:10]:
                print(f"     - {c['href']}")
    
    except Exception as e:
        print(f"   Errore: {e}")
    
    # Analizza pagina profumi
    print("\n2. PAGINA /profumi/ - Analisi struttura")
    try:
        response = session.get(f"{base_url}/profumi/", timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Cerca elementi prodotto
        print("   Cercando elementi con classi prodotto...")
        product_elements = soup.find_all(['div', 'article', 'li'], class_=re.compile(
            r'product|item|card|box|grid', re.I
        ))
        print(f"   Trovati {len(product_elements)} elementi con classi prodotto")
        
        # Analizza struttura HTML di un elemento prodotto
        if product_elements:
            sample = product_elements[0]
            print("\n   Struttura elemento prodotto (primo):")
            print(f"     Tag: {sample.name}")
            print(f"     Classi: {sample.get('class', [])}")
            
            # Cerca link dentro
            link = sample.find('a', href=True)
            if link:
                print(f"     Link: {link.get('href', '')[:70]}")
            
            # Cerca prezzo dentro
            price_elem = sample.find(string=re.compile(r'[\d.,]+\s*€', re.I))
            if price_elem:
                print(f"     Prezzo trovato: {price_elem.strip()[:30]}")
        
        # Cerca pattern di paginazione
        pagination = soup.find_all(['a', 'span'], class_=re.compile(r'page|pagination|next|prev', re.I))
        print(f"\n   Elementi paginazione: {len(pagination)}")
        for p in pagination[:5]:
            print(f"     - {p.name} class={p.get('class', [])} text={p.get_text(strip=True)[:30]}")
    
    except Exception as e:
        print(f"   Errore: {e}")
    
    # Analizza una categoria
    print("\n3. CATEGORIA /eau-de-parfum-da-donna/ - Analisi")
    try:
        response = session.get(f"{base_url}/eau-de-parfum-da-donna/", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Conta link prodotti
            product_count = 0
            for link in soup.find_all('a', href=True):
                href = link['href']
                if any(x in href.lower() for x in ['ml', 'g']) and not href.endswith('/'):
                    if 'eau-de-parfum' in href.lower() or 'eau-de-toilette' in href.lower():
                        product_count += 1
            
            print(f"   Link prodotti trovati: {product_count}")
            
            # Cerca paginazione
            next_page = soup.find('a', class_=re.compile(r'next|page', re.I))
            if next_page:
                print(f"   Link pagina successiva: {next_page.get('href', '')}")
    
    except Exception as e:
        print(f"   Errore: {e}")

if __name__ == "__main__":
    deep_analyze()
