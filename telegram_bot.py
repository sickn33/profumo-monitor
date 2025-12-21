"""
Bot Telegram interattivo per aggiungere prodotti da monitorare
"""
import logging
import re
import asyncio
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import config
import database
import scraper
import price_analyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_url_from_text(text):
    """Estrae URL da un testo"""
    # Pattern per trovare URL
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    if urls:
        # Prendi il primo URL trovato
        return urls[0].rstrip('.,;:!?)')
    return None


def is_valid_product_url(url):
    """Verifica se l'URL è valido per casadelprofumo.it"""
    if not url:
        return False
    
    try:
        parsed = urlparse(url)
        # Deve essere casadelprofumo.it
        if 'casadelprofumo.it' not in parsed.netloc.lower():
            return False
        
        # Non deve essere una pagina generica (homepage, categorie, etc)
        path = parsed.path.lower().rstrip('/')
        
        # Escludi homepage
        if not path or path == '/':
            return False
        
        # Escludi categorie comuni (pattern più rigorosi)
        exclude_patterns = [
            '/categoria', '/category', '/marca', '/brand',
            '/tutti-', '/all-', '/search', '/profumi-da-',
            '/profumi-unisex', '/profumi-da-uomo', '/profumi-da-donna',
            '/outlet', '/tester', '/set-regalo', '/notizie',
            '/chi-siamo', '/contatto', '/blog', '/eventi',
            '/pedigree', '/buoni-regalo', '/idee-regalo',
            '/perfume-bar', '/oriental-court', '/k-beauty',
            '/eau-de-parfum-da-', '/eau-de-toilette-da-',
            '/colonia-', '/unisex-', '/niche-'
        ]
        
        # Controlla se il path contiene pattern esclusi
        for pattern in exclude_patterns:
            if path.startswith(pattern) or f'/{pattern}' in path:
                return False
        
        # Deve avere almeno 2 segmenti nel path (es: /nome-prodotto/)
        # Le categorie spesso hanno solo 1 segmento o finiscono con pattern specifici
        path_segments = [s for s in path.split('/') if s]
        if len(path_segments) < 1:
            return False
        
        # Pattern che indicano categorie (non prodotti)
        category_indicators = [
            'profumi', 'eau-de-parfum', 'eau-de-toilette', 
            'colonia', 'unisex', 'niche', 'tester', 'outlet'
        ]
        
        # Se il primo segmento è un indicatore di categoria, probabilmente è una categoria
        if path_segments[0] in category_indicators and len(path_segments) <= 2:
            return False
        
        return True
    except Exception as e:
        logger.error(f"Errore nella validazione URL: {e}")
        return False


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per il comando /start"""
    welcome_message = """
🎯 <b>Monitor Prezzi Profumi - Bot</b>

Benvenuto! Questo bot ti permette di aggiungere prodotti da monitorare inviando semplicemente il link del prodotto.

<b>Come usare:</b>
1. Copia il link di un prodotto da casadelprofumo.it
2. Invia il link qui
3. Il prodotto verrà aggiunto al monitoraggio automatico

<b>Comandi disponibili:</b>
/start - Mostra questo messaggio
/help - Mostra la guida completa
/list - Lista i prodotti monitorati (prossimamente)

<b>Esempio:</b>
Invia un link come:
https://www.casadelprofumo.it/nome-prodotto/

