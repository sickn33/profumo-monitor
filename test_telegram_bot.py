"""
Script di test per verificare le funzionalità del bot Telegram
"""
import asyncio
import config
from telegram import Bot
from telegram.ext import Application

async def test_bot_connection():
    """Testa la connessione al bot"""
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN non configurato")
        return False
    
    try:
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        bot_info = await bot.get_me()
        print(f"✅ Bot connesso: @{bot_info.username}")
        return True
    except Exception as e:
        print(f"❌ Errore connessione: {e}")
        return False


async def test_url_extraction():
    """Testa l'estrazione di URL dai messaggi"""
    from telegram_bot import extract_url_from_text, is_valid_product_url
    
    test_cases = [
        ("https://www.casadelprofumo.it/prodotto-test/", True),
        ("Ecco il link: https://www.casadelprofumo.it/prodotto-test/", True),
        ("https://www.casadelprofumo.it/profumi-da-uomo/", False),  # Categoria
        ("https://www.google.com", False),  # Altro dominio
        ("Nessun link qui", False),
    ]
    
    print("\n🧪 Test estrazione URL:")
    for text, should_be_valid in test_cases:
        url = extract_url_from_text(text)
        is_valid = is_valid_product_url(url) if url else False
        status = "✅" if is_valid == should_be_valid else "❌"
        print(f"{status} '{text[:50]}...' -> Valid: {is_valid} (expected: {should_be_valid})")


def main():
    """Esegue tutti i test"""
    print("=" * 60)
    print("Test Bot Telegram")
    print("=" * 60)
    
    # Test connessione
    print("\n1. Test connessione bot...")
    asyncio.run(test_bot_connection())
    
    # Test estrazione URL
    print("\n2. Test estrazione URL...")
    asyncio.run(test_url_extraction())
    
    print("\n" + "=" * 60)
    print("Test completati!")
    print("=" * 60)
    print("\nPer avviare il bot:")
    print("  python telegram_bot.py")


if __name__ == "__main__":
    main()
