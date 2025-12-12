# ☁️ Setup su Google Cloud Platform

Guida completa per eseguire il monitoraggio prezzi su Google Cloud in modo permanente.

## 📋 Prerequisiti

1. Account Google Cloud Platform attivo
2. Progetto GCP creato
3. Billing abilitato (per Compute Engine)

---

## 🚀 Passo 1: Crea un'istanza Compute Engine

### 1.1 Vai su Google Cloud Console
- Vai su: https://console.cloud.google.com
- Seleziona il tuo progetto

### 1.2 Crea VM Instance
1. Vai su **Compute Engine** → **VM instances**
2. Clicca **"Create Instance"**
3. Configurazione consigliata:
   - **Name**: `profumo-monitor` (o nome a scelta)
   - **Region**: `europe-west1` (Milano) o `us-central1`
   - **Machine type**: `e2-micro` (gratuito con free tier) o `e2-small`
   - **Boot disk**: 
     - OS: **Ubuntu 22.04 LTS**
     - Size: 10 GB (sufficiente)
   - **Firewall**: 
     - ✅ Allow HTTP traffic
     - ✅ Allow HTTPS traffic
   - **Advanced options** → **Networking**:
     - Network tags: `profumo-monitor`
   - Clicca **"Create"**

### 1.3 Attendi che l'istanza sia pronta
- Status: **Running** (verde)

---

## 🔐 Passo 2: Connettiti all'istanza

### 2.1 Via SSH dal browser
1. Clicca sul nome dell'istanza
2. Clicca **"SSH"** (si apre una finestra nel browser)

### 2.2 Oppure via terminale locale
```bash
# Installa gcloud CLI se non ce l'hai
# macOS:
brew install google-cloud-sdk

# Configura (prima volta)
gcloud init
gcloud auth login

# Connettiti
gcloud compute ssh profumo-monitor --zone=europe-west1-b
```

---

## 📦 Passo 3: Setup ambiente sulla VM

### 3.1 Aggiorna sistema
```bash
sudo apt update
sudo apt upgrade -y
```

### 3.2 Installa Python e dipendenze
```bash
# Installa Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Verifica
python3.11 --version
```

### 3.3 Crea directory progetto
```bash
mkdir -p ~/profumo_monitor
cd ~/profumo_monitor
```

---

## 📤 Passo 4: Carica i file del progetto

### Opzione A: Via SCP (da Mac locale)
```bash
# Dalla tua Mac, nella directory del progetto
cd /Users/nicco/Downloads/profumo_price_monitor

# Carica tutti i file sulla VM
gcloud compute scp --recurse . profumo-monitor:~/profumo_monitor/ --zone=europe-west1-b
```

### Opzione B: Via Git (consigliato)
```bash
# Sulla VM
cd ~/profumo_monitor

# Se hai il progetto su GitHub/GitLab
git clone https://github.com/tuo-username/profumo-monitor.git .

# Oppure crea i file manualmente (vedi sotto)
```

### Opzione C: Crea file manualmente
```bash
# Sulla VM, crea i file uno per uno
nano config.py
# Incolla contenuto...

nano main.py
# Incolla contenuto...

# E così via per tutti i file
```

---

## ⚙️ Passo 5: Configura il progetto

### 5.1 Crea ambiente virtuale
```bash
cd ~/profumo_monitor
python3.11 -m venv venv
source venv/bin/activate
```

### 5.2 Installa dipendenze
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5.3 Configura .env
```bash
nano .env
```

Incolla la configurazione (con i tuoi dati Telegram):
```env
DATABASE_URL=sqlite:///profumi_prices.db

TELEGRAM_BOT_TOKEN=8037950581:AAFbYsxTE9tkk32z0qKO_30dE5BMgupm0m4
TELEGRAM_CHAT_ID=152494821

EMAIL_ENABLED=False

PRICE_DROP_THRESHOLD=0.15
COMPETITOR_PRICE_DIFF=0.20
MIN_PRICE_FOR_MONITORING=10.0

CHECK_INTERVAL_HOURS=6
REQUEST_DELAY=2.0
```

Salva: `Ctrl+X`, poi `Y`, poi `Enter`

### 5.4 Test rapido
```bash
# Test notifiche Telegram
python3 test_notifications.py

# Se funziona, procedi!
```

