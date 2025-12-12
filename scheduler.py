"""
Scheduler per eseguire il monitoraggio periodicamente
"""
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import config
import main

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def start_scheduler():
    """Avvia lo scheduler per il monitoraggio continuo"""
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
