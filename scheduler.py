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
    
    # Aggiungi job per eseguire il monitoraggio periodicamente
    scheduler.add_job(
        main.run_monitoring_cycle,
        trigger=IntervalTrigger(hours=config.CHECK_INTERVAL_HOURS),
        id='price_monitoring',
        name='Monitoraggio Prezzi Profumi',
        replace_existing=True
    )
    
    logger.info(f"Scheduler avviato - Controllo ogni {config.CHECK_INTERVAL_HOURS} ore")
    logger.info("Premi Ctrl+C per fermare")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler fermato")
        scheduler.shutdown()


if __name__ == "__main__":
    start_scheduler()
