#!/bin/zsh
# Versione semplificata compatibile con zsh

echo "=========================================="
echo "Setup GitHub - Versione Semplice"
echo "=========================================="
echo ""

# Vai nella directory
cd /Users/nicco/Downloads/profumo_price_monitor

# Inizializza git se non esiste
if [ ! -d ".git" ]; then
    echo "Inizializzo git..."
    git init
fi

# Aggiungi tutto
echo "Aggiungo file..."
git add .

# Commit
echo "Creo commit..."
git commit -m "Profumo price monitor"

echo ""
echo "✅ FATTO!"
echo ""
echo "Ora vai su https://github.com/new"
echo "Crea repository: profumo-monitor"
echo "Poi esegui i comandi che ti mostra GitHub"
echo ""
