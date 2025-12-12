# 🎯 Guida Completa Deploy - Fatta per Te

## 📋 Cosa Devo Fare (Passo-Passo Super Semplice)

### FASE 1: Creare Account GitHub (2 minuti)

1. **Vai su:** https://github.com/signup
2. **Inserisci:**
   - Username (es: `nicco123`)
   - Email
   - Password
3. **Verifica email** (controlla la posta)
4. **Fatto!** ✅

---

### FASE 2: Preparare il Progetto (1 minuto)

**Apri il Terminale sul Mac e incolla questo:**

```bash
cd /Users/nicco/Downloads/profumo_price_monitor
chmod +x setup_github.sh
./setup_github.sh
```

**Lo script fa tutto automaticamente!**

---

### FASE 3: Creare Repository GitHub (2 minuti)

1. **Vai su:** https://github.com/new
2. **Repository name:** `profumo-monitor`
3. **Descrizione (opzionale):** `Monitor prezzi profumi casadelprofumo.it`
4. **IMPORTANTE:** Lascia tutto deselezionato:
   - ❌ NON aggiungere README
   - ❌ NON aggiungere .gitignore
   - ❌ NON aggiungere license
5. **Clicca "Create repository"**

---

### FASE 4: Caricare Codice su GitHub (1 minuto)

**GitHub ti mostrerà dei comandi. IGNORALI!**

**Invece, nel Terminale incolla questi comandi (sostituisci `TUO_USERNAME` con il tuo username GitHub):**

```bash
cd /Users/nicco/Downloads/profumo_price_monitor
git remote add origin https://github.com/TUO_USERNAME/profumo-monitor.git
git branch -M main
git push -u origin main
```

**Esempio se il tuo username è `nicco123`:**
```bash
git remote add origin https://github.com/nicco123/profumo-monitor.git
git branch -M main
git push -u origin main
```

Ti chiederà username e password GitHub. Inseriscili.

**✅ Fatto! Il codice è su GitHub!**

---

### FASE 5: Creare Account Railway (1 minuto)

1. **Vai su:** https://railway.app
2. **Clicca "Start a New Project"**
3. **Scegli "Login with GitHub"**
4. **Autorizza Railway** ad accedere a GitHub
5. **Fatto!** ✅

---

### FASE 6: Deploy su Railway (2 minuti)

1. **Clicca "New Project"** (in alto a destra)
2. **Scegli "Deploy from GitHub repo"**
3. **Seleziona il repository:** `profumo-monitor`
4. **Railway inizia automaticamente il deploy!**

Aspetta 1-2 minuti che finisca.

---

### FASE 7: Configurare Variabili (2 minuti)

1. **Nel progetto Railway, clicca su "Variables"** (tab in alto)
2. **Clicca "New Variable"** per ognuna di queste:

**Variabile 1:**
- **Key:** `TELEGRAM_BOT_TOKEN`
- **Value:** `8037950581:AAFbYsxTE9tkk32z0qKO_30dE5BMgupm0m4`
- Clicca "Add"

**Variabile 2:**
- **Key:** `TELEGRAM_CHAT_ID`
- **Value:** `152494821`
- Clicca "Add"

**Variabile 3:**
- **Key:** `DATABASE_URL`
- **Value:** `sqlite:///profumi_prices.db`
- Clicca "Add"

**Variabile 4:**
- **Key:** `CHECK_INTERVAL_HOURS`
- **Value:** `6`
- Clicca "Add"

**Variabile 5:**
- **Key:** `PRICE_DROP_THRESHOLD`
- **Value:** `0.15`
- Clicca "Add"

**Variabile 6:**
- **Key:** `REQUEST_DELAY`
- **Value:** `2.0`
- Clicca "Add"

**Variabile 7:**
- **Key:** `EMAIL_ENABLED`
- **Value:** `False`
- Clicca "Add"

---

### FASE 8: Verificare che Funzioni (1 minuto)

1. **Vai su "Deployments"** (tab in alto)
2. **Clicca sull'ultimo deployment**
3. **Vedi i log in tempo reale**

Dovresti vedere:
```
INFO - Scheduler avviato - Controllo ogni 6 ore
```

**✅ Se vedi questo, FUNZIONA!**

---

## 🎉 FATTO!

Il sistema ora:
- ✅ Funziona 24/7 su Railway
- ✅ Controlla prezzi ogni 6 ore
- ✅ Ti invia notifiche su Telegram automaticamente

**Non devi fare altro!**

---

## 📱 Verifica Notifiche

Dopo 6 ore dal deploy:
- Dovresti ricevere la prima notifica su Telegram (se ci sono offerte)
- Se non ci sono offerte, non riceverai nulla (normale)

Per testare subito, puoi:
1. Andare su Railway → Deployments
2. Cliccare sui 3 puntini → "Redeploy"
3. Questo forza un controllo immediato

---

## ❓ Problemi?

### "Git push fallisce"
- Verifica username e password GitHub
- Assicurati di aver creato il repository su GitHub prima

### "Railway non trova il repository"
- Assicurati di aver autorizzato Railway ad accedere a GitHub
- Verifica che il repository si chiami esattamente `profumo-monitor`

### "Deploy fallisce"
- Controlla i log su Railway
- Verifica che tutte le 7 variabili siano state aggiunte

### "Non arrivano notifiche"
- Verifica `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` su Railway
- Controlla i log per errori

---

## 💰 Costo

**TUTTO GRATUITO!**
- GitHub: gratuito
- Railway: $5 crediti/mese (più che sufficienti)

---

## 🎯 Riepilogo Tempi

- Account GitHub: 2 min
- Preparazione progetto: 1 min
- Repository GitHub: 2 min
- Upload codice: 1 min
- Account Railway: 1 min
- Deploy: 2 min
- Configurazione: 2 min

**TOTALE: ~11 minuti** ⏱️

**Poi funziona per sempre automaticamente!** 🚀
