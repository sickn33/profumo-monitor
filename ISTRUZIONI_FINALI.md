# 🎯 ISTRUZIONI FINALI - Tutto da Terminale

## ✅ Comandi Pronti - Copia e Incolla nel Terminale

---

## 📝 PASSO 1: Vai nella Cartella

Apri Terminale e incolla:

```zsh
cd /Users/nicco/Downloads/profumo_price_monitor
```

Premi **Invio**.

---

## 📝 PASSO 2: Verifica Stato Git

Incolla:

```zsh
git status
```

Premi **Invio**.

Se vedi file non committati, esegui:

```zsh
git add .
```

```zsh
git commit -m "Profumo price monitor"
```

---

## 📝 PASSO 3: Collega a GitHub

**PRIMA** devi aver creato il repository su GitHub:
1. Vai su: https://github.com/new
2. Nome: `profumo-monitor`
3. NON selezionare nulla
4. Clicca "Create repository"

**POI** nel Terminale, incolla (sostituisci `sickn33` con il tuo username se diverso):

```zsh
git remote add origin https://github.com/sickn33/profumo-monitor.git
```

Premi **Invio**.

```zsh
git branch -M main
```

Premi **Invio**.

---

## 📝 PASSO 4: Crea Token GitHub

**IMPORTANTE:** GitHub non accetta password normali!

1. Vai su: https://github.com/settings/tokens
2. Clicca "Generate new token (classic)"
3. Note: `railway-deploy`
4. Seleziona: ✅ `repo`
5. Genera e **COPIA IL TOKEN** (lo vedi solo una volta!)

---

## 📝 PASSO 5: Carica Codice

Nel Terminale, incolla:

```zsh
git push -u origin main
```

Premi **Invio**.

Quando chiede:
- **Username:** `sickn33` (o il tuo username)
- **Password:** **INCOLLA IL TOKEN** (non la password!)

⚠️ Non vedrai caratteri mentre incolli (normale). Premi Invio dopo.

**Se funziona, vedrai:**
```
Enumerating objects...
Writing objects...
Branch 'main' set up to track...
```

✅ **Codice caricato!**

---

## 📝 PASSO 6: Deploy su Railway

1. Vai su: https://railway.app
2. Login with GitHub
3. New Project → Deploy from GitHub repo
4. Seleziona: `profumo-monitor`
5. Aspetta che finisca il deploy

---

## 📝 PASSO 7: Configura Variabili su Railway

Nel progetto Railway → Variables → Aggiungi queste 7 variabili:

```
TELEGRAM_BOT_TOKEN = 8037950581:AAFbYsxTE9tkk32z0qKO_30dE5BMgupm0m4
TELEGRAM_CHAT_ID = 152494821
DATABASE_URL = sqlite:///profumi_prices.db
CHECK_INTERVAL_HOURS = 6
PRICE_DROP_THRESHOLD = 0.15
REQUEST_DELAY = 2.0
EMAIL_ENABLED = False
```

---

## 🎉 FATTO!

Il sistema funziona 24/7 automaticamente!

---

## 📋 Riepilogo Comandi Terminale

Copia e incolla questi comandi **uno alla volta**:

```zsh
cd /Users/nicco/Downloads/profumo_price_monitor
```

```zsh
git status
```

(Se ci sono file non committati:)
```zsh
git add .
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

(Username: `sickn33`, Password: **TOKEN**)

---

**Buona fortuna! 🚀**
