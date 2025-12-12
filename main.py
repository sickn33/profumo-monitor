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
        
        # Processa ogni prodotto
        alerts_generated = 0
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
        
        logger.info(f"Generati {alerts_generated} alert")
        
        # Invia notifiche per alert non ancora notificati
        unnotified_alerts = db.get_unnotified_alerts()
        logger.info(f"Alert da notificare: {len(unnotified_alerts)}")
        
        for alert in unnotified_alerts:
            success = notif.notify(alert)
            if success:
                db.mark_alert_notified(alert.id)
        
        logger.info("Ciclo di monitoraggio completato")
        
    except Exception as e:
        logger.error(f"Errore durante il ciclo di monitoraggio: {e}", exc_info=True)
    finally:
        db.close()


if __name__ == "__main__":
    # Esegui un ciclo immediato
    run_monitoring_cycle()
