"""
Scheduler per eseguire il monitoraggio periodicamente
"""
import logging
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import config
import main

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def start_telegram_bot():
    """Avvia il bot Telegram in un thread separato"""
    try:
        from telegram.ext import Application
        import telegram_bot
        
        if not config.TELEGRAM_BOT_TOKEN:
            logger.warning("TELEGRAM_BOT_TOKEN non configurato - Bot Telegram disabilitato")
            return
        
        logger.info("Avvio bot Telegram...")
        
        # Crea applicazione bot
        application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Aggiungi handler (stessi handler di telegram_bot.py)
        from telegram import Update
        from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
        
        application.add_handler(CommandHandler("start", telegram_bot.start_command))
        application.add_handler(CommandHandler("help", telegram_bot.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_bot.handle_message))
        
        logger.info("Bot Telegram avviato e in ascolto...")
        
        # Avvia il bot (questo è blocking, quindi va in thread separato)
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except ImportError:
        logger.warning("python-telegram-bot non disponibile - Bot Telegram disabilitato")
    except Exception as e:
        logger.error(f"Errore nell'avvio bot Telegram: {e}", exc_info=True)


def start_scheduler():
    """Avvia lo scheduler per il monitoraggio continuo"""
    # Avvia bot Telegram in thread separato (se configurato)
    if config.TELEGRAM_BOT_TOKEN:
        bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
        bot_thread.start()
        logger.info("Bot Telegram avviato in thread separato")
    
    scheduler = BlockingScheduler()
    
    # Usa minuti se configurato, altrimenti ore
    if hasattr(config, 'CHECK_INTERVAL_MINUTES') and config.CHECK_INTERVAL_MINUTES < 60:
        interval_minutes = config.CHECK_INTERVAL_MINUTES
        trigger = IntervalTrigger(minutes=interval_minutes)
        interval_display = f"{interval_minutes} minuti"
    else:
        interval_hours = config.CHECK_INTERVAL_HOURS
        trigger = IntervalTrigger(hours=interval_hours)
        interval_display = f"{interval_hours} ore"
    
    # Esegui un controllo immediato all'avvio
    logger.info("Eseguendo controllo iniziale immediato...")
    try:
        main.run_monitoring_cycle()
    except Exception as e:
        logger.error(f"Errore nel controllo iniziale: {e}", exc_info=True)
    
    # Aggiungi job per eseguire il monitoraggio periodicamente
    scheduler.add_job(
        main.run_monitoring_cycle,
        trigger=trigger,
        id='price_monitoring',
        name='Monitoraggio Prezzi Profumi',
        replace_existing=True
    )
    
    logger.info(f"Scheduler avviato - Controllo ogni {interval_display}")
    logger.info("Premi Ctrl+C per fermare")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler fermato")
        scheduler.shutdown()


if __name__ == "__main__":
    start_scheduler()
