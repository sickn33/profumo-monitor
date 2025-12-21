"""
Scraper asincrono per casadelprofumo.it

Versione asincrona dello scraper per migliorare le performance
quando si devono scrapare molti prodotti in parallelo.
"""
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import config
import logging
from typing import List, Dict, Optional, Set
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Eccezioni per cui fare retry
RETRYABLE_EXCEPTIONS = (
    aiohttp.ClientError,
    asyncio.TimeoutError,
)


class AsyncCasaDelProfumoScraper:
    """Scraper asincrono per il sito casadelprofumo.it"""
    
    def __init__(self, max_concurrent: int = 5):
        """
        Args:
            max_concurrent: Numero massimo di richieste concorrenti
        """
        self.base_url = config.TARGET_SITE
        self.max_concurrent = max_concurrent
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Context manager async entry"""
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        timeout = aiohttp.ClientTimeout(total=30)
        self._session = aiohttp.ClientSession(
            headers={
                'User-Agent': config.USER_AGENT,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8',
            },
            timeout=timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager async exit"""
        if self._session:
            await self._session.close()
        return False
    
    def extract_price(self, price_text: str) -> Optional[float]:
        """Estrae il prezzo da una stringa"""
        if not price_text:
            return None
        
        price_clean = re.sub(r'[^\d,.]', '', price_text.replace(' ', ''))
        price_clean = price_clean.replace(',', '.')
        
        try:
            price_match = re.search(r'(\d+\.?\d*)', price_clean)
            if price_match:
                return float(price_match.group(1))
        except (ValueError, AttributeError):
            pass
        
        return None
    
    def extract_product_id(self, url: str) -> str:
        """Estrae un ID univoco dal prodotto dall'URL"""
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split('/') if p]
        if path_parts:
            return path_parts[-1] or url
        return url
    
    def is_product_url(self, href: str) -> bool:
        """Verifica se un href è un link a un prodotto"""
        if not href:
            return False
        
        href_lower = href.lower()
        
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
        
        has_size = any(x in href_lower for x in ['ml', 'g', '-50', '-100', '-75', '-30'])
        has_type = any(x in href_lower for x in [
            'eau-de-parfum', 'eau-de-toilette', 'parfum', 
            '-edp-', '-edt-', 'extrait'
        ])
        has_product_id = bool(re.search(r'_[zZ]\d+', href))
        
        if (has_size and has_type) or has_product_id:
            if not href_lower.endswith('/') or href_lower.count('/') <= 3:
                return True
        
        return False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS)
    )
    async def _fetch(self, url: str) -> str:
        """Esegue una richiesta HTTP con rate limiting e retry"""
        async with self._semaphore:
            await asyncio.sleep(config.REQUEST_DELAY)
            async with self._session.get(url) as response:
                response.raise_for_status()
                return await response.text()
    
    async def scrape_product_page(self, url: str) -> Optional[Dict]:
        """Scrapa una singola pagina prodotto"""
        try:
            html = await self._fetch(url)
            soup = BeautifulSoup(html, 'lxml')
            
            # Estrai nome prodotto
            name_elem = soup.find('h1') or soup.find('title')
            name = name_elem.get_text(strip=True) if name_elem else "Prodotto sconosciuto"
            
            # Estrai prezzo
            price = None
            
            # 1. Meta tag
            meta_price = soup.find('meta', property=re.compile(r'price', re.I))
            if meta_price and meta_price.get('content'):
                price = self.extract_price(meta_price.get('content'))
            
            # 2. Classi specifiche
            if not price:
                price_patterns = [
                    {'tag': 'span', 'class': re.compile(r'price|prezzo', re.I)},
                    {'tag': 'div', 'class': re.compile(r'price|prezzo', re.I)},
                    {'tag': 'p', 'class': re.compile(r'price|prezzo', re.I)},
                ]
                
                for pattern in price_patterns:
                    elems = soup.find_all(pattern['tag'], class_=pattern['class'])
                    for elem in elems:
                        price = self.extract_price(elem.get_text())
                        if price and price > 0:
                            break
                    if price:
                        break
            
            # 3. Pattern €
            if not price:
                price_elems = soup.find_all(string=re.compile(r'[\d.,]+\s*€|€\s*[\d.,]+', re.I))
                for elem in price_elems:
                    price = self.extract_price(elem)
                    if price and price > 0:
                        break
            
            # 4. Testo generale
            if not price:
                all_text = soup.get_text()
                price_matches = re.findall(r'(\d+[.,]?\d*)\s*€', all_text)
                for match in price_matches:
                    potential_price = self.extract_price(match)
                    if potential_price and 5 <= potential_price <= 500:
                        price = potential_price
                        break
            
            # Estrai brand
            brand = None
            brand_elem = soup.find('a', class_=re.compile(r'brand|marca', re.I)) or \
                        soup.find('span', class_=re.compile(r'brand|marca', re.I))
            if brand_elem:
                brand = brand_elem.get_text(strip=True)
            
            if not brand and name:
                parts = name.split()
                if len(parts) > 1:
                    brand = parts[0]
            
            return {
                'product_id': self.extract_product_id(url),
                'name': name,
                'brand': brand,
                'url': url,
                'price': price
            }
            
        except Exception as e:
            logger.error(f"Errore nello scraping di {url}: {e}")
            return None
    
    async def scrape_products_batch(self, urls: List[str]) -> List[Dict]:
        """Scrapa una lista di URL di prodotti in parallelo"""
        tasks = [self.scrape_product_page(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        products = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Errore per {urls[i]}: {result}")
            elif result and result.get('price'):
                products.append(result)
        
        return products
    
    def find_product_links(self, soup: BeautifulSoup, seen_urls: Set[str]) -> List[str]:
        """Trova tutti i link prodotto in una pagina"""
        product_links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            if self.is_product_url(href):
                full_url = urljoin(self.base_url, href)
                clean_url = full_url.split('?')[0].split('#')[0]
                
                if clean_url not in seen_urls:
                    seen_urls.add(clean_url)
                    product_links.append(clean_url)
        
        product_elements = soup.find_all(['div', 'article', 'li', 'section'], 
                                        class_=re.compile(r'product|item|card|box|grid-item', re.I))
        
        for elem in product_elements:
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
    
    async def scrape_category(self, category_url: str, max_pages: int = 5) -> List[Dict]:
        """Scrapa una categoria di prodotti"""
        products = []
        seen_urls: Set[str] = set()
        current_url = category_url
        pages_scraped = 0
        
        while pages_scraped < max_pages:
            try:
                html = await self._fetch(current_url)
                soup = BeautifulSoup(html, 'lxml')
                
                product_links = self.find_product_links(soup, seen_urls)
                
                if not product_links:
                    logger.info(f"Nessun prodotto trovato alla pagina, fermo lo scraping")
                    break
                
                logger.info(f"Trovati {len(product_links)} prodotti alla pagina {pages_scraped + 1}")
                
                # Scrapa i prodotti in parallelo
                page_products = await self.scrape_products_batch(product_links)
                products.extend(page_products)
                
                pages_scraped += 1
                
                # Trova prossima pagina
                next_btn = soup.find('a', class_=re.compile(r'next|btn-pager-next', re.I))
                if not next_btn or not next_btn.get('href'):
                    logger.info("Nessuna pagina successiva trovata")
                    break
                
                next_url = urljoin(self.base_url, next_btn['href'])
                if next_url == current_url:
                    break
                
                current_url = next_url
                
            except Exception as e:
                logger.error(f"Errore nello scraping della categoria: {e}")
                break
        
        return products
    
    async def scrape_all_profumes(self) -> List[Dict]:
        """Scrapa tutte le categorie di profumi"""
        all_products = []
        seen_urls: Set[str] = set()
        
        # 1. Scrapa homepage
        logger.info("=" * 60)
        logger.info("FASE 1: Scraping homepage (async)")
        logger.info("=" * 60)
        
        try:
            html = await self._fetch(self.base_url)
            soup = BeautifulSoup(html, 'lxml')
            
            product_links = self.find_product_links(soup, seen_urls)
            logger.info(f"Trovati {len(product_links)} prodotti nella homepage")
            
            if product_links:
                homepage_products = await self.scrape_products_batch(product_links)
                all_products.extend(homepage_products)
                logger.info(f"Prodotti homepage scrapati: {len(homepage_products)}")
        
        except Exception as e:
            logger.error(f"Errore nello scraping homepage: {e}")
        
        # 2. Scrapa categorie
        logger.info("=" * 60)
        logger.info("FASE 2: Scraping categorie (async)")
        logger.info("=" * 60)
        
        categories = getattr(config, 'SCRAPE_CATEGORIES', [])
        logger.info(f"Trovate {len(categories)} categorie da scrapare")
        
        for i, category_url in enumerate(categories, 1):
            logger.info(f"[{i}/{len(categories)}] Scraping categoria: {category_url}")
            try:
                products = await self.scrape_category(category_url, max_pages=5)
                
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


async def run_async_scraping() -> List[Dict]:
    """Helper function per eseguire lo scraping asincrono"""
    async with AsyncCasaDelProfumoScraper(max_concurrent=5) as scraper:
        return await scraper.scrape_all_profumes()


def scrape_all_async() -> List[Dict]:
    """Wrapper sincrono per lo scraping asincrono"""
    return asyncio.run(run_async_scraping())


if __name__ == "__main__":
    # Test dello scraper asincrono
    products = scrape_all_async()
    print(f"Trovati {len(products)} prodotti")
