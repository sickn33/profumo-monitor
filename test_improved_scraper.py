"""
Test dello scraper migliorato
"""
import logging
import scraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_discovery():
    """Test della scoperta automatica"""
    print("=" * 80)
    print("TEST SCRAPER MIGLIORATO - Scoperta Automatica")
    print("=" * 80)
    
    scraper_instance = scraper.CasaDelProfumoScraper()
    
    # Test 1: Scoperta categorie
    print("\n1. TEST SCOPERTA CATEGORIE")
    print("-" * 80)
    categories = scraper_instance.discover_categories()
    print(f"✅ Trovate {len(categories)} categorie")
    print("\nPrime 10 categorie:")
    for i, cat in enumerate(categories[:10], 1):
        print(f"   {i}. {cat}")
    
    # Test 2: Scraping homepage
    print("\n2. TEST SCRAPING HOMEPAGE")
    print("-" * 80)
    homepage_products = scraper_instance.scrape_homepage_products()
    print(f"✅ Trovati {len(homepage_products)} prodotti nella homepage")
    if homepage_products:
        print("\nPrimi 3 prodotti:")
        for i, product in enumerate(homepage_products[:3], 1):
            print(f"   {i}. {product['name'][:50]}")
            print(f"      Prezzo: €{product.get('price', 'N/A')}")
    
    # Test 3: Scraping una categoria
    print("\n3. TEST SCRAPING CATEGORIA")
    print("-" * 80)
    if categories:
        test_category = categories[0]
        print(f"Testando categoria: {test_category}")
        category_products = scraper_instance.scrape_category(test_category, max_pages=2)
        print(f"✅ Trovati {len(category_products)} prodotti")
        if category_products:
            print("\nPrimi 3 prodotti:")
            for i, product in enumerate(category_products[:3], 1):
                print(f"   {i}. {product['name'][:50]}")
                print(f"      Prezzo: €{product.get('price', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETATO")
    print("=" * 80)

if __name__ == "__main__":
    test_discovery()
