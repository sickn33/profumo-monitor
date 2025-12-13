"""
Script per ottimizzare lo scraping riducendo il numero di pagine/categorie
"""
import scraper

# Opzioni di ottimizzazione:

# Opzione 1: Ridurre pagine per categoria (da 15 a 5)
# Modifica in scraper.py: max_pages=5 invece di max_pages=15

# Opzione 2: Scrapare solo categorie principali
# Modifica scrape_all_profumes() per usare solo alcune categorie

# Opzione 3: Scrapare solo homepage + categorie più importanti
# Modifica per saltare categorie meno importanti

def get_optimized_categories():
    """Restituisce solo le categorie più importanti"""
    base_url = "https://www.casadelprofumo.it"
    
    # Solo categorie principali (più prodotti)
    important_categories = [
        f"{base_url}/eau-de-parfum-da-donna/",
        f"{base_url}/eau-de-parfum-da-uomo/",
        f"{base_url}/eau-de-toilette-da-donna/",
        f"{base_url}/eau-de-toilette-da-uomo/",
        f"{base_url}/niche-eau-de-parfum/",
    ]
    
    return important_categories
