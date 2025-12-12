"""
Scraper per casadelprofumo.it
"""
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CasaDelProfumoScraper:
    """Scraper per il sito casadelprofumo.it"""
    
    def __init__(self):
        self.base_url = config.TARGET_SITE
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8',
        })
    
    def extract_price(self, price_text):
        """Estrae il prezzo da una stringa"""
        if not price_text:
            return None
        
        # Rimuovi spazi e caratteri non numerici tranne punto e virgola
        price_clean = re.sub(r'[^\d,.]', '', price_text.replace(' ', ''))
        # Sostituisci virgola con punto se presente
        price_clean = price_clean.replace(',', '.')
        
        try:
            # Estrai solo numeri e punto
            price_match = re.search(r'(\d+\.?\d*)', price_clean)
            if price_match:
                return float(price_match.group(1))
        except (ValueError, AttributeError):
            pass
        
        return None
    
    def extract_product_id(self, url):
        """Estrae un ID univoco dal prodotto dall'URL o dal contenuto"""
        # Prova a estrarre dall'URL
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split('/') if p]
        if path_parts:
            return path_parts[-1] or url
        return url
    
    def scrape_product_page(self, url):
        """Scrapa una singola pagina prodotto"""
        try:
            time.sleep(config.REQUEST_DELAY)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Estrai nome prodotto
            name_elem = soup.find('h1') or soup.find('title')
            name = name_elem.get_text(strip=True) if name_elem else "Prodotto sconosciuto"
            
            # Estrai prezzo - cerca vari pattern comuni
            price = None
            
            # 1. Cerca meta tag per prezzo strutturato
            meta_price = soup.find('meta', property=re.compile(r'price', re.I))
            if meta_price and meta_price.get('content'):
                price = self.extract_price(meta_price.get('content'))
            
            # 2. Cerca elementi con classi specifiche per prezzo
            if not price:
                price_patterns = [
                    {'tag': 'span', 'class': re.compile(r'price|prezzo', re.I)},
                    {'tag': 'div', 'class': re.compile(r'price|prezzo', re.I)},
                    {'tag': 'p', 'class': re.compile(r'price|prezzo', re.I)},
                    {'tag': 'span', 'class': re.compile(r'amount|valore|cost', re.I)},
                    {'tag': 'strong', 'class': re.compile(r'price|prezzo', re.I)},
                ]
                
                for pattern in price_patterns:
                    elems = soup.find_all(pattern['tag'], class_=pattern['class'])
                    for elem in elems:
                        price_text = elem.get_text()
                        price = self.extract_price(price_text)
                        if price and price > 0:  # Verifica che sia un prezzo valido
                            break
                    if price:
                        break
            
            # 3. Cerca pattern con simbolo €
            if not price:
                price_elems = soup.find_all(string=re.compile(r'[\d.,]+\s*€|€\s*[\d.,]+', re.I))
                for elem in price_elems:
                    price = self.extract_price(elem)
                    if price and price > 0:
                        break
            
            # 4. Cerca in tutti i testi che contengono numeri seguiti da €
            if not price:
                all_text = soup.get_text()
                price_matches = re.findall(r'(\d+[.,]?\d*)\s*€', all_text)
                for match in price_matches:
                    potential_price = self.extract_price(match)
                    # Filtra prezzi ragionevoli (tra 5 e 500 euro per profumi)
                    if potential_price and 5 <= potential_price <= 500:
                        price = potential_price
                        break
            
            # Estrai brand
            brand = None
            brand_elem = soup.find('a', class_=re.compile(r'brand|marca', re.I)) or \
                        soup.find('span', class_=re.compile(r'brand|marca', re.I))
            if brand_elem:
                brand = brand_elem.get_text(strip=True)
            
            # Se non trovato, prova a estrarre dal nome
            if not brand and name:
                # Pattern comune: "Brand Name Product"
                parts = name.split()
                if len(parts) > 1:
                    brand = parts[0]
            
            product_id = self.extract_product_id(url)
            
            return {
                'product_id': product_id,
                'name': name,
                'brand': brand,
                'url': url,
                'price': price
            }
            
        except Exception as e:
            logger.error(f"Errore nello scraping di {url}: {e}")
            return None
    
    def is_product_url(self, href):
        """Verifica se un href è un link a un prodotto"""
        if not href:
            return False
        
        href_lower = href.lower()
        
        # Escludi categorie e pagine generiche
        exclude_patterns = [
            '/categoria/', '/category/', '/marca/', '/brand/',
            '/tutti-', '/all-', '/search', '/profumi/?',
            '/outlet', '/tester', '/set-regalo', '/notizie',
            '/chi-siamo', '/contatto', '/blog', '/eventi',
            '/pedigree', '/buoni-regalo', '/idee-regalo',
            '/perfume-bar', '/oriental-court', '/k-beauty'
        ]
        
        if any(exclude in href_lower for exclude in exclude_patterns):
            return False
        
        # Pattern per prodotti: devono avere ml/g E (eau-de-parfum/edt/parfum)
        has_size = any(x in href_lower for x in ['ml', 'g', '-50', '-100', '-75', '-30'])
        has_type = any(x in href_lower for x in [
            'eau-de-parfum', 'eau-de-toilette', 'parfum', 
            '-edp-', '-edt-', 'extrait'
        ])
        
        # Oppure pattern con _z seguito da numeri (ID prodotto)
        has_product_id = bool(re.search(r'_[zZ]\d+', href))
        
        # Deve essere un prodotto se ha (tipo E dimensione) O ID prodotto
        if (has_size and has_type) or has_product_id:
            # Non deve essere una categoria (non finisce con / o ha troppi /)
            if not href_lower.endswith('/') or href_lower.count('/') <= 3:
                return True
        
        return False
    
    def find_product_links(self, soup, seen_urls):
        """Trova tutti i link prodotto in una pagina"""
        product_links = []
        
        # Metodo 1: Cerca tutti i link e filtra
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            if self.is_product_url(href):
                full_url = urljoin(self.base_url, href)
                clean_url = full_url.split('?')[0].split('#')[0]
                
                if clean_url not in seen_urls:
                    seen_urls.add(clean_url)
                    product_links.append(clean_url)
        
        # Metodo 2: Cerca elementi prodotto e estrai link
        product_elements = soup.find_all(['div', 'article', 'li', 'section'], 
                                        class_=re.compile(r'product|item|card|box|grid-item', re.I))
        
        for elem in product_elements:
            # Cerca link dentro l'elemento
            link_elem = elem.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                if self.is_product_url(href):
                    full_url = urljoin(self.base_url, href)
                    clean_url = full_url.split('?')[0].split('#')[0]
                    
                    if clean_url not in seen_urls:
                        seen_urls.add(clean_url)
                        product_links.append(clean_url)
        
        return product_links
    
    def get_next_page_url(self, soup, current_url):
        """Trova l'URL della pagina successiva"""
        # Cerca bottoni next
        next_btn = soup.find('a', class_=re.compile(r'next|btn-pager-next', re.I))
        if next_btn and next_btn.get('href'):
            return urljoin(self.base_url, next_btn['href'])
        
        # Cerca link con testo "successivo" o "next"
        for link in soup.find_all('a', href=True):
            text = link.get_text(strip=True).lower()
            if 'successivo' in text or 'next' in text or '>' in text:
                href = link.get('href')
                if href and href != current_url:
                    return urljoin(self.base_url, href)
        
        # Prova paginazione numerica
        parsed = urlparse(current_url)
        if 'page' in parsed.query:
            # Estrai numero pagina corrente
            import re as regex_module
            page_match = regex_module.search(r'page=(\d+)', parsed.query)
            if page_match:
                next_page = int(page_match.group(1)) + 1
                if '?' in current_url:
                    next_url = f"{current_url.split('?')[0]}?page={next_page}"
                else:
                    next_url = f"{current_url}?page={next_page}"
                return next_url
        
        return None
    
    def scrape_category(self, category_url, max_pages=10):
        """Scrapa una categoria di prodotti con paginazione intelligente"""
        products = []
        seen_urls = set()
        current_url = category_url
        pages_scraped = 0
        
        while pages_scraped < max_pages:
            try:
                time.sleep(config.REQUEST_DELAY)
                response = self.session.get(current_url, timeout=30)
                
                # Se 404, prova senza parametri
                if response.status_code == 404:
                    # Rimuovi eventuali parametri
                    clean_url = current_url.split('?')[0]
                    if clean_url != current_url:
                        current_url = clean_url
                        response = self.session.get(current_url, timeout=30)
                
                if response.status_code != 200:
                    logger.warning(f"Status {response.status_code} per {current_url}, fermo")
                    break
                
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Trova link prodotti
                product_links = self.find_product_links(soup, seen_urls)
                
                if not product_links:
                    logger.info(f"Nessun prodotto trovato alla pagina, fermo lo scraping")
                    break
                
                logger.info(f"Trovati {len(product_links)} prodotti alla pagina {pages_scraped + 1}")
                
                # Scrapa ogni prodotto
                for product_url in product_links:
                    product_data = self.scrape_product_page(product_url)
                    if product_data and product_data.get('price'):
                        products.append(product_data)
                
                pages_scraped += 1
                
                # Trova prossima pagina
                next_url = self.get_next_page_url(soup, current_url)
                if not next_url or next_url == current_url:
                    logger.info("Nessuna pagina successiva trovata")
                    break
                
                current_url = next_url
                
            except Exception as e:
                logger.error(f"Errore nello scraping della categoria: {e}")
                break
        
        return products
    
    def discover_categories(self):
        """Scopre automaticamente le categorie dal sito"""
        # Categorie principali note (fallback)
        main_categories = [
            f"{self.base_url}/eau-de-parfum-da-donna/",
            f"{self.base_url}/eau-de-toilette-da-donna/",
            f"{self.base_url}/colonia-femminile/",
            f"{self.base_url}/eau-de-parfum-da-uomo/",
            f"{self.base_url}/eau-de-toilette-da-uomo/",
            f"{self.base_url}/colonia-maschile/",
            f"{self.base_url}/unisex-eau-de-parfum/",
            f"{self.base_url}/unisex-eau-de-toilette/",
            f"{self.base_url}/unisex-colonia/",
            f"{self.base_url}/niche-eau-de-parfum/",
            f"{self.base_url}/niche-eau-de-toilette/",
        ]
        
        categories = set(main_categories)
        
        try:
            # Prendi homepage
            response = self.session.get(self.base_url, timeout=30)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Cerca link categorie
            for link in soup.find_all('a', href=True):
                href = link['href']
                href_lower = href.lower()
                
                # Pattern per categorie profumi
                if any(keyword in href_lower for keyword in [
                    'eau-de-parfum', 'eau-de-toilette', 'colonia',
                    'parfum', 'niche'
                ]):
                    # Deve finire con / e non essere un prodotto
                    if href.endswith('/') and not self.is_product_url(href):
                        full_url = urljoin(self.base_url, href)
                        categories.add(full_url)
            
            categories.update(main_categories)
            
        except Exception as e:
            logger.warning(f"Errore nella scoperta categorie: {e}, uso categorie predefinite")
            # Fallback a categorie predefinite
            categories = set(main_categories)
        
        return list(categories)
    
    def scrape_homepage_products(self):
        """Scrapa prodotti direttamente dalla homepage"""
        products = []
        seen_urls = set()
        
        try:
            logger.info("Scraping prodotti dalla homepage...")
            response = self.session.get(self.base_url, timeout=30)
            soup = BeautifulSoup(response.content, 'lxml')
            
            product_links = self.find_product_links(soup, seen_urls)
            logger.info(f"Trovati {len(product_links)} prodotti nella homepage")
            
            for product_url in product_links:
                product_data = self.scrape_product_page(product_url)
                if product_data and product_data.get('price'):
                    products.append(product_data)
        
        except Exception as e:
            logger.error(f"Errore nello scraping homepage: {e}")
        
        return products
    
    def scrape_all_profumes(self):
        """Scrapa tutte le categorie di profumi con scoperta automatica"""
        all_products = []
        seen_urls = set()  # Per evitare duplicati tra categorie
        
        # 1. Scrapa prodotti dalla homepage
        logger.info("=" * 60)
        logger.info("FASE 1: Scraping homepage")
        logger.info("=" * 60)
        homepage_products = self.scrape_homepage_products()
        for product in homepage_products:
            if product['url'] not in seen_urls:
                seen_urls.add(product['url'])
                all_products.append(product)
        logger.info(f"Prodotti homepage: {len(homepage_products)}")
        
        # 2. Scopri e scrapa categorie
        logger.info("=" * 60)
        logger.info("FASE 2: Scoperta e scraping categorie")
        logger.info("=" * 60)
        categories = self.discover_categories()
        logger.info(f"Trovate {len(categories)} categorie")
        
        for i, category_url in enumerate(categories, 1):
            logger.info(f"[{i}/{len(categories)}] Scraping categoria: {category_url}")
            try:
                products = self.scrape_category(category_url, max_pages=15)
                
                # Filtra duplicati
                unique_products = []
                for product in products:
                    if product['url'] not in seen_urls:
                        seen_urls.add(product['url'])
                        unique_products.append(product)
                
                all_products.extend(unique_products)
                logger.info(f"  ✓ Trovati {len(unique_products)} prodotti unici (totale: {len(all_products)})")
                
            except Exception as e:
                logger.error(f"  ✗ Errore categoria {category_url}: {e}")
                continue
        
        logger.info("=" * 60)
        logger.info(f"TOTALE PRODOTTI UNICI TROVATI: {len(all_products)}")
        logger.info("=" * 60)
        
        return all_products
