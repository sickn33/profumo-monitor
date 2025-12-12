"""
Sistema di notifiche per alert
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Notifier:
    """Gestisce le notifiche via email e Telegram"""
    
    def __init__(self):
        self.telegram_enabled = bool(config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID)
        self.email_enabled = config.EMAIL_ENABLED
        
        if self.telegram_enabled:
            try:
                from telegram import Bot
                self.telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
                self.telegram_chat_id = config.TELEGRAM_CHAT_ID
            except ImportError:
                logger.warning("python-telegram-bot non installato, Telegram disabilitato")
                self.telegram_enabled = False
    
    def send_telegram(self, message):
        """Invia notifica via Telegram (wrapper sincrono per async)"""
        if not self.telegram_enabled:
            return False
        
        try:
            # Esegue la funzione async in modo sincrono
            asyncio.run(self._send_telegram_async(message))
            logger.info("Notifica Telegram inviata")
            return True
        except Exception as e:
            logger.error(f"Errore nell'invio Telegram: {e}")
            return False
    
    async def _send_telegram_async(self, message):
        """Invia notifica via Telegram (versione async)"""
        await self.telegram_bot.send_message(
            chat_id=self.telegram_chat_id,
            text=message,
            parse_mode='HTML'
        )
    
    def send_email(self, subject, message):
        """Invia notifica via email"""
        if not self.email_enabled:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_USER
            msg['To'] = config.EMAIL_TO
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT)
            server.starttls()
            server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logger.info("Email inviata")
            return True
        except Exception as e:
            logger.error(f"Errore nell'invio email: {e}")
            return False
    
    def notify(self, alert):
        """Invia notifica per un alert"""
        message = alert.message
        
        # Prova Telegram
        if self.telegram_enabled:
            success = self.send_telegram(message)
            if success:
                return True
        
        # Prova Email
        if self.email_enabled:
            subject = f"🚨 Alert Profumi: {alert.alert_type}"
            success = self.send_email(subject, message)
            if success:
                return True
        
        # Se nessun metodo disponibile, stampa
        if not self.telegram_enabled and not self.email_enabled:
            logger.info(f"ALERT: {message}")
            return True
        
        return False
