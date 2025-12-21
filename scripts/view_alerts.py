"""
Script per visualizzare gli alert e i prodotti monitorati
"""
import sys
import os

# Aggiungi la directory root al path per importare i moduli
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database
from datetime import datetime, timedelta, timezone


def view_recent_alerts(days=7):
    """Visualizza gli alert degli ultimi N giorni"""
    with database.Database() as db:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        alerts = db.session.query(database.Alert).filter(
            database.Alert.timestamp >= cutoff_date
        ).order_by(database.Alert.timestamp.desc()).all()
        
        print("=" * 80)
        print(f"ALERT DEGLI ULTIMI {days} GIORNI")
        print("=" * 80)
        print(f"Totale: {len(alerts)} alert\n")
        
        for alert in alerts:
            print(f"[{alert.timestamp.strftime('%Y-%m-%d %H:%M')}] {alert.alert_type.upper()}")
            print(f"  {alert.message}")
            if alert.old_price and alert.new_price:
                print(f"  Prezzo: €{alert.old_price:.2f} → €{alert.new_price:.2f}")
            print(f"  Notificato: {'✅' if alert.notified else '❌'}")
            print("-" * 80)


def view_top_deals(limit=10):
    """Visualizza le migliori offerte attuali"""
    with database.Database() as db:
        products = db.session.query(database.Product).filter(
            database.Product.is_on_sale == True,
            database.Product.price_drop_percentage.isnot(None)
        ).order_by(database.Product.price_drop_percentage.desc()).limit(limit).all()
        
        print("=" * 80)
        print(f"TOP {limit} OFFERTE ATTUALI")
        print("=" * 80)
        print()
        
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.name}")
            if product.brand:
                print(f"   Brand: {product.brand}")
            print(f"   Prezzo attuale: €{product.current_price:.2f}")
            if product.previous_price:
                print(f"   Prezzo precedente: €{product.previous_price:.2f}")
            if product.price_drop_percentage:
                print(f"   Sconto: {product.price_drop_percentage:.1f}%")
            print(f"   URL: {product.url}")
            print("-" * 80)


def view_statistics():
    """Visualizza statistiche generali"""
    with database.Database() as db:
        total_products = db.session.query(database.Product).count()
        products_on_sale = db.session.query(database.Product).filter(
            database.Product.is_on_sale == True
        ).count()
        total_alerts = db.session.query(database.Alert).count()
        unnotified_alerts = db.session.query(database.Alert).filter(
            database.Alert.notified == False
        ).count()
        
        print("=" * 80)
        print("STATISTICHE")
        print("=" * 80)
        print(f"Prodotti monitorati: {total_products}")
        print(f"Prodotti in offerta: {products_on_sale}")
        print(f"Totale alert generati: {total_alerts}")
        print(f"Alert non notificati: {unnotified_alerts}")
        print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "alerts":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            view_recent_alerts(days)
        elif command == "deals":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            view_top_deals(limit)
        elif command == "stats":
            view_statistics()
        else:
            print("Uso: python view_alerts.py [alerts|deals|stats] [opzioni]")
    else:
        print("Uso: python view_alerts.py [alerts|deals|stats]")
        print("\nComandi disponibili:")
        print("  alerts [giorni]  - Mostra alert degli ultimi N giorni (default: 7)")
        print("  deals [numero]   - Mostra le migliori N offerte (default: 10)")
        print("  stats            - Mostra statistiche generali")