Il bot controllerà immediatamente il prezzo e inizierà a monitorarlo! 🚀
    """
    await update.message.reply_text(welcome_message, parse_mode='HTML')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per il comando /help"""
    help_message = """
📖 <b>Guida all'uso del Bot</b>

<b>Funzionalità principali:</b>
• Aggiungi prodotti inviando il link
• Monitoraggio automatico dei prezzi
• Notifiche quando ci sono cali di prezzo o offerte

<b>Come aggiungere un prodotto:</b>
1. Vai su casadelprofumo.it
2. Trova il prodotto che vuoi monitorare
3. Copia l'URL della pagina prodotto
4. Invia il link qui

<b>Esempi di link validi:</b>
• https://www.casadelprofumo.it/nome-prodotto-edp-100ml/
• https://www.casadelprofumo.it/profumo-marca-modello/

<b>Link NON validi:</b>
• Link a categorie (/profumi-da-uomo/)
• Link alla homepage
• Link ad altri siti

<b>Dopo l'aggiunta:</b>
Il prodotto verrà controllato immediatamente e poi monitorato automaticamente nei cicli successivi. Riceverai notifiche quando:
• Il prezzo scende significativamente
• Viene rilevata un'ottima offerta
• Il prodotto raggiunge un nuovo prezzo minimo

Per iniziare, invia semplicemente un link! 🎯
    """
    await update.message.reply_text(help_message, parse_mode='HTML')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per messaggi di testo con link"""
    message_text = update.message.text
    
    # Estrai URL dal messaggio
    url = extract_url_from_text(message_text)
    
    if not url:
        await update.message.reply_text(
            "❌ Nessun link trovato nel messaggio.\n\n"
            "Invia un link di un prodotto da casadelprofumo.it per aggiungerlo al monitoraggio."
        )
        return
    
    # Valida URL
    if not is_valid_product_url(url):
        await update.message.reply_text(
            "❌ Link non valido.\n\n"
            "Il link deve essere di un prodotto da casadelprofumo.it\n"
            "Non sono supportati link a categorie o pagine generiche.\n\n"
            "Esempio valido: https://www.casadelprofumo.it/nome-prodotto/"
        )
        return
    
    # Invia messaggio di attesa
    status_message = await update.message.reply_text(
        "⏳ Sto processando il prodotto...\n"
        "Scraping dati e aggiunta al database..."
    )
    
    db = None
    try:
        # Inizializza componenti
        db = database.Database()
        scraper_instance = scraper.CasaDelProfumoScraper()
        analyzer = price_analyzer.PriceAnalyzer(db)
        
        # Scrapa il prodotto
        logger.info(f"Scraping prodotto da URL: {url}")
        product_data = scraper_instance.scrape_product_page(url)
        
        if not product_data:
            await status_message.edit_text(
                "❌ Errore nello scraping del prodotto.\n\n"
                "Verifica che:\n"
                "• Il link sia corretto\n"
                "• Il prodotto sia ancora disponibile\n"
                "• Il sito sia raggiungibile"
            )
            return
        
        if not product_data.get('price'):
            await status_message.edit_text(
                "❌ Impossibile ottenere il prezzo del prodotto.\n\n"
                "Il prodotto potrebbe non essere più disponibile o il link potrebbe essere errato."
            )
            return
        
        # Verifica se il prodotto esiste già
        existing_product = db.get_product(product_data['product_id'])
        
        # Salva/aggiorna nel database
        product = db.get_or_create_product(
            product_id=product_data['product_id'],
            name=product_data['name'],
            url=product_data['url'],
            price=product_data['price'],
            brand=product_data.get('brand')
        )
        
        # Analizza il prodotto
        alerts = analyzer.analyze_product(product)
        
        # Prepara messaggio di conferma
        if existing_product:
            confirmation_message = (
                f"✅ <b>Prodotto già monitorato - Aggiornato!</b>\n\n"
                f"📦 <b>{product.name}</b>\n"
            )
        else:
            confirmation_message = (
                f"✅ <b>Prodotto aggiunto con successo!</b>\n\n"
                f"📦 <b>{product.name}</b>\n"
            )
        
        if product.brand:
            confirmation_message += f"🏷️ Brand: {product.brand}\n"
        
        confirmation_message += (
            f"💰 Prezzo attuale: <b>€{product.current_price:.2f}</b>\n"
            f"🔗 <a href='{product.url}'>Vedi prodotto</a>\n\n"
        )
        
        if product.lowest_price and product.highest_price:
            confirmation_message += (
                f"📊 Prezzo più basso: €{product.lowest_price:.2f}\n"
                f"📊 Prezzo più alto: €{product.highest_price:.2f}\n\n"
            )
        
        if alerts:
            confirmation_message += f"🔔 Generati {len(alerts)} alert!\n"
        
        confirmation_message += (
            "\n✅ Il prodotto verrà monitorato automaticamente nei cicli successivi.\n"
            "Riceverai notifiche quando ci sono variazioni di prezzo interessanti!"
        )
        
        await status_message.edit_text(confirmation_message, parse_mode='HTML', disable_web_page_preview=True)
        
        logger.info(f"Prodotto aggiunto/aggiornato: {product.name} (€{product.current_price:.2f})")
        
    except Exception as e:
        logger.error(f"Errore nell'aggiunta prodotto: {e}", exc_info=True)
        await status_message.edit_text(
            "❌ Errore durante l'elaborazione del prodotto.\n\n"
            f"Errore: {str(e)}\n\n"
            "Riprova più tardi o contatta il supporto."
        )
    finally:
        # Garantisce sempre la chiusura del database
        if db:
            db.close()


def main():
    """Avvia il bot Telegram"""
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN non configurato nel file .env")
        print("❌ Errore: TELEGRAM_BOT_TOKEN non trovato!")
        print("Aggiungi TELEGRAM_BOT_TOKEN nel file .env")
        return
    
    logger.info("Avvio bot Telegram...")
    
    # Crea applicazione
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Aggiungi handler per comandi
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Aggiungi handler per messaggi di testo (che potrebbero contenere link)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot Telegram avviato e in ascolto...")
    print("✅ Bot Telegram avviato!")
    print("Invia /start al bot per iniziare")
    
    # Avvia il bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
