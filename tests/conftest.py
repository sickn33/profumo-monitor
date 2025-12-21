"""
Configurazione e fixture condivise per pytest
"""
import pytest
import os
import sys

# Aggiungi la directory root al path per importare i moduli
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imposta variabili d'ambiente per i test
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['TELEGRAM_BOT_TOKEN'] = ''
os.environ['TELEGRAM_CHAT_ID'] = ''


@pytest.fixture
def sample_product_data():
    """Dati di esempio per un prodotto"""
    return {
        'product_id': 'test-product-123',
        'name': 'Test Profumo EDP 100ml',
        'brand': 'Test Brand',
        'url': 'https://www.casadelprofumo.it/test-product/',
        'price': 99.99
    }


@pytest.fixture
def sample_html_with_price():
    """HTML di esempio con prezzo"""
    return """
    <html>
    <head><title>Test Profumo - Casa del Profumo</title></head>
    <body>
        <h1>Test Profumo EDP 100ml</h1>
        <span class="price">€ 99,99</span>
        <a class="brand" href="/marca/test-brand/">Test Brand</a>
    </body>
    </html>
    """


@pytest.fixture
def sample_html_without_price():
    """HTML di esempio senza prezzo"""
    return """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <h1>Test Page</h1>
        <p>No price here</p>
    </body>
    </html>
    """


@pytest.fixture
def db_session():
    """Crea una sessione database in memoria per i test"""
    import database
    db = database.Database()
    yield db
    db.close()
