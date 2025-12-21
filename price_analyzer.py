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
        
        # Se il prezzo è inferiore alla soglia configurata del prezzo più alto mai visto
        error_threshold = getattr(config, 'ERROR_PRICE_THRESHOLD', 0.30)
        if product.highest_price and product.current_price < (product.highest_price * error_threshold):
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
        
        # Usa il vecchio highest_price per il confronto (prima dell'aggiornamento)
        previous_highest = getattr(product, '_previous_highest_price', product.highest_price)
        
        # Se il prezzo è inferiore al 20% del prezzo più alto PRECEDENTE
        if previous_highest and product.current_price < (previous_highest * 0.8):
            # Usa il vecchio lowest_price per il confronto (prima dell'aggiornamento)
            previous_lowest = getattr(product, '_previous_lowest_price', product.lowest_price)
            # E se è vicino al prezzo più basso mai visto PRIMA dell'aggiornamento
            if previous_lowest and product.current_price <= (previous_lowest * 1.1):
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
                    old_price=previous_highest,
                    new_price=product.current_price
                )
                
                logger.info(f"Ottima offerta rilevata per {product.name}")
                return alert
        
        return None
    
    def analyze_new_low_price(self, product):
        """Rileva se è stato raggiunto un nuovo prezzo minimo"""
        if not product.current_price or product.current_price <= 0:
            return None
        
        # Usa il vecchio lowest_price (prima dell'aggiornamento) per il confronto
        # Questo è salvato come attributo temporaneo in get_or_create_product
        previous_lowest = getattr(product, '_previous_lowest_price', product.lowest_price)
        
        # Se il prezzo attuale è inferiore al prezzo più basso PRECEDENTE (prima dell'aggiornamento)
        if previous_lowest and product.current_price < previous_lowest:
            drop_from_low = ((previous_lowest - product.current_price) / previous_lowest) * 100
            
            # Usa la soglia configurabile (default 5%)
            new_low_threshold = getattr(config, 'NEW_LOW_THRESHOLD', 0.05) * 100
            if drop_from_low >= new_low_threshold:
                message = (
                    f"🎯 NUOVO PREZZO MINIMO!\n"
                    f"📦 {product.name}\n"
                    f"💰 Nuovo prezzo: €{product.current_price:.2f}\n"
                    f"💰 Prezzo minimo precedente: €{previous_lowest:.2f}\n"
                    f"📉 Risparmio: {drop_from_low:.1f}%\n"
                    f"🔗 {product.url}"
                )
                
                alert = self.db.create_alert(
                    product_id=product.product_id,
                    alert_type='new_low',
                    message=message,
                    old_price=previous_lowest,
                    new_price=product.current_price
                )
                
                logger.info(f"Nuovo prezzo minimo per {product.name}")
                return alert
        
        return None
    
    # #region agent log - DEBUG counter
    _debug_counter = {'total': 0, 'with_previous': 0, 'price_changed': 0}
    # #endregion
    
    def analyze_product(self, product):
        """Esegue tutte le analisi su un prodotto"""
        alerts = []
        
        # #region agent log - DEBUG: Traccia stato prodotto (Ipotesi B, C)
        PriceAnalyzer._debug_counter['total'] += 1
        has_previous = product.previous_price is not None and product.previous_price > 0
        if has_previous:
            PriceAnalyzer._debug_counter['with_previous'] += 1
            if product.current_price != product.previous_price:
                PriceAnalyzer._debug_counter['price_changed'] += 1
        # Log ogni 50 prodotti per non spammare
        if PriceAnalyzer._debug_counter['total'] % 50 == 0:
            logger.info(f"[DEBUG-BC] Analisi {PriceAnalyzer._debug_counter['total']} prodotti: "
                       f"{PriceAnalyzer._debug_counter['with_previous']} con previous_price, "
                       f"{PriceAnalyzer._debug_counter['price_changed']} con prezzo cambiato")
        # #endregion
        
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
