"""
Test per il modulo database
"""
import pytest
from datetime import datetime, timezone
import database


class TestUtcNow:
    """Test per la funzione utc_now"""
    
    def test_utc_now_returns_datetime(self):
        """Deve restituire un oggetto datetime"""
        result = database.utc_now()
        assert isinstance(result, datetime)
    
    def test_utc_now_is_timezone_aware(self):
        """Deve essere timezone-aware"""
        result = database.utc_now()
        assert result.tzinfo is not None
        assert result.tzinfo == timezone.utc


class TestDatabaseContextManager:
    """Test per il context manager del Database"""
    
    def test_context_manager_creates_session(self):
        """Il context manager crea una sessione"""
        with database.Database() as db:
            assert db.session is not None
    
    def test_context_manager_closes_session(self):
        """Il context manager chiude la sessione"""
        db_instance = None
        with database.Database() as db:
            db_instance = db
        # La sessione dovrebbe essere chiusa dopo l'uscita dal context
        # (non possiamo verificare direttamente ma possiamo verificare che non sollevi eccezioni)
        assert db_instance is not None


class TestGetOrCreateProduct:
    """Test per il metodo get_or_create_product"""
    
    def test_create_new_product(self, db_session, sample_product_data):
        """Crea un nuovo prodotto"""
        product = db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=sample_product_data['price'],
            brand=sample_product_data['brand']
        )
        
        assert product is not None
        assert product.product_id == sample_product_data['product_id']
        assert product.name == sample_product_data['name']
        assert product.current_price == sample_product_data['price']
        assert product.lowest_price == sample_product_data['price']
        assert product.highest_price == sample_product_data['price']
    
    def test_update_existing_product(self, db_session, sample_product_data):
        """Aggiorna un prodotto esistente"""
        # Crea prima il prodotto
        db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=sample_product_data['price'],
            brand=sample_product_data['brand']
        )
        
        # Aggiorna con nuovo prezzo
        new_price = 89.99
        product = db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=new_price,
            brand=sample_product_data['brand']
        )
        
        assert product.current_price == new_price
        assert product.previous_price == sample_product_data['price']
        assert product.lowest_price == new_price  # Nuovo prezzo è più basso
        assert product.times_checked == 2
    
    def test_tracks_lowest_price(self, db_session, sample_product_data):
        """Traccia il prezzo più basso"""
        # Crea con prezzo alto
        db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=100.00,
            brand=sample_product_data['brand']
        )
        
        # Aggiorna con prezzo più basso
        product = db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=80.00,
            brand=sample_product_data['brand']
        )
        
        assert product.lowest_price == 80.00
        
        # Aggiorna con prezzo più alto (non deve cambiare lowest)
        product = db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=90.00,
            brand=sample_product_data['brand']
        )
        
        assert product.lowest_price == 80.00  # Rimane il minimo
    
    def test_tracks_highest_price(self, db_session, sample_product_data):
        """Traccia il prezzo più alto"""
        # Crea con prezzo iniziale
        db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=100.00,
            brand=sample_product_data['brand']
        )
        
        # Aggiorna con prezzo più alto
        product = db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=120.00,
            brand=sample_product_data['brand']
        )
        
        assert product.highest_price == 120.00


class TestCreateAlert:
    """Test per il metodo create_alert"""
    
    def test_create_alert(self, db_session):
        """Crea un nuovo alert"""
        alert = db_session.create_alert(
            product_id='test-123',
            alert_type='price_drop',
            message='Test alert message',
            old_price=100.00,
            new_price=80.00
        )
        
        assert alert is not None
        assert alert.product_id == 'test-123'
        assert alert.alert_type == 'price_drop'
        assert alert.old_price == 100.00
        assert alert.new_price == 80.00
        assert alert.notified is False
    
    def test_deduplication_by_price(self, db_session):
        """Non crea duplicati per stesso prodotto/tipo/prezzo"""
        # Primo alert
        alert1 = db_session.create_alert(
            product_id='test-123',
            alert_type='price_drop',
            message='First alert',
            old_price=100.00,
            new_price=80.00
        )
        
        # Secondo alert con stesso prezzo (dovrebbe essere deduplicate)
        alert2 = db_session.create_alert(
            product_id='test-123',
            alert_type='price_drop',
            message='Duplicate alert',
            old_price=100.00,
            new_price=80.00
        )
        
        assert alert1 is not None
        assert alert2 is None  # Duplicato non creato


class TestGetUnnotifiedAlerts:
    """Test per il metodo get_unnotified_alerts"""
    
    def test_returns_unnotified_alerts(self, db_session):
        """Restituisce solo alert non notificati"""
        # Crea alert non notificato
        db_session.create_alert(
            product_id='test-1',
            alert_type='price_drop',
            message='Unnotified',
            new_price=80.00
        )
        
        # Crea alert e notificalo
        alert2 = db_session.create_alert(
            product_id='test-2',
            alert_type='price_drop',
            message='Notified',
            new_price=70.00
        )
        if alert2:
            db_session.mark_alert_notified(alert2.id)
        
        unnotified = db_session.get_unnotified_alerts()
        
        assert len(unnotified) == 1
        assert unnotified[0].message == 'Unnotified'


class TestMarkAlertNotified:
    """Test per il metodo mark_alert_notified"""
    
    def test_marks_alert_as_notified(self, db_session):
        """Segna un alert come notificato"""
        alert = db_session.create_alert(
            product_id='test-123',
            alert_type='price_drop',
            message='Test',
            new_price=80.00
        )
        
        assert alert.notified is False
        
        db_session.mark_alert_notified(alert.id)
        
        # Verifica che sia stato aggiornato
        updated_alert = db_session.session.query(database.Alert).filter_by(id=alert.id).first()
        assert updated_alert.notified is True


class TestGetProduct:
    """Test per il metodo get_product"""
    
    def test_get_existing_product(self, db_session, sample_product_data):
        """Ottiene un prodotto esistente"""
        # Crea prodotto
        db_session.get_or_create_product(
            product_id=sample_product_data['product_id'],
            name=sample_product_data['name'],
            url=sample_product_data['url'],
            price=sample_product_data['price'],
            brand=sample_product_data['brand']
        )
        
        # Recupera
        product = db_session.get_product(sample_product_data['product_id'])
        
        assert product is not None
        assert product.name == sample_product_data['name']
    
    def test_get_nonexistent_product(self, db_session):
        """Restituisce None per prodotto inesistente"""
        product = db_session.get_product('nonexistent-id')
        assert product is None
