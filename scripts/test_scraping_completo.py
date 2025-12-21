"""
Test completo dello scraper per verificare che funzioni
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import scraper
import database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_scraping():
    """Test completo dello scraping"""
    print("=" * 80)
    print("TEST COMPLETO SCRAPER - Verifica Funzionamento")
    print("=" * 80)
    print()
    
    scraper_instance = scraper.CasaDelProfumoScraper()
    
    # Test 1: Scraping homepage
    print("TEST 1: Scraping Homepage")
    print("-" * 80)
    try:
        homepage_products = scraper_instance.scrape_homepage_products()
        print(f"✅ Trovati {len(homepage_products)} prodotti nella homepage")
        if homepage_products:
            print("\nPrimi 3 prodotti homepage:")
            for i, product in enumerate(homepage_products[:3], 1):
                print(f"  {i}. {product['name'][:60]}")
                print(f"     Prezzo: €{product.get('price', 'N/A')}")
                print(f"     URL: {product['url'][:70]}...")
        else:
            print("⚠️ Nessun prodotto trovato nella homepage")
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Test 2: Scoperta categorie
    print("TEST 2: Scoperta Categorie")
    print("-" * 80)
    try:
        categories = scraper_instance.discover_categories()
        print(f"✅ Trovate {len(categories)} categorie")
        print("\nPrime 5 categorie:")
        for i, cat in enumerate(categories[:5], 1):
            print(f"  {i}. {cat}")
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Test 3: Scraping una categoria
    print("TEST 3: Scraping Categoria (prima pagina)")
    print("-" * 80)
    if categories:
        try:
            test_category = categories[0]
            print(f"Testando: {test_category}")
            category_products = scraper_instance.scrape_category(test_category, max_pages=1)
            print(f"✅ Trovati {len(category_products)} prodotti")
            if category_products:
                print("\nPrimi 3 prodotti categoria:")
                for i, product in enumerate(category_products[:3], 1):
                    print(f"  {i}. {product['name'][:60]}")
                    print(f"     Prezzo: €{product.get('price', 'N/A')}")
        except Exception as e:
            print(f"❌ Errore: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    
    # Test 4: Test completo (limitato)
    print("TEST 4: Test Scraping Completo (limitato)")
    print("-" * 80)
    print("⚠️ Questo test è limitato per non sovraccaricare il sito")
    print("   Scrapa solo homepage + 1 categoria")
    try:
        # Scrapa homepage
        all_products = scraper_instance.scrape_homepage_products()
        
        # Scrapa una categoria
        if categories:
            cat_products = scraper_instance.scrape_category(categories[0], max_pages=1)
            all_products.extend(cat_products)
        
        print(f"✅ Totale prodotti trovati: {len(all_products)}")
        
        if all_products:
            print("\nStatistiche:")
            products_with_price = [p for p in all_products if p.get('price')]
            print(f"  - Prodotti con prezzo: {len(products_with_price)}")
            print(f"  - Prodotti senza prezzo: {len(all_products) - len(products_with_price)}")
            
            if products_with_price:
                prices = [p['price'] for p in products_with_price]
                print(f"  - Prezzo minimo: €{min(prices):.2f}")
                print(f"  - Prezzo massimo: €{max(prices):.2f}")
                print(f"  - Prezzo medio: €{sum(prices)/len(prices):.2f}")
        else:
            print("❌ Nessun prodotto trovato!")
            print("   Potrebbe essere necessario aggiornare lo scraper")
    
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    print("TEST COMPLETATO")
    print("=" * 80)

if __name__ == "__main__":
    test_scraping()
