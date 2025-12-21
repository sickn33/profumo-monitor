# Scripts Directory

Questa cartella contiene script di utility, test manuali e strumenti di debug.

## Script disponibili

### Test e Verifica
- `quick_test.py` - Test rapido su una pagina prodotto
- `test_scraper.py` - Test base dello scraper
- `test_improved_scraper.py` - Test dello scraper migliorato
- `test_scraping_completo.py` - Test completo dello scraping
- `test_notifications.py` - Test delle notifiche Telegram
- `test_telegram_bot.py` - Test del bot Telegram

### Telegram
- `verify_telegram.py` - Verifica configurazione Telegram
- `send_test_message.py` - Invia messaggio di test

### Utility
- `run_immediate.py` - Esegue un controllo immediato
- `view_alerts.py` - Visualizza alert e statistiche

### Analisi
- `analyze_structure.py` - Analizza struttura del sito
- `debug_site.py` - Debug del sito target
- `analizza_copertura.py` - Analizza copertura scraping
- `ottimizza_scraping.py` - Helper per ottimizzazione

## Utilizzo

Esegui gli script dalla directory root del progetto:

```bash
python scripts/quick_test.py
python scripts/view_alerts.py stats
```
