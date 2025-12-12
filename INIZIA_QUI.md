# 🚀 INIZIA QUI - Guida Super Semplice

## ✅ Tutto Pronto! Segui Questi Passi

### 📝 PASSO 1: Apri il Terminale

Premi `Cmd + Spazio` e cerca "Terminale", oppure vai in:
**Applicazioni → Utility → Terminale**

---

### 📝 PASSO 2: Vai nella Cartella del Progetto

Copia e incolla questo comando nel Terminale:

```bash
cd /Users/nicco/Downloads/profumo_price_monitor
```

Premi **Invio**.

---

### 📝 PASSO 3: Prepara Git (3 comandi)

Copia e incolla questi comandi **uno alla volta**, premendo Invio dopo ognuno:

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Profumo price monitor"
```

---

### 📝 PASSO 4: Crea Repository su GitHub

1. **Apri il browser** (Safari, Chrome, ecc.)
2. **Vai su:** https://github.com/new
3. Se non hai account:
   - Clicca "Sign up"
   - Crea account (username, email, password)
   - Verifica email
4. **Repository name:** `profumo-monitor`
5. **IMPORTANTE:** NON selezionare nulla:
   - ❌ NON aggiungere README
   - ❌ NON aggiungere .gitignore  
   - ❌ NON aggiungere license
6. **Clicca "Create repository"**

---

### 📝 PASSO 5: Carica Codice su GitHub

**GitHub ti mostrerà dei comandi. IGNORALI!**

**Invece, nel Terminale, copia e incolla questi comandi:**

**SOSTITUISCI `TUO_USERNAME` con il tuo username GitHub!**

```bash
git remote add origin https://github.com/TUO_USERNAME/profumo-monitor.git
```

```bash
git branch -M main
```

```bash
git push -u origin main
```

**Esempio se il tuo username è `nicco123`:**
```bash
git remote add origin https://github.com/nicco123/profumo-monitor.git
git branch -M main
git push -u origin main
```

**Ti chiederà:**
- **Username:** Il tuo username GitHub
- **Password:** La tua password GitHub (o un token - vedi sotto)

---

### ⚠️ Se Git Chiede Password e Non Funziona

GitHub non accetta più password normali. Devi usare un **Personal Access Token**:

1. **Vai su:** https://github.com/settings/tokens
2. **Clicca "Generate new token (classic)"**
3. **Nome:** `railway-deploy`
4. **Seleziona:** `repo` (tutti i permessi repo)
5. **Clicca "Generate token"**
6. **COPIA IL TOKEN** (lo vedi solo una volta!)
7. **Usa il token come password** quando git chiede la password

---

### 📝 PASSO 6: Deploy su Railway

1. **Vai su:** https://railway.app
2. **Clicca "Start a New Project"**
3. **Scegli "Login with GitHub"**
4. **Autorizza Railway** ad accedere a GitHub
5. **Clicca "New Project"** (in alto a destra)
6. **Scegli "Deploy from GitHub repo"**
7. **Seleziona:** `profumo-monitor`
8. **Railway inizia automaticamente!** ⏳

Aspetta 1-2 minuti che finisca il deploy.

---

### 📝 PASSO 7: Configura Variabili

Nel progetto Railway:

1. **Clicca su "Variables"** (tab in alto)
2. **Clicca "New Variable"** per ognuna di queste:

**Variabile 1:**
- Key: `TELEGRAM_BOT_TOKEN`
- Value: `8037950581:AAFbYsxTE9tkk32z0qKO_30dE5BMgupm0m4`
- Clicca "Add"

**Variabile 2:**
- Key: `TELEGRAM_CHAT_ID`
- Value: `152494821`
- Clicca "Add"

**Variabile 3:**
- Key: `DATABASE_URL`
- Value: `sqlite:///profumi_prices.db`
- Clicca "Add"

**Variabile 4:**
- Key: `CHECK_INTERVAL_HOURS`
- Value: `6`
- Clicca "Add"

**Variabile 5:**
- Key: `PRICE_DROP_THRESHOLD`
- Value: `0.15`
- Clicca "Add"

**Variabile 6:**
- Key: `REQUEST_DELAY`
- Value: `2.0`
- Clicca "Add"

**Variabile 7:**
- Key: `EMAIL_ENABLED`
- Value: `False`
- Clicca "Add"

---

### 📝 PASSO 8: Verifica

1. **Vai su "Deployments"** (tab in alto)
2. **Clicca sull'ultimo deployment**
3. **Vedi i log**

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

## 📱 Quando Riceverai Notifiche?

- **Prima notifica:** Dopo 6 ore dal deploy (se ci sono offerte)
- **Poi:** Ogni 6 ore automaticamente
- **Se non ci sono offerte:** Non riceverai nulla (normale)

---

## ❓ Problemi?

### "git push non funziona"
→ Usa un Personal Access Token (vedi sopra)

### "Railway non trova il repository"
→ Assicurati di aver autorizzato Railway ad accedere a GitHub

### "Deploy fallisce"
→ Controlla i log su Railway → Deployments
→ Verifica che tutte le 7 variabili siano state aggiunte

### "Non arrivano notifiche"
→ Verifica `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` su Railway
→ Controlla i log per errori

---

## 💰 Costo

**TUTTO GRATUITO!**
- GitHub: gratuito
- Railway: $5 crediti/mese (più che sufficienti)

---

**Buona fortuna! 🚀**
