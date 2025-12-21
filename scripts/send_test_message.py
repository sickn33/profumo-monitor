"""
Script per inviare un messaggio di test più visibile
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import config
from telegram import Bot

async def send_visible_test():
    """Invia un messaggio di test molto visibile"""
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    
    message = """
🔔 <b>TEST NOTIFICHE - MONITOR PREZZI PROFUMI</b>

✅ Il sistema di notifiche funziona correttamente!

📊 <b>Il bot è pronto per monitorare:</b>
• Cali di prezzo significativi
• Errori di prezzo
• Ottime offerte
• Nuovi prezzi minimi

🚀 <b>Prossimi passi:</b>
1. Esegui: <code>python3 main.py</code> per un controllo singolo
2. Oppure: <code>python3 scheduler.py</code> per monitoraggio continuo

💡 Riceverai notifiche automatiche quando vengono rilevate offerte interessanti!
    """
    
    try:
        await bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='HTML'
        )
        print("✅ Messaggio di test inviato!")
        print("Controlla la conversazione con @casadelprofumoBOT su Telegram")
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    asyncio.run(send_visible_test())
