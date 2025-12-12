# 📖 Come Funziona il Sistema di Monitoraggio Prezzi

## 🎯 Panoramica Generale

Il sistema monitora automaticamente i prezzi dei profumi su **casadelprofumo.it** e ti invia notifiche quando trova:
- 🔥 Cali di prezzo significativi (≥15%)
- ⚠️ Possibili errori di prezzo
- ✨ Ottime offerte
- 🎯 Nuovi prezzi minimi storici

---

## 🔄 Flusso Completo del Sistema

### 1️⃣ **AVVIO** (quando esegui `python3 scheduler.py` o `python3 main.py`)

```
┌─────────────────────────────────────┐
│  Script Avviato                     │
│  (main.py o scheduler.py)           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  1. Carica Configurazione           │
│     - Legge .env                     │
│     - Configura Telegram/Email        │
│     - Imposta soglie (15% sconto)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. Inizializza Database             │
│     - Crea/collega profumi_prices.db│
│     - Crea tabelle se non esistono   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. AVVIA SCRAPING                  │
└──────────────┬──────────────────────┘
```

### 2️⃣ **SCRAPING** (trova tutti i prodotti)

```
┌─────────────────────────────────────┐
│  FASE 1: Scraping Homepage          │
│  ─────────────────────────────────  │
│  1. Visita casadelprofumo.it         │
│  2. Trova link prodotti nella home  │
│  3. Scrapa ogni prodotto trovato    │
│     - Nome                           │
│     - Prezzo                         │
│     - Brand                          │
│     - URL                            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  FASE 2: Scoperta Categorie         │
│  ─────────────────────────────────  │
│  1. Analizza homepage                │
│  2. Trova link a categorie:          │
│     - /eau-de-parfum-da-donna/       │
│     - /eau-de-toilette-da-uomo/      │
│     - /niche-eau-de-parfum/          │
│     - ... (tutte le categorie)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  FASE 3: Scraping Categorie         │
│  ─────────────────────────────────  │
│  Per ogni categoria trovata:          │
│  1. Visita pagina categoria          │
│  2. Trova tutti i link prodotto      │
│  3. Segue paginazione (pagina 2,3..)│
│  4. Scrapa ogni prodotto:            │
│     - Visita pagina prodotto         │
│     - Estrae nome, prezzo, brand     │
│     - Salva nel database             │
└──────────────┬──────────────────────┘
```

### 3️⃣ **SALVATAGGIO NEL DATABASE**

Per ogni prodotto trovato:

```
┌─────────────────────────────────────┐
│  Database: profumi_prices.db         │
│  ─────────────────────────────────  │
│                                      │
│  Tabella: products                   │
│  ┌──────────────────────────────┐   │
│  │ product_id: "clinique-..."   │   │
│  │ name: "Clinique Aromatics..."│   │
│  │ brand: "Clinique"            │   │
│  │ current_price: 46.95         │   │
│  │ previous_price: 52.00        │   │
│  │ lowest_price: 46.95          │   │
│  │ highest_price: 52.00         │   │
│  │ price_drop_percentage: 9.7%  │   │
│  │ is_on_sale: True/False       │   │
│  │ last_checked: 2025-01-15...  │   │
│  └──────────────────────────────┘   │
│                                      │
│  Tabella: price_history              │
│  ┌──────────────────────────────┐   │
│  │ product_id | price | timestamp│   │
│  │ clinique...| 46.95 | 2025-...│   │
│  │ clinique...| 52.00 | 2025-...│   │
│  └──────────────────────────────┘   │
└──────────────┬──────────────────────┘
```

**Cosa succede:**
- Se il prodotto **esiste già**: aggiorna il prezzo e calcola la variazione
- Se il prodotto **è nuovo**: lo crea nel database
- **Salva sempre** nella cronologia prezzi

### 4️⃣ **ANALISI PREZZI** (rileva offerte)

Per ogni prodotto aggiornato:

```
┌─────────────────────────────────────┐
│  PriceAnalyzer.analyze_product()     │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌─────────────┐  ┌─────────────┐
│ Calo Prezzo │  │ Errore      │
│ ≥15%?       │  │ Prezzo?     │
└──────┬──────┘  └──────┬──────┘
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│ Ottima      │  │ Nuovo Prezzo │
│ Offerta?    │  │ Minimo?      │
└──────┬──────┘  └──────┬──────┘
       │                │
       └───────┬────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Se trovato qualcosa:                │
│  → Crea ALERT nel database           │
│  → Tipo: price_drop/error/great_deal │
└──────────────┬──────────────────────┘
```

**Esempi di analisi:**

1. **Calo Prezzo ≥15%**:
   ```
   Prezzo precedente: €52.00
   Prezzo attuale: €44.20
   Calo: 15% → ✅ ALERT!
   ```

2. **Possibile Errore**:
   ```
   Prezzo più alto visto: €100.00
   Prezzo attuale: €25.00
   Differenza: 75% → ⚠️ ALERT!
   ```

