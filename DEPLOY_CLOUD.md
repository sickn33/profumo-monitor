# ☁️ Deploy su Cloud Gratuito - Guida Completa

## 🎯 Opzioni Migliori (Gratuite)

### 1. **Railway.app** ⭐ (Consigliato - Più Semplice)
- ✅ Tier gratuito: $5 di crediti/mese
- ✅ Facile da usare
- ✅ Supporta Python
- ✅ Deploy automatico da GitHub

### 2. **Render.com**
- ✅ Tier gratuito disponibile
- ✅ Supporta Python
- ✅ Deploy da GitHub

### 3. **PythonAnywhere**
- ✅ Gratuito per task schedulati
- ✅ Specifico per Python
- ⚠️ Limitato a 1 task schedulato

---

## 🚀 Opzione 1: Railway.app (Consigliato)

### Step 1: Prepara il progetto per il deploy

Crea questi file aggiuntivi:

#### `Procfile` (per Railway)
```
worker: python3 scheduler.py
```

#### `runtime.txt` (specifica versione Python)
```
python-3.11.0
```

#### `railway.json` (configurazione Railway)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python3 scheduler.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Crea repository GitHub

```bash
cd /Users/nicco/Downloads/profumo_price_monitor

# Inizializza git (se non già fatto)
git init

# Crea .gitignore se non esiste
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.db
*.sqlite
*.sqlite3
.env
*.log
.DS_Store
venv/
env/
EOF

# Aggiungi tutti i file
git add .

# Commit
git commit -m "Initial commit - Profumo price monitor"

# Crea repository su GitHub (vai su github.com e crea un nuovo repo)
# Poi esegui:
# git remote add origin https://github.com/TUO_USERNAME/profumo-monitor.git
# git push -u origin main
```

### Step 3: Deploy su Railway

1. **Vai su [railway.app](https://railway.app)**
2. **Registrati** (puoi usare GitHub)
3. **Clicca "New Project"**
4. **Scegli "Deploy from GitHub repo"**
5. **Seleziona il tuo repository**
6. **Railway rileva automaticamente Python**

### Step 4: Configura Variabili d'Ambiente

1. Nel progetto Railway, vai su **"Variables"**
2. Aggiungi tutte le variabili dal tuo `.env`:
   ```
   TELEGRAM_BOT_TOKEN=8037950581:AAFbYsxTE9tkk32z0qKO_30dE5BMgupm0m4
   TELEGRAM_CHAT_ID=152494821
   DATABASE_URL=sqlite:///profumi_prices.db
   CHECK_INTERVAL_HOURS=6
   PRICE_DROP_THRESHOLD=0.15
   REQUEST_DELAY=2.0
   ```

### Step 5: Avvia il Deploy

Railway:
- Installa automaticamente le dipendenze da `requirements.txt`
- Avvia `scheduler.py`
- Il sistema è attivo! 🎉

**Costo:** Gratuito (con $5 crediti/mese, più che sufficienti)

---

## 🌐 Opzione 2: Render.com

### Step 1: Prepara il progetto

Crea `render.yaml`:

```yaml
services:
  - type: worker
    name: profumo-monitor
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python3 scheduler.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: TELEGRAM_CHAT_ID
        sync: false
      - key: DATABASE_URL
        value: sqlite:///profumi_prices.db
      - key: CHECK_INTERVAL_HOURS
        value: 6
      - key: PRICE_DROP_THRESHOLD
        value: 0.15
      - key: REQUEST_DELAY
        value: 2.0
```

### Step 2: Deploy

1. Vai su [render.com](https://render.com)
2. Registrati
3. "New" → "Background Worker"
4. Connetti il repository GitHub
5. Render usa automaticamente `render.yaml`
6. Aggiungi variabili d'ambiente nella dashboard
7. Deploy!

**Nota:** Render può fermare i worker gratuiti dopo 15 minuti di inattività. Per evitarlo, usa un "ping" periodico (vedi sotto).

---

## 🐍 Opzione 3: PythonAnywhere

### Step 1: Crea account

1. Vai su [pythonanywhere.com](https://www.pythonanywhere.com)
2. Crea account gratuito

### Step 2: Upload file

1. Vai su "Files"
2. Carica tutti i file del progetto
3. Crea cartella `profumo_price_monitor`

### Step 3: Installa dipendenze

1. Vai su "Tasks"
2. Crea nuovo task:
   ```bash
   pip3.10 install --user -r /home/TUO_USERNAME/profumo_price_monitor/requirements.txt
   ```

### Step 4: Crea task schedulato

1. Vai su "Tasks" → "Schedule a new task"
2. Imposta:
   - **When:** Every day at 00:00 (o ogni 6 ore)
   - **Command:** 
     ```bash
     cd /home/TUO_USERNAME/profumo_price_monitor && python3.10 main.py
     ```

**Limitazione:** Account gratuito permette 1 task schedulato al giorno. Per monitoraggio ogni 6 ore, usa Railway o Render.

---

## 🔧 Soluzione per Render (Keep-Alive)

Se usi Render e il worker si ferma, aggiungi questo script:

### `keep_alive.py`

```python
"""
Script per mantenere attivo il worker su Render
"""
import requests
import time
import os

def ping():
    """Esegue un ping per mantenere attivo il worker"""
    # Usa un servizio di ping o semplicemente log
    print(f"Keep-alive ping: {time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    while True:
        ping()
        time.sleep(300)  # Ogni 5 minuti
```

Modifica `scheduler.py` per includere keep-alive in background.

---

## 📝 File da Creare per Deploy

Crea questi file nel progetto:

### `Procfile`
```
worker: python3 scheduler.py
```

### `runtime.txt`
```
python-3.11.0
```

### `railway.json` (solo per Railway)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python3 scheduler.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## ✅ Checklist Pre-Deploy

- [ ] Tutti i file del progetto sono pronti
- [ ] `requirements.txt` è aggiornato
- [ ] `.env` NON è nel repository (è in `.gitignore`)
- [ ] Repository GitHub creato e file caricati
- [ ] Variabili d'ambiente note (per inserirle nel cloud)

---

## 🎯 Raccomandazione Finale

**Per semplicità:** Usa **Railway.app**
- ✅ Più facile da configurare
- ✅ Tier gratuito generoso
- ✅ Deploy automatico
- ✅ Funziona 24/7 senza problemi

**Passi rapidi:**
1. Crea repo GitHub
2. Deploy su Railway
3. Aggiungi variabili d'ambiente
4. Fatto! 🎉

---

## 🔍 Monitoraggio

Dopo il deploy, puoi:
- Vedere i log in tempo reale su Railway/Render
- Verificare che le notifiche arrivino su Telegram
- Controllare statistiche nel dashboard

Il sistema funzionerà 24/7 automaticamente! 🚀
