#!/bin/bash
# Script di setup automatico per Google Cloud

echo "=========================================="
echo "Setup Monitor Prezzi Profumi - Google Cloud"
echo "=========================================="
echo ""

# Colori per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica che siamo sulla VM
if [ ! -f /etc/os-release ]; then
    echo "❌ Questo script deve essere eseguito sulla VM Google Cloud"
    exit 1
fi

echo -e "${YELLOW}Passo 1: Aggiornamento sistema...${NC}"
sudo apt update
sudo apt upgrade -y

echo -e "${YELLOW}Passo 2: Installazione Python...${NC}"
sudo apt install python3.11 python3.11-venv python3-pip -y

echo -e "${YELLOW}Passo 3: Creazione directory progetto...${NC}"
mkdir -p ~/profumo_monitor
cd ~/profumo_monitor

echo -e "${YELLOW}Passo 4: Creazione ambiente virtuale...${NC}"
python3.11 -m venv venv
source venv/bin/activate

echo -e "${YELLOW}Passo 5: Installazione dipendenze...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✅ Setup completato!${NC}"
echo ""
echo "Prossimi passi:"
echo "1. Configura il file .env con le tue credenziali"
echo "2. Testa con: python3 test_notifications.py"
echo "3. Crea il servizio systemd (vedi GOOGLE_CLOUD_SETUP.md)"
