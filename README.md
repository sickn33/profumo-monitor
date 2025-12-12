# 🎯 Monitor Prezzi Profumi - Casa del Profumo

Tool automatico per monitorare i prezzi dei profumi su [casadelprofumo.it](https://www.casadelprofumo.it) e ricevere notifiche su:
- 🔥 Cali di prezzo significativi
- ⚠️ Possibili errori di prezzo
- ✨ Ottime offerte
- 🎯 Nuovi prezzi minimi

## 📋 Caratteristiche

- **Monitoraggio continuo**: Controlla automaticamente i prezzi a intervalli regolari
- **Database storico**: Traccia tutti i prezzi nel tempo
- **Notifiche intelligenti**: Ricevi alert via Telegram o Email
- **Rilevamento automatico**: Identifica cali di prezzo, errori e offerte

## 🚀 Installazione

### 1. Clona o scarica il progetto

```bash
cd profumo_price_monitor
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 3. Configura le notifiche

Copia il file `.env.example` in `.env`:

```bash
cp .env.example .env
```

Modifica il file `.env` con le tue credenziali:

#### Opzione A: Telegram (Consigliato - più semplice)

1. Crea un bot Telegram:
   - Apri Telegram e cerca `@BotFather`
   - Invia `/newbot` e segui le istruzioni
   - Copia il token ricevuto

2. Ottieni il tuo Chat ID:
   - Cerca il bot `@userinfobot` su Telegram
   - Invia `/start` e copia il tuo ID

3. Aggiungi nel file `.env`:
   ```
   TELEGRAM_BOT_TOKEN=il_tuo_token_qui
   TELEGRAM_CHAT_ID=il_tuo_chat_id_qui
   ```

#### Opzione B: Email

1. Per Gmail, crea una "App Password":
   - Vai su [Google Account](https://myaccount.google.com/)
   - Sicurezza → Verifica in due passaggi (deve essere attiva)
   - App passwords → Genera password per "Mail"

2. Aggiungi nel file `.env`:
   ```
   EMAIL_ENABLED=True
   EMAIL_USER=tua_email@gmail.com
   EMAIL_PASSWORD=la_tua_app_password
   EMAIL_TO=destinatario@example.com
   ```

## 🎮 Utilizzo

### Esecuzione singola

Per eseguire un controllo immediato:

```bash
python main.py
```

### Monitoraggio continuo

Per avviare il monitoraggio automatico che controlla ogni 6 ore (configurabile):

```bash
python scheduler.py
```

Lo scheduler continuerà a funzionare fino a quando non lo interrompi con `Ctrl+C`.

### Configurazione frequenza

Modifica nel file `.env`:
```
CHECK_INTERVAL_HOURS=6  # Cambia con il numero di ore desiderato
```

## ⚙️ Configurazione Avanzata

### Soglie per le notifiche

Nel file `.env` puoi modificare:

- `PRICE_DROP_THRESHOLD=0.15`: Notifica se il prezzo scende del 15% o più
- `COMPETITOR_PRICE_DIFF=0.20`: Differenza percentuale per confronto concorrenza
- `MIN_PRICE_FOR_MONITORING=10.0`: Prezzo minimo per monitorare un prodotto

### Delay tra richieste

Per essere rispettosi con il server:

```
REQUEST_DELAY=2.0  # Secondi di attesa tra una richiesta e l'altra
```

## 📊 Database

Il tool crea automaticamente un database SQLite (`profumi_prices.db`) che contiene:

- **products**: Informazioni sui prodotti e prezzi attuali
- **price_history**: Storico completo di tutti i prezzi
- **alerts**: Tutti gli alert generati

Puoi esplorare il database con qualsiasi tool SQLite.

## 🔍 Tipi di Alert

Il sistema genera diversi tipi di notifiche:

1. **price_drop**: Calo di prezzo significativo (≥15% di default)
2. **error**: Possibile errore di prezzo (prezzo anormalmente basso)
3. **great_deal**: Ottima offerta rispetto alla media storica
4. **new_low**: Nuovo prezzo minimo storico

## 🛠️ Troubleshooting

### Il bot Telegram non funziona

- Verifica che il token e il chat ID siano corretti
- Assicurati di aver avviato una conversazione con il bot

### Lo scraper non trova prodotti

- Il sito potrebbe aver cambiato struttura HTML
- Controlla i log per errori specifici
- Potrebbe essere necessario aggiornare i selettori CSS in `scraper.py`

### Troppe notifiche

- Aumenta le soglie in `.env` (es. `PRICE_DROP_THRESHOLD=0.25` per 25%)
- Aumenta `MIN_PRICE_FOR_MONITORING` per ignorare prodotti economici

## 📝 Note Legali

Questo tool è per uso personale. Rispetta i termini di servizio del sito web e non sovraccaricare i server con troppe richieste.

## 🔄 Aggiornamenti Futuri

Possibili miglioramenti:
- Confronto prezzi con altri siti (concorrenza)
- Dashboard web per visualizzare i dati
- Filtri per brand o categorie specifiche
- Export dati in CSV/Excel

## 📧 Supporto

Per problemi o suggerimenti, controlla i log del tool o modifica il codice secondo le tue esigenze.

---

**Buona caccia alle offerte! 🎁**
