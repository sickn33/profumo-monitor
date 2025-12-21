"""
Test per il modulo price_analyzer
"""
import pytest
from unittest.mock import Mock, MagicMock
import price_analyzer
import database


class MockProduct:
    """Mock per oggetto Product"""
    def __init__(self, **kwargs):
        self.product_id = kwargs.get('product_id', 'test-123')
        self.name = kwargs.get('name', 'Test Product')
        self.url = kwargs.get('url', 'https://example.com/product')
        self.current_price = kwargs.get('current_price', 100.0)
        self.previous_price = kwargs.get('previous_price', None)
        self.lowest_price = kwargs.get('lowest_price', None)
        self.highest_price = kwargs.get('highest_price', None)
        self.times_checked = kwargs.get('times_checked', 1)
        self._previous_lowest_price = kwargs.get('_previous_lowest_price', None)
        self._previous_highest_price = kwargs.get('_previous_highest_price', None)


class TestPriceDecreasedSinceLastCheck:
    """Test per il metodo _price_decreased_since_last_check"""
    
    def test_price_decreased(self):
        """Prezzo diminuito"""
        product = MockProduct(current_price=80.0, previous_price=100.0)
        assert price_analyzer.PriceAnalyzer._price_decreased_since_last_check(product) is True
    
    def test_price_increased(self):
        """Prezzo aumentato"""
        product = MockProduct(current_price=120.0, previous_price=100.0)
        assert price_analyzer.PriceAnalyzer._price_decreased_since_last_check(product) is False
    
    def test_price_unchanged(self):
        """Prezzo invariato"""
        product = MockProduct(current_price=100.0, previous_price=100.0)
        assert price_analyzer.PriceAnalyzer._price_decreased_since_last_check(product) is False
    
    def test_no_previous_price(self):
        """Nessun prezzo precedente"""
        product = MockProduct(current_price=100.0, previous_price=None)
        assert price_analyzer.PriceAnalyzer._price_decreased_since_last_check(product) is False
    
    def test_zero_previous_price(self):
        """Prezzo precedente zero"""
        product = MockProduct(current_price=100.0, previous_price=0)
        assert price_analyzer.PriceAnalyzer._price_decreased_since_last_check(product) is False


class TestAnalyzePriceDrop:
    """Test per il metodo analyze_price_drop"""
    
    def test_significant_price_drop(self, db_session):
        """Calo di prezzo significativo (>15%)"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        # 20% di sconto: da 100 a 80
        product = MockProduct(
            current_price=80.0,
            previous_price=100.0
        )
        
        alert = analyzer.analyze_price_drop(product)
        
        assert alert is not None
        assert alert.alert_type == 'price_drop'
        assert '20' in alert.message  # Percentuale nel messaggio
    
    def test_small_price_drop(self, db_session):
        """Calo di prezzo piccolo (<15%)"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        # 5% di sconto: da 100 a 95
        product = MockProduct(
            current_price=95.0,
            previous_price=100.0
        )
        
        alert = analyzer.analyze_price_drop(product)
        
        assert alert is None  # Nessun alert per cali piccoli
    
    def test_no_previous_price(self, db_session):
        """Nessun prezzo precedente"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        product = MockProduct(
            current_price=100.0,
            previous_price=None
        )
        
        alert = analyzer.analyze_price_drop(product)
        
        assert alert is None


class TestAnalyzePriceError:
    """Test per il metodo analyze_price_error"""
    
    def test_possible_price_error(self, db_session):
        """Possibile errore di prezzo (< 30% del massimo)"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        # Prezzo attuale è 20% del massimo (dovrebbe essere un errore)
        product = MockProduct(
            current_price=20.0,
            previous_price=100.0,  # Per attivare _price_decreased_since_last_check
            highest_price=100.0,
            times_checked=5
        )
        
        alert = analyzer.analyze_price_error(product)
        
        assert alert is not None
        assert alert.alert_type == 'error'
    
    def test_normal_price(self, db_session):
        """Prezzo normale (> 30% del massimo)"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        product = MockProduct(
            current_price=50.0,  # 50% del massimo
            previous_price=60.0,
            highest_price=100.0,
            times_checked=5
        )
        
        alert = analyzer.analyze_price_error(product)
        
        assert alert is None
    
    def test_new_product(self, db_session):
        """Prodotto nuovo (pochi check)"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        product = MockProduct(
            current_price=20.0,
            previous_price=100.0,
            highest_price=100.0,
            times_checked=2  # Pochi check
        )
        
        alert = analyzer.analyze_price_error(product)
        
        assert alert is None  # Non genera alert per prodotti nuovi


class TestAnalyzeNewLowPrice:
    """Test per il metodo analyze_new_low_price"""
    
    def test_new_low_price(self, db_session):
        """Nuovo prezzo minimo significativo"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        # Prezzo sceso del 10% rispetto al minimo precedente
        product = MockProduct(
            current_price=90.0,
            previous_price=100.0,
            lowest_price=90.0,  # Aggiornato
            _previous_lowest_price=100.0  # Prima dell'aggiornamento
        )
        
        alert = analyzer.analyze_new_low_price(product)
        
        assert alert is not None
        assert alert.alert_type == 'new_low'
    
    def test_small_price_decrease(self, db_session):
        """Piccolo calo (< 5%) non genera alert"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        # Prezzo sceso del 2%
        product = MockProduct(
            current_price=98.0,
            previous_price=100.0,
            lowest_price=98.0,
            _previous_lowest_price=100.0
        )
        
        alert = analyzer.analyze_new_low_price(product)
        
        assert alert is None
    
    def test_no_previous_lowest(self, db_session):
        """Nessun prezzo minimo precedente"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        product = MockProduct(
            current_price=100.0,
            _previous_lowest_price=None
        )
        
        alert = analyzer.analyze_new_low_price(product)
        
        assert alert is None


class TestAnalyzeProduct:
    """Test per il metodo analyze_product"""
    
    def test_multiple_alerts(self, db_session):
        """Può generare più alert per lo stesso prodotto"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        # Prodotto con calo significativo e nuovo minimo
        product = MockProduct(
            product_id='multi-alert-test',
            current_price=70.0,
            previous_price=100.0,
            lowest_price=70.0,
            highest_price=100.0,
            _previous_lowest_price=100.0,
            _previous_highest_price=100.0,
            times_checked=5
        )
        
        alerts = analyzer.analyze_product(product)
        
        # Dovrebbe generare almeno un alert per il calo di prezzo
        assert len(alerts) >= 1
    
    def test_no_alerts(self, db_session):
        """Nessun alert per prodotto stabile"""
        analyzer = price_analyzer.PriceAnalyzer(db_session)
        
        # Prodotto con prezzo stabile
        product = MockProduct(
            current_price=100.0,
            previous_price=100.0,
            lowest_price=100.0,
            highest_price=100.0,
            times_checked=5
        )
        
        alerts = analyzer.analyze_product(product)
        
        assert len(alerts) == 0
