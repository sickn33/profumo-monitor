"""
Script per analizzare quante pagine ha realmente ogni categoria
"""
import requests
from bs4 import BeautifulSoup
import time

def analizza_categoria(url):
    """Analizza una categoria per vedere quante pagine ha"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    })
    
    try:
        response = session.get(url, timeout=10)
        if response.status_code != 200:
            return 0, 0
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Conta link prodotti nella prima pagina
        product_count = 0
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            if any(x in href for x in ['ml', 'g']) and any(x in href for x in ['eau-de-parfum', 'eau-de-toilette', 'parfum']):
                if not href.endswith('/') or href.count('/') <= 3:
                    product_count += 1
        
        # Cerca paginazione
        next_page = soup.find('a', class_=lambda x: x and ('next' in x.lower() or 'pager-next' in x.lower()))
        has_next = next_page is not None
        
        return product_count, 1 if has_next else 0
    
    except Exception as e:
        print(f"Errore: {e}")
        return 0, 0

def analizza_tutte_categorie():
    """Analizza tutte le categorie"""
    base_url = "https://www.casadelprofumo.it"
    
    categories = [
        f"{base_url}/eau-de-parfum-da-donna/",
        f"{base_url}/eau-de-toilette-da-donna/",
        f"{base_url}/colonia-femminile/",
        f"{base_url}/eau-de-parfum-da-uomo/",
        f"{base_url}/eau-de-toilette-da-uomo/",
        f"{base_url}/colonia-maschile/",
        f"{base_url}/unisex-eau-de-parfum/",
        f"{base_url}/unisex-eau-de-toilette/",
        f"{base_url}/unisex-colonia/",
        f"{base_url}/niche-eau-de-parfum/",
        f"{base_url}/niche-eau-de-toilette/",
    ]
    
    print("=" * 80)
    print("ANALISI COPERTURA REALE")
    print("=" * 80)
    print()
    
    total_products = 0
    categories_with_products = 0
    
    for cat in categories:
        print(f"Analizzando: {cat}")
        products, has_pages = analizza_categoria(cat)
        total_products += products
        if products > 0:
            categories_with_products += 1
        print(f"  Prodotti prima pagina: {products}")
        print(f"  Ha paginazione: {'Sì' if has_pages else 'No'}")
        print()
        time.sleep(1)  # Delay per non sovraccaricare
    
    print("=" * 80)
    print(f"TOTALE PRODOTTI PRIMA PAGINA: {total_products}")
    print(f"Categorie con prodotti: {categories_with_products}/{len(categories)}")
    print("=" * 80)

if __name__ == "__main__":
    analizza_tutte_categorie()
