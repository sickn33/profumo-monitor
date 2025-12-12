"""
Configurazione per il monitoraggio prezzi profumi
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///profumi_prices.db')

# Sito da monitorare
TARGET_SITE = "https://www.casadelprofumo.it"

# Notifiche Telegram (opzionale)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Notifiche Email (opzionale)
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False').lower() == 'true'
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_TO = os.getenv('EMAIL_TO', '')

# Soglie per le notifiche
PRICE_DROP_THRESHOLD = float(os.getenv('PRICE_DROP_THRESHOLD', '0.15'))  # 15% di sconto
COMPETITOR_PRICE_DIFF = float(os.getenv('COMPETITOR_PRICE_DIFF', '0.20'))  # 20% più economico
MIN_PRICE_FOR_MONITORING = float(os.getenv('MIN_PRICE_FOR_MONITORING', '10.0'))  # Prezzo minimo da monitorare

# Scheduler
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', '15'))  # Controllo ogni 15 minuti (default)
CHECK_INTERVAL_HOURS = float(os.getenv('CHECK_INTERVAL_HOURS', str(CHECK_INTERVAL_MINUTES / 60)))  # Converti in ore per compatibilità

# User-Agent per le richieste
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Delay tra le richieste (secondi)
REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', '2.0'))
