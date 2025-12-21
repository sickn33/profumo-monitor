"""
Script per testare le notifiche Telegram
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import notifier

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_telegram():
    """Test invio notifica Telegram"""
    print("=" * 60)
    print("Test Notifiche Telegram")
    print("=" * 60)
    
    notif = notifier.Notifier()
    
    if not notif.telegram_enabled:
        print("❌ Telegram non configurato correttamente!")
        print("Verifica TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID nel file .env")
        return False
    
    print("✅ Telegram configurato")
    print(f"   Bot Token: {notif.telegram_bot.token[:10]}...")
    print(f"   Chat ID: {notif.telegram_chat_id}")
    print("\nInvio messaggio di test...")
    
    test_message = (
        "🧪 <b>Test Notifiche Monitor Prezzi Profumi</b>\n\n"
        "Se ricevi questo messaggio, le notifiche Telegram funzionano correttamente! ✅\n\n"
        "Ora puoi avviare il monitoraggio con:\n"
        "• <code>python3 main.py</code> - per un controllo singolo\n"
        "• <code>python3 scheduler.py</code> - per monitoraggio continuo"
    )
    
    success = notif.send_telegram(test_message)
    
    if success:
        print("✅ Messaggio inviato con successo!")
        print("Controlla Telegram per vedere il messaggio di test.")
        return True
    else:
        print("❌ Errore nell'invio del messaggio")
        print("Verifica:")
        print("1. Il bot token è corretto")
        print("2. Il chat ID è corretto")
        print("3. Hai avviato una conversazione con il bot")
        return False

if __name__ == "__main__":
    test_telegram()
