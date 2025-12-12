"""
Script di test per verificare lo scraper
"""
import logging
import scraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_single_product():
    """Test su una singola pagina prodotto"""
    print("=" * 60)
    print("Test scraping singolo prodotto")
    print("=" * 60)
    
    scraper_instance = scraper.CasaDelProfumoScraper()
    
    # Prova con una URL valida
    test_url = "https://www.casadelprofumo.it/eau-de-parfum-da-donna/"
    
    print(f"\nTestando URL: {test_url}")
    print("Scraping prima pagina della categoria...")
    
    products = scraper_instance.scrape_category(test_url, max_pages=1)
    
    print(f"\n✅ Trovati {len(products)} prodotti")
    
    if products:
        print("\nPrimi 3 prodotti trovati:")
        for i, product in enumerate(products[:3], 1):
            print(f"\n{i}. {product['name']}")
            print(f"   Brand: {product.get('brand', 'N/A')}")
            print(f"   Prezzo: €{product.get('price', 'N/A')}")
            print(f"   URL: {product['url']}")
    else:
        print("\n⚠️ Nessun prodotto trovato. Potrebbe essere necessario aggiornare i selettori CSS.")

if __name__ == "__main__":
    test_single_product()
