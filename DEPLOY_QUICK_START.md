# 🚀 Deploy Rapido su Railway.app (5 Minuti)

## ⚡ Guida Veloce

### 1️⃣ Prepara GitHub (2 minuti)

```bash
cd /Users/nicco/Downloads/profumo_price_monitor

# Inizializza git
git init

# Aggiungi file
git add .

# Commit
git commit -m "Profumo price monitor"

# Crea repository su GitHub.com (nuovo repo)
# Poi esegui:
git remote add origin https://github.com/TUO_USERNAME/profumo-monitor.git
git branch -M main
git push -u origin main
```

### 2️⃣ Deploy su Railway (3 minuti)

1. **Vai su [railway.app](https://railway.app)**
2. **Clicca "Start a New Project"**
3. **Scegli "Deploy from GitHub repo"**
4. **Autorizza Railway ad accedere a GitHub**
5. **Seleziona il repository `profumo-monitor`**
6. **Railway rileva automaticamente Python e avvia il deploy**

### 3️⃣ Configura Variabili (1 minuto)

Nel progetto Railway:

1. Vai su **"Variables"** (tab in alto)
2. Clicca **"New Variable"**
3. Aggiungi queste variabili:

```
TELEGRAM_BOT_TOKEN = 8037950581:AAFbYsxTE9tkk32z0qKO_30dE5BMgupm0m4
TELEGRAM_CHAT_ID = 152494821
DATABASE_URL = sqlite:///profumi_prices.db
CHECK_INTERVAL_HOURS = 6
PRICE_DROP_THRESHOLD = 0.15
REQUEST_DELAY = 2.0
EMAIL_ENABLED = False
```

4. **Salva**

### 4️⃣ Fatto! ✅

Railway:
- ✅ Installa automaticamente le dipendenze
- ✅ Avvia `scheduler.py`
- ✅ Il sistema è attivo 24/7!

**Vedi i log:** Clicca su "Deployments" → Vedi log in tempo reale

---

## 📱 Verifica

Dopo qualche minuto:
- Controlla i log su Railway (dovresti vedere "Scheduler avviato")
- Dopo 6 ore, dovresti ricevere la prima notifica su Telegram (se ci sono offerte)

---

## 💰 Costo

**Gratuito!** Railway dà $5 di crediti al mese.
- Il nostro script usa pochissime risorse
- $5 sono più che sufficienti per un mese intero
- Se finisci i crediti, Railway ti avvisa (ma è difficile)

---

## 🔧 Troubleshooting

**Il deploy fallisce?**
- Controlla i log su Railway
- Verifica che tutte le variabili d'ambiente siano impostate

**Non arrivano notifiche?**
- Verifica che `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` siano corretti
- Controlla i log per errori

**Vuoi fermare il monitoraggio?**
- Su Railway: Settings → Delete Project

---

## 🎉 Risultato

Il sistema ora funziona **24/7 automaticamente** su Railway!
- ✅ Controlla prezzi ogni 6 ore
- ✅ Ti invia notifiche su Telegram
- ✅ Non devi fare nulla!

**Buon monitoraggio! 🎁**
