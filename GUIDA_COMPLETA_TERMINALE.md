# 🚀 Guida Completa - Tutto da Terminale Mac (ZSH)

## ✅ Tutti i Comandi Pronti - Copia e Incolla

---

## 📋 FASE 1: Preparare il Progetto (2 minuti)

### Passo 1.1: Apri Terminale
Premi `Cmd + Spazio`, cerca "Terminale" e aprilo.

### Passo 1.2: Vai nella Cartella del Progetto
Copia e incolla questo comando:

```zsh
cd /Users/nicco/Downloads/profumo_price_monitor
```

Premi **Invio**.

### Passo 1.3: Inizializza Git
Copia e incolla:

```zsh
git init
```

Premi **Invio**.

### Passo 1.4: Aggiungi Tutti i File
Copia e incolla:

```zsh
git add .
```

Premi **Invio**.

### Passo 1.5: Crea il Primo Commit
Copia e incolla:

```zsh
git commit -m "Profumo price monitor"
```

Premi **Invio**.

**✅ Fase 1 completata!**

---

## 📋 FASE 2: Creare Account GitHub (se non ce l'hai)

### Passo 2.1: Apri Browser
Apri Safari, Chrome o Firefox.

### Passo 2.2: Vai su GitHub
Vai su: **https://github.com/signup**

### Passo 2.3: Crea Account
- Inserisci username (es: `sickn33`)
- Inserisci email
- Inserisci password
- Clicca "Sign up"

### Passo 2.4: Verifica Email
- Controlla la posta
- Clicca sul link di verifica

**✅ Account GitHub creato!**

---

## 📋 FASE 3: Creare Repository su GitHub (2 minuti)

### Passo 3.1: Vai su GitHub
Nel browser, vai su: **https://github.com/new**

### Passo 3.2: Crea Repository
- **Repository name:** `profumo-monitor`
- **Description (opzionale):** `Monitor prezzi profumi`
- **IMPORTANTE:** Lascia tutto deselezionato:
  - ❌ NON selezionare "Add a README file"
  - ❌ NON selezionare "Add .gitignore"
  - ❌ NON selezionare "Choose a license"
- **Clicca "Create repository"**

**✅ Repository creato!**

---

## 📋 FASE 4: Creare Token GitHub (3 minuti)

### Passo 4.1: Vai alle Impostazioni Token
Nel browser, vai su: **https://github.com/settings/tokens**

### Passo 4.2: Genera Nuovo Token
- Clicca **"Generate new token"**
- Clicca **"Generate new token (classic)"**

### Passo 4.3: Configura Token
- **Note:** Scrivi `railway-deploy`
- **Expiration:** Scegli `90 days` (o `No expiration`)
- **Scorri in basso** e seleziona:
  - ✅ **`repo`** (tutti i permessi repo)
- **Clicca "Generate token"** (in fondo)

### Passo 4.4: COPIA IL TOKEN
⚠️ **IMPORTANTE:** Il token viene mostrato **UNA SOLA VOLTA**!

- **COPIA SUBITO** il token (è una stringa tipo: `ghp_xxxxxxxxxxxxxxxxxxxx`)
- **Salvalo** da qualche parte (Note, TextEdit, ecc.)
- **Non perderlo!**

**✅ Token creato!**

---

## 📋 FASE 5: Caricare Codice su GitHub (1 minuto)

### Passo 5.1: Collega Repository Locale a GitHub
Torna al Terminale e copia/incolla questi comandi **uno alla volta**:

**SOSTITUISCI `sickn33` con il tuo username GitHub se è diverso:**

```zsh
git remote add origin https://github.com/sickn33/profumo-monitor.git
```

Premi **Invio**.

```zsh
git branch -M main
```

Premi **Invio**.

```zsh
git push -u origin main
```

Premi **Invio**.

### Passo 5.2: Inserisci Credenziali
Quando chiede:
- **Username:** Inserisci il tuo username GitHub (es: `sickn33`)
- **Password:** **INCOLLA IL TOKEN** che hai copiato prima (non la password normale!)

⚠️ **Nota:** Non vedrai caratteri mentre incolli il token (normale, è per sicurezza). Premi **Invio** dopo aver incollato.

### Passo 5.3: Verifica
Se vedi:
```
Enumerating objects: ...
Writing objects: ...
Branch 'main' set up to track...
```

**✅ Codice caricato su GitHub!**

