"""
Test per il modulo scraper
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
import scraper


class TestExtractPrice:
    """Test per il metodo extract_price"""
    
    def test_extract_price_euro_symbol_after(self):
        """Prezzo con simbolo € dopo il numero"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price("99,99 €") == 99.99
    
    def test_extract_price_euro_symbol_before(self):
        """Prezzo con simbolo € prima del numero"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price("€ 99,99") == 99.99
    
    def test_extract_price_with_dot(self):
        """Prezzo con punto come separatore decimale"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price("99.99") == 99.99
    
    def test_extract_price_with_comma(self):
        """Prezzo con virgola come separatore decimale"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price("99,99") == 99.99
    
    def test_extract_price_integer(self):
        """Prezzo intero senza decimali"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price("100") == 100.0
    
    def test_extract_price_empty_string(self):
        """Stringa vuota"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price("") is None
    
    def test_extract_price_none(self):
        """Valore None"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price(None) is None
    
    def test_extract_price_invalid(self):
        """Stringa non valida"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price("prezzo non disponibile") is None
    
    def test_extract_price_with_spaces(self):
        """Prezzo con spazi extra"""
        s = scraper.CasaDelProfumoScraper()
        assert s.extract_price("  99 , 99  €  ") == 99.99


class TestExtractProductId:
    """Test per il metodo extract_product_id"""
    
    def test_extract_id_from_url(self):
        """Estrae ID dall'URL"""
        s = scraper.CasaDelProfumoScraper()
        url = "https://www.casadelprofumo.it/test-product-100ml/"
        assert s.extract_product_id(url) == "test-product-100ml"
    
    def test_extract_id_url_with_params(self):
        """URL con parametri"""
        s = scraper.CasaDelProfumoScraper()
        url = "https://www.casadelprofumo.it/product/?id=123"
        # Dovrebbe estrarre l'ultimo segmento del path
        result = s.extract_product_id(url)
        assert result == "product"


class TestIsProductUrl:
    """Test per il metodo is_product_url"""
    
    def test_valid_product_url_edp(self):
        """URL prodotto EDP valido"""
        s = scraper.CasaDelProfumoScraper()
        assert s.is_product_url("/test-eau-de-parfum-100ml") is True
    
    def test_valid_product_url_edt(self):
        """URL prodotto EDT valido"""
        s = scraper.CasaDelProfumoScraper()
        assert s.is_product_url("/test-eau-de-toilette-50ml") is True
    
    def test_valid_product_url_with_id(self):
        """URL prodotto con ID"""
        s = scraper.CasaDelProfumoScraper()
        assert s.is_product_url("/product_z12345") is True
    
    def test_invalid_category_url(self):
        """URL categoria non è un prodotto"""
        s = scraper.CasaDelProfumoScraper()
        assert s.is_product_url("/categoria/profumi/") is False
    
    def test_invalid_brand_url(self):
        """URL marca non è un prodotto"""
        s = scraper.CasaDelProfumoScraper()
        assert s.is_product_url("/marca/dior/") is False
    
    def test_empty_url(self):
        """URL vuoto"""
        s = scraper.CasaDelProfumoScraper()
        assert s.is_product_url("") is False
    
    def test_none_url(self):
        """URL None"""
        s = scraper.CasaDelProfumoScraper()
        assert s.is_product_url(None) is False


class TestScrapeProductPage:
    """Test per il metodo scrape_product_page"""
    
    @patch.object(scraper.CasaDelProfumoScraper, '_make_request')
    def test_scrape_valid_page(self, mock_request, sample_html_with_price):
        """Scraping di una pagina valida"""
        mock_response = Mock()
        mock_response.content = sample_html_with_price.encode()
        mock_request.return_value = mock_response
        
        s = scraper.CasaDelProfumoScraper()
        result = s.scrape_product_page("https://www.casadelprofumo.it/test/")
        
        assert result is not None
        assert result['price'] == 99.99
        assert 'Test Profumo' in result['name']
    
    @patch.object(scraper.CasaDelProfumoScraper, '_make_request')
    def test_scrape_page_without_price(self, mock_request, sample_html_without_price):
        """Scraping di una pagina senza prezzo"""
        mock_response = Mock()
        mock_response.content = sample_html_without_price.encode()
        mock_request.return_value = mock_response
        
        s = scraper.CasaDelProfumoScraper()
        result = s.scrape_product_page("https://www.casadelprofumo.it/test/")
        
        assert result is not None
        assert result['price'] is None
    
    @patch.object(scraper.CasaDelProfumoScraper, '_make_request')
    def test_scrape_request_error(self, mock_request):
        """Errore durante la richiesta"""
        mock_request.side_effect = Exception("Connection error")
        
        s = scraper.CasaDelProfumoScraper()
        result = s.scrape_product_page("https://www.casadelprofumo.it/test/")
        
        assert result is None


class TestFindProductLinks:
    """Test per il metodo find_product_links"""
    
    def test_find_links_in_page(self):
        """Trova link prodotti in una pagina"""
        html = """
        <html>
        <body>
            <a href="/test-eau-de-parfum-100ml/">Product 1</a>
            <a href="/test-eau-de-toilette-50ml/">Product 2</a>
            <a href="/categoria/profumi/">Category</a>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'lxml')
        s = scraper.CasaDelProfumoScraper()
        seen_urls = set()
        
        links = s.find_product_links(soup, seen_urls)
        
        # Dovrebbe trovare i prodotti ma non la categoria
        assert len(links) == 2
        assert any('eau-de-parfum' in link for link in links)
        assert any('eau-de-toilette' in link for link in links)
    
    def test_no_duplicate_links(self):
        """Non restituisce link duplicati"""
        html = """
        <html>
        <body>
            <a href="/test-eau-de-parfum-100ml/">Product 1</a>
            <a href="/test-eau-de-parfum-100ml/">Product 1 Again</a>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'lxml')
        s = scraper.CasaDelProfumoScraper()
        seen_urls = set()
        
        links = s.find_product_links(soup, seen_urls)
        
        assert len(links) == 1