---

## 🔄 Passo 6: Crea servizio systemd (per esecuzione permanente)

### 6.1 Crea file servizio
```bash
sudo nano /etc/systemd/system/profumo-monitor.service
```

Incolla questo contenuto:
```ini
[Unit]
Description=Monitor Prezzi Profumi - Casa del Profumo
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/profumo_monitor
Environment="PATH=/home/YOUR_USERNAME/profumo_monitor/venv/bin"
ExecStart=/home/YOUR_USERNAME/profumo_monitor/venv/bin/python3 /home/YOUR_USERNAME/profumo_monitor/scheduler.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**IMPORTANTE**: Sostituisci `YOUR_USERNAME` con il tuo username sulla VM!
Per trovarlo: `whoami`

### 6.2 Abilita e avvia servizio
```bash
# Ricarica systemd
sudo systemctl daemon-reload

# Abilita servizio (avvio automatico al boot)
sudo systemctl enable profumo-monitor.service

# Avvia servizio
sudo systemctl start profumo-monitor.service

# Verifica stato
sudo systemctl status profumo-monitor.service
```

### 6.3 Comandi utili
```bash
# Vedi log in tempo reale
sudo journalctl -u profumo-monitor.service -f

# Ferma servizio
sudo systemctl stop profumo-monitor.service

# Riavvia servizio
sudo systemctl restart profumo-monitor.service

# Vedi ultimi log
sudo journalctl -u profumo-monitor.service -n 50
```

---

## ✅ Verifica che funzioni

### Test 1: Controlla che il servizio sia attivo
```bash
sudo systemctl status profumo-monitor.service
```
Dovresti vedere: `Active: active (running)`

### Test 2: Vedi i log
```bash
sudo journalctl -u profumo-monitor.service -f
```
Dovresti vedere i log dello scraping in tempo reale.

### Test 3: Aspetta 6 ore
Dopo 6 ore, dovresti ricevere una notifica su Telegram se ci sono offerte!

---

## 🔧 Troubleshooting

### Il servizio non parte
```bash
# Vedi errori dettagliati
sudo journalctl -u profumo-monitor.service -n 100

# Verifica che il path sia corretto
ls -la /home/YOUR_USERNAME/profumo_monitor/

# Verifica che Python sia nel venv
/home/YOUR_USERNAME/profumo_monitor/venv/bin/python3 --version
```

### Non ricevo notifiche
```bash
# Test manuale notifiche
cd ~/profumo_monitor
source venv/bin/activate
python3 test_notifications.py
```

### Il servizio si ferma
```bash
# Verifica log per errori
sudo journalctl -u profumo-monitor.service --since "1 hour ago"

# Il servizio si riavvia automaticamente grazie a Restart=always
```

---

## 💰 Costi Google Cloud

### Con Free Tier
- **e2-micro**: Gratuito per sempre (con limiti)
- **Storage**: 30 GB gratuiti
- **Network**: 1 GB egress gratuito/mese

### Stima costi (senza free tier)
- **e2-micro**: ~$6-8/mese
- **Storage**: ~$0.17/GB/mese
- **Network**: ~$0.12/GB (oltre il gratuito)

**Totale stimato**: ~$7-10/mese (o gratuito con free tier)

---

## 🎯 Risultato Finale

Una volta completato:
- ✅ Il sistema gira 24/7 su Google Cloud
- ✅ Controlla prezzi ogni 6 ore automaticamente
- ✅ Ti invia notifiche su Telegram
- ✅ Si riavvia automaticamente se si blocca
- ✅ Funziona anche se spegni il Mac
- ✅ Costi minimi o gratuiti

---

## 📝 Comandi Rapidi Riepilogo

```bash
# Connettiti alla VM
gcloud compute ssh profumo-monitor --zone=europe-west1-b

# Vedi stato servizio
sudo systemctl status profumo-monitor.service

# Vedi log
sudo journalctl -u profumo-monitor.service -f

# Riavvia servizio
sudo systemctl restart profumo-monitor.service

# Ferma servizio
sudo systemctl stop profumo-monitor.service
```

---

**🎉 Fatto! Il sistema ora gira permanentemente su Google Cloud!**