---

## 📋 FASE 6: Creare Account Railway (1 minuto)

### Passo 6.1: Vai su Railway
Nel browser, vai su: **https://railway.app**

### Passo 6.2: Registrati
- Clicca **"Start a New Project"**
- Clicca **"Login with GitHub"**
- Autorizza Railway ad accedere a GitHub
- Completa la registrazione

**✅ Account Railway creato!**

---

## 📋 FASE 7: Deploy su Railway (2 minuti)

### Passo 7.1: Crea Nuovo Progetto
- Clicca **"New Project"** (in alto a destra)
- Scegli **"Deploy from GitHub repo"**

### Passo 7.2: Seleziona Repository
- Seleziona il repository: **`profumo-monitor`**
- Railway inizia automaticamente il deploy

### Passo 7.3: Attendi
Aspetta 1-2 minuti che finisca il deploy.

**✅ Deploy avviato!**

---

## 📋 FASE 8: Configurare Variabili (3 minuti)

### Passo 8.1: Vai su Variables
Nel progetto Railway:
- Clicca su **"Variables"** (tab in alto)

### Passo 8.2: Aggiungi Variabili
Clicca **"New Variable"** per ognuna di queste (copia e incolla i valori):

**Variabile 1:**
- **Key:** `TELEGRAM_BOT_TOKEN`
- **Value:** `8037950581:AAFbYsxTE9tkk32z0qKO_30dE5BMgupm0m4`
- Clicca **"Add"**

**Variabile 2:**
- **Key:** `TELEGRAM_CHAT_ID`
- **Value:** `152494821`
- Clicca **"Add"**

**Variabile 3:**
- **Key:** `DATABASE_URL`
- **Value:** `sqlite:///profumi_prices.db`
- Clicca **"Add"**

**Variabile 4:**
- **Key:** `CHECK_INTERVAL_HOURS`
- **Value:** `6`
- Clicca **"Add"**

**Variabile 5:**
- **Key:** `PRICE_DROP_THRESHOLD`
- **Value:** `0.15`
- Clicca **"Add"**

**Variabile 6:**
- **Key:** `REQUEST_DELAY`
- **Value:** `2.0`
- Clicca **"Add"**

**Variabile 7:**
- **Key:** `EMAIL_ENABLED`
- **Value:** `False`
- Clicca **"Add"**

**✅ Variabili configurate!**

---

## 📋 FASE 9: Verificare che Funzioni (1 minuto)

### Passo 9.1: Vai su Deployments
Nel progetto Railway:
- Clicca su **"Deployments"** (tab in alto)
- Clicca sull'ultimo deployment

### Passo 9.2: Controlla i Log
Dovresti vedere nei log:
```
INFO - Scheduler avviato - Controllo ogni 6 ore
```

**✅ Se vedi questo, FUNZIONA!**

---

## 🎉 FATTO!

Il sistema ora:
- ✅ Funziona 24/7 su Railway
- ✅ Controlla prezzi ogni 6 ore automaticamente
- ✅ Ti invia notifiche su Telegram quando trova offerte

**Non devi fare altro!**

---

## 📱 Quando Riceverai Notifiche?

- **Prima notifica:** Dopo 6 ore dal deploy (se ci sono offerte)
- **Poi:** Ogni 6 ore automaticamente
- **Se non ci sono offerte:** Non riceverai nulla (normale)

---

## ❓ Problemi Comuni

### "git push non funziona"
→ Assicurati di usare il **TOKEN** come password, non la password normale
→ Verifica che il repository esista su GitHub

### "Railway non trova il repository"
→ Assicurati di aver autorizzato Railway ad accedere a GitHub
→ Verifica che il repository si chiami esattamente `profumo-monitor`

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
- Railway: $5 crediti/mese (più che sufficienti per questo script)

---

## 📊 Riepilogo Comandi Terminale

Ecco tutti i comandi in sequenza (copia e incolla uno alla volta):

```zsh
cd /Users/nicco/Downloads/profumo_price_monitor
```

```zsh
git init
```

```zsh
git add .
```

```zsh
git commit -m "Profumo price monitor"
```

```zsh
git remote add origin https://github.com/sickn33/profumo-monitor.git
```

```zsh
git branch -M main
```

```zsh
git push -u origin main
```

(Quando chiede username/password: username = `sickn33`, password = **TOKEN**)

---

**Buona fortuna! 🚀**
