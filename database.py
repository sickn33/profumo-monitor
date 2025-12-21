"""
Gestione database per tracciare i prezzi dei profumi
"""
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()


class Product(Base):
    """Modello per i prodotti"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    url = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)
    previous_price = Column(Float)
    lowest_price = Column(Float)
    highest_price = Column(Float)
    price_drop_percentage = Column(Float)
    is_on_sale = Column(Boolean, default=False)
    last_checked = Column(DateTime, default=datetime.utcnow)
    first_seen = Column(DateTime, default=datetime.utcnow)
    times_checked = Column(Integer, default=1)
    
    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.current_price})>"


class PriceHistory(Base):
    """Storico dei prezzi"""
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<PriceHistory(product_id='{self.product_id}', price={self.price}, timestamp={self.timestamp})>"


class Alert(Base):
    """Alert generati"""
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, nullable=False, index=True)
    alert_type = Column(String, nullable=False)  # 'price_drop', 'error', 'competitor_beat', 'great_deal'
    message = Column(String, nullable=False)
    old_price = Column(Float)
    new_price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    notified = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Alert(type='{self.alert_type}', message='{self.message}')>"


class Database:
    """Classe per gestire il database"""
    
    def __init__(self):
        self.engine = create_engine(config.DATABASE_URL, echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_or_create_product(self, product_id, name, url, price, brand=None):
        """Ottiene o crea un prodotto"""
        product = self.session.query(Product).filter_by(product_id=product_id).first()
        
        if product:
            # Salva i valori storici PRIMA di aggiornarli (per l'analisi)
            old_lowest_price = product.lowest_price
            old_highest_price = product.highest_price
            
            # Aggiorna il prodotto
            product.previous_price = product.current_price
            product.current_price = price
            product.last_checked = datetime.utcnow()
            product.times_checked += 1
            
            # Calcola la variazione di prezzo
            if product.previous_price and product.previous_price > 0:
                drop = ((product.previous_price - price) / product.previous_price) * 100
                product.price_drop_percentage = drop if drop > 0 else 0
                product.is_on_sale = drop > config.PRICE_DROP_THRESHOLD * 100
            
            # Aggiorna prezzo più basso/alto
            if not product.lowest_price or price < product.lowest_price:
                product.lowest_price = price
            if not product.highest_price or price > product.highest_price:
                product.highest_price = price
            
            # Salva i valori vecchi come attributi temporanei per l'analisi
            # (questi non vengono salvati nel DB, sono solo per uso interno)
            product._previous_lowest_price = old_lowest_price
            product._previous_highest_price = old_highest_price
            
            if brand:
                product.brand = brand
        else:
            # Crea nuovo prodotto
            product = Product(
                product_id=product_id,
                name=name,
                brand=brand,
                url=url,
                current_price=price,
                lowest_price=price,
                highest_price=price,
                first_seen=datetime.utcnow()
            )
            # Per prodotti nuovi, non c'è un "vecchio" lowest_price
            product._previous_lowest_price = None
            product._previous_highest_price = None
            self.session.add(product)
        
        # Aggiungi alla cronologia prezzi
        history = PriceHistory(product_id=product_id, price=price)
        self.session.add(history)
        
        self.session.commit()
        return product
    
    def create_alert(self, product_id, alert_type, message, old_price=None, new_price=None):
        """Crea un nuovo alert.
        
        Deduplicazione migliorata: evita di creare più volte lo stesso alert per lo stesso prodotto,
        tipo e nuovo prezzo (più robusto del controllo sul messaggio completo).
        """
        # Deduplicazione migliorata: controlla product_id + alert_type + new_price
        # Questo è più robusto perché il messaggio potrebbe variare leggermente per arrotondamenti
        query = self.session.query(Alert).filter_by(
            product_id=product_id,
            alert_type=alert_type
        )
        
        # Se abbiamo un new_price, deduplica anche su quello (più preciso)
        if new_price is not None:
            # Confronta con tolleranza per float (arrotonda a 2 decimali)
            from sqlalchemy import func
            query = query.filter(
                func.abs(Alert.new_price - new_price) < 0.01  # Tolleranza 1 centesimo
            )
        else:
            # Se non c'è new_price, fallback al controllo del messaggio
            query = query.filter_by(message=message)
        
        existing = query.order_by(Alert.timestamp.desc()).first()
        if existing:
            return None
        
        alert = Alert(
            product_id=product_id,
            alert_type=alert_type,
            message=message,
            old_price=old_price,
            new_price=new_price
        )
        self.session.add(alert)
        self.session.commit()
        return alert
    
    def get_unnotified_alerts(self):
        """Ottiene gli alert non ancora notificati"""
        return self.session.query(Alert).filter_by(notified=False).all()
    
    def mark_alert_notified(self, alert_id):
        """Segna un alert come notificato"""
        alert = self.session.query(Alert).filter_by(id=alert_id).first()
        if alert:
            alert.notified = True
            self.session.commit()
    
    def get_product(self, product_id):
        """Ottiene un prodotto per ID"""
        return self.session.query(Product).filter_by(product_id=product_id).first()
    
    def close(self):
        """Chiude la connessione"""
        self.session.close()
