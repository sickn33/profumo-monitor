#!/bin/zsh
# Script compatibile con zsh e bash

echo "=========================================="
echo "🚀 Setup Automatico per GitHub"
echo "=========================================="
echo ""

# Controlla se git è installato
if ! command -v git > /dev/null 2>&1; then
    echo "❌ Git non è installato. Installalo da: https://git-scm.com/"
    exit 1
fi

echo "✅ Git trovato"
echo ""

# Vai nella directory del progetto
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Controlla se già è un repository git
if [ -d ".git" ]; then
    echo "⚠️  Repository git già esistente"
    echo "Continuo comunque..."
else
    echo "📦 Inizializzo repository git..."
    git init
fi

echo ""
echo "📝 Aggiungo tutti i file..."
git add .

echo ""
echo "💾 Creo commit..."
git commit -m "Profumo price monitor - initial commit"

echo ""
echo "✅ Repository git preparato!"
echo ""
echo "=========================================="
echo "📋 PROSSIMI PASSI:"
echo "=========================================="
echo ""
echo "1. Vai su https://github.com/new"
echo "2. Crea un nuovo repository chiamato: profumo-monitor"
echo "3. NON inizializzare con README, .gitignore o license"
echo "4. Copia e incolla questi comandi nel terminale:"
echo ""
echo "git remote add origin https://github.com/TUO_USERNAME/profumo-monitor.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "   (Sostituisci TUO_USERNAME con il tuo username GitHub)"
echo ""
echo "=========================================="
