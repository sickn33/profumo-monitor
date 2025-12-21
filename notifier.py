"""
Sistema di notifiche per alert
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
from typing import List, Optional
import config
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Notifier:
    """Gestisce le notifiche via email e Telegram.
    
    Ottimizzazioni:
    - Event loop persistente per evitare overhead di asyncio.run()
    - Retry automatico su errori transitori
    - Supporto batch per invio multiplo
    """
    
    def __init__(self):
        self.telegram_enabled = bool(config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID)
        self.email_enabled = config.EMAIL_ENABLED
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        
        if self.telegram_enabled:
            try:
                from telegram import Bot
                self.telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
                self.telegram_chat_id = config.TELEGRAM_CHAT_ID
            except ImportError:
                logger.warning("python-telegram-bot non installato, Telegram disabilitato")
                self.telegram_enabled = False
    
    def _get_event_loop(self) -> asyncio.AbstractEventLoop:
        """Ottiene o crea un event loop persistente"""
        if self._loop is None or self._loop.is_closed():
            try:
                # Prova a ottenere un loop esistente
                self._loop = asyncio.get_event_loop()
                if self._loop.is_closed():
                    raise RuntimeError("Loop chiuso")
            except RuntimeError:
                # Crea un nuovo loop se non ne esiste uno
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop
    
    def send_telegram(self, message: str, max_retries: int = 3) -> bool:
        """Invia notifica via Telegram con retry automatico"""
        if not self.telegram_enabled:
            return False
        
        try:
            loop = self._get_event_loop()
            loop.run_until_complete(self._send_telegram_with_retry(message, max_retries))
            logger.info("Notifica Telegram inviata")
            return True
        except Exception as e:
            logger.error(f"Errore nell'invio Telegram dopo {max_retries} tentativi: {e}")
            return False
    
    async def _send_telegram_with_retry(self, message: str, max_retries: int = 3):
        """Invia notifica via Telegram con retry (versione async)"""
        from telegram.error import NetworkError, TimedOut, RetryAfter
        
        last_error = None
        for attempt in range(max_retries):
            try:
                await self.telegram_bot.send_message(
                    chat_id=self.telegram_chat_id,
                    text=message,
                    parse_mode='HTML'
                )
                return  # Successo
            except RetryAfter as e:
                # Telegram ci chiede di aspettare
                wait_time = e.retry_after
                logger.warning(f"Telegram rate limit, attendo {wait_time}s")
                await asyncio.sleep(wait_time)
                last_error = e
            except (NetworkError, TimedOut) as e:
                # Errori di rete, retry con backoff
                wait_time = 2 ** attempt  # Backoff esponenziale: 1, 2, 4 secondi
                logger.warning(f"Errore rete Telegram (tentativo {attempt + 1}/{max_retries}), attendo {wait_time}s")
                await asyncio.sleep(wait_time)
                last_error = e
            except Exception as e:
                # Altri errori, non fare retry
                raise e
        
        # Se arriviamo qui, tutti i retry sono falliti
        raise last_error or Exception("Max retries exceeded")
    
    def send_telegram_batch(self, messages: List[str]) -> int:
        """Invia più messaggi Telegram in batch.
        
        Returns:
            Numero di messaggi inviati con successo
        """
        if not self.telegram_enabled or not messages:
            return 0
        
        try:
            loop = self._get_event_loop()
            return loop.run_until_complete(self._send_telegram_batch_async(messages))
        except Exception as e:
            logger.error(f"Errore nell'invio batch Telegram: {e}")
            return 0
    
    async def _send_telegram_batch_async(self, messages: List[str]) -> int:
        """Invia più messaggi in batch con delay per evitare rate limit"""
        sent = 0
        for message in messages:
            try:
                await self._send_telegram_with_retry(message)
                sent += 1
                # Piccolo delay tra i messaggi per evitare rate limit
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(f"Errore invio messaggio batch: {e}")
        return sent
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((smtplib.SMTPException, ConnectionError, TimeoutError))
    )
    def _send_email_with_retry(self, msg: MIMEMultipart):
        """Invia email con retry automatico"""
        server = smtplib.SMTP(config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT, timeout=30)
        try:
            server.starttls()
            server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            server.send_message(msg)
        finally:
            server.quit()
    
    def send_email(self, subject: str, message: str) -> bool:
        """Invia notifica via email con retry automatico"""
        if not self.email_enabled:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_USER
            msg['To'] = config.EMAIL_TO
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            self._send_email_with_retry(msg)
            logger.info("Email inviata")
            return True
        except Exception as e:
            logger.error(f"Errore nell'invio email: {e}")
            return False
    
    def notify(self, alert) -> bool:
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
    
    def notify_batch(self, alerts: list) -> int:
        """Invia notifiche per una lista di alert.
        
        Returns:
            Numero di notifiche inviate con successo
        """
        if not alerts:
            return 0
        
        messages = [alert.message for alert in alerts]
        
        # Usa batch per Telegram se abilitato
        if self.telegram_enabled:
            return self.send_telegram_batch(messages)
        
        # Fallback: invio singolo
        sent = 0
        for alert in alerts:
            if self.notify(alert):
                sent += 1
        return sent
    
    def close(self):
        """Chiude le risorse (event loop)"""
        if self._loop and not self._loop.is_closed():
            self._loop.close()
            self._loop = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        return False
