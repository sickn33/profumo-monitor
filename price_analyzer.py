"""
Analizzatore di prezzi per rilevare offerte, errori e cali di prezzo
"""
import logging
from datetime import datetime, timedelta
import config
import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PriceAnalyzer:
    """Analizza i prezzi e rileva opportunità"""
    
    def __init__(self, db):
        self.db = db

    @staticmethod
    def _price_decreased_since_last_check(product) -> bool:
        """Ritorna True solo se il prezzo è sceso rispetto al check precedente.

        Serve a evitare alert ripetuti ad ogni ciclo quando una condizione resta vera
        (es. "ottima offerta" che rimane tale per ore/giorni).
        """
        try:
            if not product.previous_price or product.previous_price <= 0:
                return False
            if not product.current_price or product.current_price <= 0:
                return False
            # Normalizza a "centesimi" per evitare falsi positivi dovuti a float
            prev = round(float(product.previous_price), 2)
            curr = round(float(product.current_price), 2)
            return curr < prev
        except Exception:
            # In caso di oggetti incompleti/atipici, meglio non generare alert ripetitivi
            return False
    
    def analyze_price_drop(self, product):
        """Analizza se c'è stato un calo di prezzo significativo"""
        if not product.previous_price or product.previous_price <= 0:
            return None
        
        drop_percentage = ((product.previous_price - product.current_price) / product.previous_price) * 100
        
        if drop_percentage >= config.PRICE_DROP_THRESHOLD * 100:
            message = (
                f"🔥 CALO DI PREZZO SIGNIFICATIVO!\n"
                f"📦 {product.name}\n"
                f"💰 Prezzo precedente: €{product.previous_price:.2f}\n"
                f"💰 Prezzo attuale: €{product.current_price:.2f}\n"
                f"📉 Sconto: {drop_percentage:.1f}%\n"
                f"🔗 {product.url}"
            )
            
            alert = self.db.create_alert(
                product_id=product.product_id,
                alert_type='price_drop',
                message=message,
                old_price=product.previous_price,
                new_price=product.current_price
            )
            
            logger.info(f"Rilevato calo di prezzo per {product.name}: {drop_percentage:.1f}%")
            return alert
        
        return None
    
    def analyze_price_error(self, product):
        """Rileva possibili errori di prezzo (prezzi anormalmente bassi)"""
        if not product.current_price or product.current_price <= 0:
            return None

        # Evita spam: l'alert "error" deve scattare quando il prezzo "entra" nella zona anomala,
        # non ad ogni ciclo se resta invariato.
        if not self._price_decreased_since_last_check(product):
            return None
        
        # Se il prezzo è inferiore al 30% del prezzo più alto mai visto
        if product.highest_price and product.current_price < (product.highest_price * 0.3):
            # Verifica che non sia semplicemente un nuovo prodotto
            if product.times_checked > 3:  # Abbiamo già visto questo prodotto diverse volte
                message = (
                    f"⚠️ POSSIBILE ERRORE DI PREZZO!\n"
                    f"📦 {product.name}\n"
                    f"💰 Prezzo attuale: €{product.current_price:.2f}\n"
                    f"💰 Prezzo più alto visto: €{product.highest_price:.2f}\n"
                    f"📊 Differenza: {((product.highest_price - product.current_price) / product.highest_price * 100):.1f}%\n"
                    f"🔗 {product.url}\n"
                    f"⚠️ Verifica se è un errore o un'offerta eccezionale!"
                )
                
                alert = self.db.create_alert(
                    product_id=product.product_id,
                    alert_type='error',
                    message=message,
                    old_price=product.highest_price,
                    new_price=product.current_price
                )
                
                logger.warning(f"Possibile errore di prezzo per {product.name}")
                return alert
        
        return None
    
    def analyze_great_deal(self, product):
        """Rileva se il prezzo è un'ottima offerta rispetto alla media storica"""
        if not product.current_price or product.current_price <= 0:
            return None

        # Evita di notificare continuamente la stessa offerta: manda l'alert solo quando c'è un calo
        # rispetto al check precedente (così se il prezzo resta uguale non spamma).
        if not self._price_decreased_since_last_check(product):
            return None
        
        # Se il prezzo è inferiore al 20% del prezzo più alto
        if product.highest_price and product.current_price < (product.highest_price * 0.8):
            # E se è vicino al prezzo più basso mai visto
            if product.lowest_price and product.current_price <= (product.lowest_price * 1.1):
                message = (
                    f"✨ OTTIMA OFFERTA!\n"
                    f"📦 {product.name}\n"
                    f"💰 Prezzo attuale: €{product.current_price:.2f}\n"
                    f"💰 Prezzo più basso storico: €{product.lowest_price:.2f}\n"
                    f"💰 Prezzo più alto storico: €{product.highest_price:.2f}\n"
                    f"🔗 {product.url}"
                )
                
                alert = self.db.create_alert(
                    product_id=product.product_id,
                    alert_type='great_deal',
                    message=message,
                    old_price=product.highest_price,
                    new_price=product.current_price
                )
                
                logger.info(f"Ottima offerta rilevata per {product.name}")
                return alert
        
        return None
    
    def analyze_new_low_price(self, product):
        """Rileva se è stato raggiunto un nuovo prezzo minimo"""
        if not product.current_price or product.current_price <= 0:
            return None
        
        # Se il prezzo attuale è inferiore al prezzo più basso precedente
        if product.lowest_price and product.current_price < product.lowest_price:
            drop_from_low = ((product.lowest_price - product.current_price) / product.lowest_price) * 100
            
            if drop_from_low >= 5:  # Almeno 5% di sconto rispetto al minimo precedente
                message = (
                    f"🎯 NUOVO PREZZO MINIMO!\n"
                    f"📦 {product.name}\n"
                    f"💰 Nuovo prezzo: €{product.current_price:.2f}\n"
                    f"💰 Prezzo minimo precedente: €{product.lowest_price:.2f}\n"
                    f"📉 Risparmio: {drop_from_low:.1f}%\n"
                    f"🔗 {product.url}"
                )
                
                alert = self.db.create_alert(
                    product_id=product.product_id,
                    alert_type='new_low',
                    message=message,
                    old_price=product.lowest_price,
                    new_price=product.current_price
                )
                
                logger.info(f"Nuovo prezzo minimo per {product.name}")
                return alert
        
        return None
    
    def analyze_product(self, product):
        """Esegue tutte le analisi su un prodotto"""
        alerts = []
        
        # Analizza calo di prezzo
        alert = self.analyze_price_drop(product)
        if alert:
            alerts.append(alert)
        
        # Analizza errore di prezzo
        alert = self.analyze_price_error(product)
        if alert:
            alerts.append(alert)
        
        # Analizza ottima offerta
        alert = self.analyze_great_deal(product)
        if alert:
            alerts.append(alert)
        
        # Analizza nuovo prezzo minimo
        alert = self.analyze_new_low_price(product)
        if alert:
            alerts.append(alert)
        
        return alerts
