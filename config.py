"""
Configurazione per il monitoraggio prezzi profumi

Usa pydantic per validazione automatica dei valori di configurazione.
I valori sono letti dalle variabili d'ambiente o da un file .env
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Configurazione dell'applicazione con validazione automatica"""
    
    # Database
    database_url: str = Field(
        default='sqlite:///profumi_prices.db',
        description="URL di connessione al database"
    )
    
    # Sito da monitorare
    target_site: str = Field(
        default="https://www.casadelprofumo.it",
        description="URL del sito da monitorare"
    )
    
    # Notifiche Telegram (opzionale)
    telegram_bot_token: str = Field(
        default='',
        description="Token del bot Telegram"
    )
    telegram_chat_id: str = Field(
        default='',
        description="ID della chat Telegram per le notifiche"
    )
    
    # Notifiche Email (opzionale)
    email_enabled: bool = Field(
        default=False,
        description="Abilita notifiche email"
    )
    email_smtp_server: str = Field(
        default='smtp.gmail.com',
        description="Server SMTP per l'invio email"
    )
    email_smtp_port: int = Field(
        default=587,
        ge=1,
        le=65535,
        description="Porta del server SMTP"
    )
    email_user: str = Field(
        default='',
        description="Username per l'autenticazione SMTP"
    )
    email_password: str = Field(
        default='',
        description="Password per l'autenticazione SMTP"
    )
    email_to: str = Field(
        default='',
        description="Indirizzo email destinatario"
    )
    
    # Soglie per le notifiche
    price_drop_threshold: float = Field(
        default=0.15,
        ge=0.0,
        le=1.0,
        description="Soglia percentuale per calo di prezzo significativo (0.15 = 15%)"
    )
    competitor_price_diff: float = Field(
        default=0.20,
        ge=0.0,
        le=1.0,
        description="Soglia differenza prezzo competitor (0.20 = 20%)"
    )
    min_price_for_monitoring: float = Field(
        default=10.0,
        ge=0.0,
        description="Prezzo minimo per includere un prodotto nel monitoraggio"
    )
    
    # Soglie aggiuntive per price_analyzer
    error_price_threshold: float = Field(
        default=0.30,
        ge=0.0,
        le=1.0,
        description="Soglia per rilevare errori di prezzo (prezzo < 30% del massimo)"
    )
    new_low_threshold: float = Field(
        default=0.05,
        ge=0.0,
        le=1.0,
        description="Soglia minima per alert nuovo prezzo minimo (5%)"
    )
    
    # Scheduler
    check_interval_minutes: int = Field(
        default=15,
        ge=1,
        le=1440,
        description="Intervallo di controllo in minuti (1-1440)"
    )
    
    # User-Agent per le richieste
    user_agent: str = Field(
        default='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        description="User-Agent per le richieste HTTP"
    )
    
    # Delay tra le richieste (secondi)
    request_delay: float = Field(
        default=2.0,
        ge=0.5,
        le=60.0,
        description="Delay tra le richieste HTTP in secondi (0.5-60)"
    )
    
    # Categorie da scrapare (configurabili)
    scrape_categories: List[str] = Field(
        default=[
            "https://www.casadelprofumo.it/outlet-di-profumi/?dynamic_filter%5Bparameters%5D%5B71%5D%5Bvalue%5D%5B0%5D=55649&dynamic_filter%5Bparameters%5D%5B71%5D%5Bvalue%5D%5B1%5D=63837",
            "https://www.casadelprofumo.it/profumi-da-uomo/",
            "https://www.casadelprofumo.it/tester-di-profumi/f/da-uomo%7Cunisex/",
            "https://www.casadelprofumo.it/profumi-unisex/",
        ],
        description="Lista delle categorie da scrapare"
    )
    
    @field_validator('check_interval_minutes')
    @classmethod
    def validate_interval(cls, v: int) -> int:
        """Valida l'intervallo di controllo"""
        if v < 1:
            raise ValueError('L\'intervallo di controllo deve essere almeno 1 minuto')
        if v > 1440:
            raise ValueError('L\'intervallo di controllo non può superare 1440 minuti (24 ore)')
        return v
    
    @field_validator('price_drop_threshold', 'competitor_price_diff', 'error_price_threshold', 'new_low_threshold')
    @classmethod
    def validate_threshold(cls, v: float) -> float:
        """Valida le soglie percentuali"""
        if not 0.0 <= v <= 1.0:
            raise ValueError('La soglia deve essere tra 0.0 e 1.0')
        return v
    
    @property
    def check_interval_hours(self) -> float:
        """Ritorna l'intervallo in ore (per compatibilità)"""
        return self.check_interval_minutes / 60
    
    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8',
        'extra': 'ignore',  # Ignora variabili d'ambiente extra
    }


# Istanza singleton delle impostazioni
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Ottiene l'istanza singleton delle impostazioni"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Esporta le variabili per compatibilità con il codice esistente
# Questo permette di usare `import config; config.DATABASE_URL`
_s = get_settings()

DATABASE_URL = _s.database_url
TARGET_SITE = _s.target_site
TELEGRAM_BOT_TOKEN = _s.telegram_bot_token
TELEGRAM_CHAT_ID = _s.telegram_chat_id
EMAIL_ENABLED = _s.email_enabled
EMAIL_SMTP_SERVER = _s.email_smtp_server
EMAIL_SMTP_PORT = _s.email_smtp_port
EMAIL_USER = _s.email_user
EMAIL_PASSWORD = _s.email_password
EMAIL_TO = _s.email_to
PRICE_DROP_THRESHOLD = _s.price_drop_threshold
COMPETITOR_PRICE_DIFF = _s.competitor_price_diff
MIN_PRICE_FOR_MONITORING = _s.min_price_for_monitoring
ERROR_PRICE_THRESHOLD = _s.error_price_threshold
NEW_LOW_THRESHOLD = _s.new_low_threshold
CHECK_INTERVAL_MINUTES = _s.check_interval_minutes
CHECK_INTERVAL_HOURS = _s.check_interval_hours
USER_AGENT = _s.user_agent
REQUEST_DELAY = _s.request_delay
SCRAPE_CATEGORIES = _s.scrape_categories
