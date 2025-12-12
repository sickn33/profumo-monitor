# 🚀 Quick Start - Guida Rapida

## Setup in 5 minuti

### 1. Installa le dipendenze

```bash
cd profumo_price_monitor
pip install -r requirements.txt
```

### 2. Configura Telegram (Consigliato)

#### Passo 1: Crea un bot
1. Apri Telegram
2. Cerca `@BotFather`
3. Invia `/newbot`
4. Segui le istruzioni e copia il **token**

#### Passo 2: Ottieni il tuo Chat ID
1. Cerca `@userinfobot` su Telegram
2. Invia `/start`
3. Copia il tuo **ID numerico**

#### Passo 3: Configura
Crea il file `.env`:

```bash
cp .env.example .env
```

Apri `.env` e inserisci:
```
TELEGRAM_BOT_TOKEN=il_tuo_token_qui
TELEGRAM_CHAT_ID=il_tuo_id_qui
```

### 3. Test rapido

Esegui un test per verificare che tutto funzioni:

```bash
python test_scraper.py
```

### 4. Primo monitoraggio

Esegui un controllo manuale:

```bash
python main.py
```

Dovresti ricevere notifiche se ci sono offerte!

### 5. Avvia il monitoraggio continuo

Per monitorare automaticamente ogni 6 ore:

```bash
python scheduler.py
```

Premi `Ctrl+C` per fermare.

## 📊 Visualizza i risultati

### Vedere gli alert recenti
```bash
python view_alerts.py alerts 7  # Ultimi 7 giorni
```

### Vedere le migliori offerte
```bash
python view_alerts.py deals 10  # Top 10 offerte
```

### Statistiche
```bash
python view_alerts.py stats
```

## ⚙️ Personalizzazione

Modifica `.env` per cambiare:
- Frequenza di controllo: `CHECK_INTERVAL_HOURS=6`
- Soglia sconto: `PRICE_DROP_THRESHOLD=0.15` (15%)
- Delay richieste: `REQUEST_DELAY=2.0` (secondi)

## ❓ Problemi comuni

**Bot Telegram non funziona?**
- Verifica token e chat ID
- Assicurati di aver avviato una conversazione con il bot

**Nessun prodotto trovato?**
- Il sito potrebbe aver cambiato struttura
- Controlla i log per errori
- Potrebbe essere necessario aggiornare `scraper.py`

**Troppe notifiche?**
- Aumenta `PRICE_DROP_THRESHOLD` in `.env`
- Aumenta `MIN_PRICE_FOR_MONITORING`

## 🎯 Prossimi passi

1. Lascia `scheduler.py` in esecuzione
2. Ricevi notifiche automatiche
3. Approfitta delle offerte! 🎁
