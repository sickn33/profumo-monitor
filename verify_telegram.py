"""
Script per verificare e ottenere il Chat ID corretto
"""
import asyncio
import config
from telegram import Bot

async def get_chat_info():
    """Ottiene informazioni sul bot e sui chat disponibili"""
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    
    print("=" * 60)
    print("Verifica Configurazione Telegram")
    print("=" * 60)
    
    # Verifica bot
    try:
        bot_info = await bot.get_me()
        print(f"\n✅ Bot connesso:")
        print(f"   Nome: {bot_info.first_name}")
        print(f"   Username: @{bot_info.username}")
        print(f"   ID: {bot_info.id}")
    except Exception as e:
        print(f"\n❌ Errore connessione bot: {e}")
        return
    
    # Prova a inviare un messaggio al chat ID configurato
    chat_id = config.TELEGRAM_CHAT_ID
    print(f"\n📱 Chat ID configurato: {chat_id}")
    print(f"\nInvio messaggio di test...")
    
    try:
        message = await bot.send_message(
            chat_id=chat_id,
            text="🧪 <b>Test di verifica</b>\n\nSe ricevi questo messaggio, la configurazione è corretta! ✅",
            parse_mode='HTML'
        )
        print(f"✅ Messaggio inviato con successo!")
        print(f"   Message ID: {message.message_id}")
        print(f"   Chat ID: {message.chat.id}")
        print(f"   Tipo chat: {message.chat.type}")
        
        if str(message.chat.id) != str(chat_id):
            print(f"\n⚠️ ATTENZIONE: Il Chat ID nel messaggio ({message.chat.id}) è diverso da quello configurato ({chat_id})")
            print(f"   Aggiorna il file .env con: TELEGRAM_CHAT_ID={message.chat.id}")
        
    except Exception as e:
        print(f"❌ Errore nell'invio: {e}")
        print("\n💡 Suggerimenti:")
        print("   1. Assicurati di aver inviato almeno un messaggio al bot")
        print("   2. Verifica che il Chat ID sia corretto")
        print("   3. Prova a ottenere il Chat ID con @userinfobot su Telegram")
    
    # Prova a ottenere gli aggiornamenti recenti
    print(f"\n📬 Ultimi aggiornamenti ricevuti dal bot:")
    try:
        updates = await bot.get_updates(limit=5)
        if updates:
            for update in updates:
                if update.message:
                    print(f"   - Da: {update.message.from_user.first_name} (ID: {update.message.from_user.id})")
                    print(f"     Chat ID: {update.message.chat.id}")
                    print(f"     Testo: {update.message.text[:50]}...")
        else:
            print("   Nessun aggiornamento trovato")
            print("   💡 Invia un messaggio al bot per generare un aggiornamento")
    except Exception as e:
        print(f"   Errore: {e}")

if __name__ == "__main__":
    asyncio.run(get_chat_info())