3. **Ottima Offerta**:
   ```
   Prezzo attuale: €30.00
   Prezzo più basso storico: €29.50
   Prezzo più alto storico: €50.00
   → ✨ ALERT!
   ```

### 5️⃣ **INVIO NOTIFICHE**

```
┌─────────────────────────────────────┐
│  Trova tutti gli ALERT non notificati│
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Per ogni alert:                     │
│  ─────────────────────────────────  │
│  1. Prepara messaggio:               │
│     "🔥 CALO DI PREZZO!              │
│      📦 Clinique Aromatics...        │
│      💰 Da €52.00 a €44.20           │
│      📉 Sconto: 15%                   │
│      🔗 [link]"                       │
│                                      │
│  2. Invia via Telegram                │
│     (se configurato)                 │
│                                      │
│  3. Invia via Email                  │
│     (se configurato)                 │
│                                      │
│  4. Segna come "notificato"          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  ✅ Notifica ricevuta su Telegram!   │
└─────────────────────────────────────┘
```

---

## ⏰ Monitoraggio Continuo (Scheduler)

Se esegui `python3 scheduler.py`:

```
┌─────────────────────────────────────┐
│  Scheduler Avviato                  │
│  Controllo ogni 6 ore (configurabile)│
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Loop Infinito:                      │
│  ─────────────────────────────────  │
│  1. Attendi 6 ore                    │
│  2. Esegui ciclo completo:           │
│     - Scraping                       │
│     - Analisi                        │
│     - Notifiche                      │
│  3. Ripeti                           │
└─────────────────────────────────────┘
```

**Esempio timeline:**
```
Ore 00:00 → Scraping → 0 alert
Ore 06:00 → Scraping → 2 alert (notifiche inviate!)
Ore 12:00 → Scraping → 0 alert
Ore 18:00 → Scraping → 1 alert (notifica inviata!)
```

---

## 📊 Struttura Database

Il database SQLite (`profumi_prices.db`) contiene:

### Tabella `products`
- Informazioni su ogni prodotto
- Prezzo attuale, precedente, minimo, massimo
- Percentuale di sconto
- Data ultimo controllo

### Tabella `price_history`
- Storico completo di tutti i prezzi
- Ogni volta che un prezzo cambia, viene salvato qui
- Permette di vedere l'andamento nel tempo

### Tabella `alerts`
- Tutti gli alert generati
- Tipo di alert (price_drop, error, great_deal)
- Se è stato notificato o meno
- Messaggio completo

---

## 🎮 Come Usare

### Esecuzione Singola
```bash
python3 main.py
```
- Esegue UN ciclo completo
- Scrapa, analizza, notifica
- Si ferma alla fine

### Monitoraggio Continuo
```bash
python3 scheduler.py
```
- Esegue cicli ogni 6 ore (configurabile)
- Continua fino a Ctrl+C
- Ideale per lasciare in esecuzione

### Visualizzare Risultati
```bash
python3 view_alerts.py stats      # Statistiche
python3 view_alerts.py alerts 7    # Alert ultimi 7 giorni
python3 view_alerts.py deals 10    # Top 10 offerte
```

---

## ⚙️ Configurazione

Tutto è configurabile nel file `.env`:

```env
# Frequenza controllo (ore)
CHECK_INTERVAL_HOURS=6

# Soglia calo prezzo (0.15 = 15%)
PRICE_DROP_THRESHOLD=0.15

# Delay tra richieste (secondi)
REQUEST_DELAY=2.0

# Telegram
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

---

## 🔍 Esempio Pratico

**Scenario:** Il profumo "Clinique Aromatics" costa normalmente €52.00

**Giorno 1 (primo controllo):**
- Sistema trova il prodotto a €52.00
- Salva nel database
- Nessun alert (è il primo controllo)

**Giorno 2 (controllo dopo 6 ore):**
- Sistema trova il prodotto a €44.20
- Calcola: (52.00 - 44.20) / 52.00 = 15% di sconto
- ✅ **ALERT GENERATO!**
- 📱 **Notifica inviata su Telegram:**
  ```
  🔥 CALO DI PREZZO SIGNIFICATIVO!
  📦 Clinique Aromatics Elixir Eau de Parfum
  💰 Prezzo precedente: €52.00
  💰 Prezzo attuale: €44.20
  📉 Sconto: 15.0%
  🔗 https://www.casadelprofumo.it/...
  ```

**Giorno 3:**
- Prezzo torna a €52.00
- Sistema aggiorna, ma nessun alert (è un aumento)

---

## 🎯 In Sintesi

1. **Scrapa** → Trova tutti i prodotti dal sito
2. **Salva** → Memorizza prezzi nel database
3. **Analizza** → Confronta con prezzi precedenti
4. **Rileva** → Trova offerte/cali/errori
5. **Notifica** → Ti avvisa su Telegram/Email
6. **Ripete** → Ogni 6 ore (o quando esegui manualmente)

**Risultato:** Ricevi notifiche automatiche quando ci sono offerte interessanti! 🎁
