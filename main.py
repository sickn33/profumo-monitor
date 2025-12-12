"""
Script principale per il monitoraggio prezzi profumi
"""
import logging
import time
from datetime import datetime
import config
import database
import scraper
import price_analyzer
import notifier

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_monitoring_cycle():
    """Esegue un ciclo completo di monitoraggio"""
    logger.info("=" * 60)
    logger.info("Inizio ciclo di monitoraggio")
    logger.info("=" * 60)
    
    db = database.Database()
    analyzer = price_analyzer.PriceAnalyzer(db)
    notif = notifier.Notifier()
    
    try:
        # Scrapa i prodotti
        logger.info("Avvio scraping prodotti...")
        scraper_instance = scraper.CasaDelProfumoScraper()
        products = scraper_instance.scrape_all_profumes()
        
        logger.info(f"Trovati {len(products)} prodotti")
        
        if len(products) == 0:
            logger.warning("⚠️ Nessun prodotto trovato! Verifica che lo scraper funzioni correttamente.")
            return
        
        # Processa ogni prodotto
        alerts_generated = 0
        products_processed = 0
        for product_data in products:
            if not product_data or not product_data.get('price'):
                continue
            
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
            alerts_generated += len(alerts)
            products_processed += 1
        
        logger.info(f"Processati {products_processed} prodotti")
        logger.info(f"Generati {alerts_generated} alert")
        
        if products_processed == 0:
            logger.warning("⚠️ Nessun prodotto processato! Verifica che i prodotti abbiano prezzi validi.")
        
        # Invia notifiche per alert non ancora notificati
        unnotified_alerts = db.get_unnotified_alerts()
        logger.info(f"Alert da notificare: {len(unnotified_alerts)}")
        
        for alert in unnotified_alerts:
            success = notif.notify(alert)
            if success:
                db.mark_alert_notified(alert.id)
        
        # Invia riepilogo su Telegram
        try:
            summary = (
                f"📊 <b>Riepilogo Monitoraggio</b>\n\n"
                f"✅ Prodotti trovati: {len(products)}\n"
                f"✅ Prodotti processati: {products_processed}\n"
                f"🔔 Alert generati: {alerts_generated}\n"
                f"📬 Notifiche inviate: {len(unnotified_alerts)}\n\n"
            )
            
            if products_processed > 0:
                # Statistiche prodotti
                products_with_price = [p for p in products if p.get('price')]
                if products_with_price:
                    prices = [p['price'] for p in products_with_price]
                    summary += (
                        f"💰 Prezzo minimo: €{min(prices):.2f}\n"
                        f"💰 Prezzo massimo: €{max(prices):.2f}\n"
                        f"💰 Prezzo medio: €{sum(prices)/len(prices):.2f}\n\n"
                    )
            
            if alerts_generated == 0:
                summary += "ℹ️ Nessun calo di prezzo significativo rilevato.\n"
                summary += "Il prossimo controllo tra 15 minuti."
            else:
                summary += f"🎯 Trovati {alerts_generated} cali di prezzo/offerte!"
            
            # Invia riepilogo
            notif.send_telegram(summary)
            logger.info("Riepilogo inviato su Telegram")
        except Exception as e:
            logger.error(f"Errore nell'invio riepilogo Telegram: {e}")
        
        logger.info("Ciclo di monitoraggio completato")
        
    except Exception as e:
        logger.error(f"Errore durante il ciclo di monitoraggio: {e}", exc_info=True)
    finally:
        db.close()


if __name__ == "__main__":
    # Esegui un ciclo immediato
    run_monitoring_cycle()
