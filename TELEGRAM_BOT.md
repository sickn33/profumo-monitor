# Bot Telegram - Aggiunta Prodotti

## Descrizione

Il bot Telegram permette di aggiungere prodotti da monitorare inviando semplicemente il link del prodotto. Il prodotto viene scrapato immediatamente e aggiunto al database per il monitoraggio automatico.

## Avvio del Bot

```bash
python telegram_bot.py
```

Il bot rimarrà in ascolto continuamente e risponderà ai messaggi ricevuti.

## Utilizzo

### Comandi disponibili

- `/start` - Mostra il messaggio di benvenuto con le istruzioni
- `/help` - Mostra la guida completa all'uso

### Aggiungere un prodotto

1. Copia il link di un prodotto da [casadelprofumo.it](https://www.casadelprofumo.it)
2. Invia il link direttamente al bot (puoi anche includere testo prima o dopo il link)
3. Il bot:
   - Scrapa immediatamente il prodotto
   - Estrae nome, prezzo e brand
   - Aggiunge il prodotto al database
   - Analizza il prezzo per eventuali offerte
   - Invia un messaggio di conferma con i dettagli

### Esempi di link validi

- `https://www.casadelprofumo.it/nome-prodotto-edp-100ml/`
- `https://www.casadelprofumo.it/profumo-marca-modello/`

### Link NON validi

- Link a categorie: `/profumi-da-uomo/`, `/profumi-unisex/`
- Link alla homepage
- Link ad altri siti (non casadelprofumo.it)

## Funzionalità

### Controllo immediato

Quando aggiungi un prodotto:
- Viene scrapato immediatamente
- Il prezzo viene salvato nel database
- Viene analizzato per rilevare offerte o cali di prezzo
- Ricevi una conferma con tutti i dettagli

### Monitoraggio automatico

Dopo l'aggiunta, il prodotto viene monitorato automaticamente nei cicli successivi eseguiti da `main.py` o `scheduler.py`. Riceverai notifiche quando:
- Il prezzo scende significativamente
- Viene rilevata un'ottima offerta
- Il prodotto raggiunge un nuovo prezzo minimo
- Viene rilevato un possibile errore di prezzo

### Gestione prodotti esistenti

Se invii un link di un prodotto già monitorato:
- Il prodotto viene aggiornato con il prezzo attuale
- Ricevi una notifica che il prodotto era già monitorato
- Il monitoraggio continua normalmente

## Configurazione

Il bot usa le stesse variabili di configurazione del sistema di notifiche:

- `TELEGRAM_BOT_TOKEN` - Token del bot Telegram (obbligatorio)
- `TELEGRAM_CHAT_ID` - Chat ID per le notifiche (non necessario per il bot interattivo)

## Test

Per testare le funzionalità del bot:

```bash
python test_telegram_bot.py
```

Questo script verifica:
- Connessione al bot
- Estrazione e validazione degli URL

## Note

- Il bot può ricevere messaggi da qualsiasi utente che ha avviato una conversazione
- Per limitare l'accesso, puoi aggiungere un controllo sulla whitelist di chat_id nel codice
- Il bot deve essere in esecuzione per ricevere e processare i messaggi
- Puoi eseguire il bot in parallelo allo scheduler senza problemi

## Risoluzione problemi

### Bot non risponde

1. Verifica che il bot sia in esecuzione: `python telegram_bot.py`
2. Verifica che `TELEGRAM_BOT_TOKEN` sia configurato correttamente nel file `.env`
3. Controlla i log per eventuali errori

### Link non riconosciuto

- Assicurati che il link sia di un prodotto specifico, non di una categoria
- Il link deve essere di `casadelprofumo.it`
- Prova a copiare il link direttamente dalla pagina prodotto

### Errore nello scraping

- Verifica che il prodotto sia ancora disponibile sul sito
- Controlla che il link sia corretto
- Il sito potrebbe essere temporaneamente non raggiungibile
