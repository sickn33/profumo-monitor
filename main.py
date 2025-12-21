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
    
    with database.Database() as db:
        analyzer = price_analyzer.PriceAnalyzer(db)
        notif = notifier.Notifier()
        
        try:
            # #region agent log - DEBUG: Verifica stato DB prima dello scraping (Ipotesi A)
            existing_products_before = db.session.query(database.Product).count()
            products_with_history = db.session.query(database.Product).filter(
                database.Product.times_checked > 1
            ).count()
            logger.info(f"[DEBUG-A] Stato DB PRIMA scraping: {existing_products_before} prodotti esistenti, {products_with_history} con storico (times_checked>1)")
            logger.info(f"[DEBUG-A] DATABASE_URL: {config.DATABASE_URL}")
            # #endregion
            
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
            
            # Statistiche prodotti
            total_in_db = db.session.query(database.Product).count()
            products_on_sale = db.session.query(database.Product).filter(
                database.Product.is_on_sale == True
            ).count()
            
            # #region agent log - DEBUG: Verifica prodotti con storico (Ipotesi B, C)
            products_with_previous = db.session.query(database.Product).filter(
                database.Product.previous_price.isnot(None)
            ).count()
            products_checked_multiple = db.session.query(database.Product).filter(
                database.Product.times_checked > 1
            ).count()
            total_alerts_in_db = db.session.query(database.Alert).count()
            logger.info(f"[DEBUG-BC] DOPO scraping: {products_with_previous} prodotti con previous_price, {products_checked_multiple} con times_checked>1")
            logger.info(f"[DEBUG-BC] Alert totali nel DB: {total_alerts_in_db}")
            # #endregion
            
            logger.info(f"Statistiche DB: {total_in_db} prodotti totali, {products_on_sale} in offerta")
            
            # Invia notifiche per alert non ancora notificati
            unnotified_alerts = db.get_unnotified_alerts()
            logger.info(f"Alert da notificare: {len(unnotified_alerts)}")
            
            notified_count = 0
            for alert in unnotified_alerts:
                logger.debug(f"Invio notifica per alert: {alert.alert_type} - {alert.message[:50]}...")
                success = notif.notify(alert)
                if success:
                    db.mark_alert_notified(alert.id)
                    notified_count += 1
                    logger.info(f"✅ Notifica inviata: {alert.alert_type}")
                else:
                    logger.warning(f"❌ Errore invio notifica per alert {alert.id}")
            
            if notified_count > 0:
                logger.info(f"✅ Inviate {notified_count} notifiche con successo")
            
            # #region agent log - DEBUG: Statistiche finali analisi (Ipotesi B, C)
            logger.info(f"[DEBUG-BC] FINALE: {price_analyzer.PriceAnalyzer._debug_counter}")
            # Reset counter per prossimo ciclo
            price_analyzer.PriceAnalyzer._debug_counter = {'total': 0, 'with_previous': 0, 'price_changed': 0}
            # #endregion
            
            logger.info("Ciclo di monitoraggio completato")
            
        except Exception as e:
            logger.error(f"Errore durante il ciclo di monitoraggio: {e}", exc_info=True)


if __name__ == "__main__":
    # Esegui un ciclo immediato
    run_monitoring_cycle()
