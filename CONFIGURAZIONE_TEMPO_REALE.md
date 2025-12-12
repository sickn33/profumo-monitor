# ⚡ Configurazione Tempo Reale

## 🎯 Monitoraggio Frequente

Ho modificato il sistema per supportare controlli ogni **minuti** invece di ore!

---

## ⚙️ Opzioni di Frequenza

### Opzione 1: Ogni 5 Minuti (Molto Frequente)
```env
CHECK_INTERVAL_MINUTES=5
```

### Opzione 2: Ogni 15 Minuti (Consigliato)
```env
CHECK_INTERVAL_MINUTES=15
```

### Opzione 3: Ogni 30 Minuti
```env
CHECK_INTERVAL_MINUTES=30
```

### Opzione 4: Ogni 1 Ora
```env
CHECK_INTERVAL_MINUTES=60
```

---

## 🔧 Come Configurare su Railway

### Passo 1: Vai su Railway
1. Apri il progetto su Railway
2. Vai su **"Variables"**

### Passo 2: Modifica/Crea Variabile
1. Cerca `CHECK_INTERVAL_HOURS` (se esiste, eliminala)
2. Clicca **"New Variable"**
3. **Key:** `CHECK_INTERVAL_MINUTES`
4. **Value:** `15` (o il numero di minuti che preferisci)
5. Clicca **"Add"**

### Passo 3: Riavvia Deploy
1. Vai su **"Deployments"**
2. Clicca sui **3 puntini** sull'ultimo deployment
3. Clicca **"Redeploy"**

---

## 📊 Confronto Frequenze

| Frequenza | Controlli/Giorno | Quando Ricevi Notifiche |
|-----------|------------------|-------------------------|
| 5 minuti  | 288 controlli     | Quasi immediato         |
| 15 minuti | 96 controlli      | Entro 15 minuti         |
| 30 minuti | 48 controlli      | Entro 30 minuti         |
| 1 ora     | 24 controlli      | Entro 1 ora             |
| 6 ore     | 4 controlli       | Entro 6 ore             |

---

## ⚠️ Considerazioni

### Frequenze Molto Basse (< 5 minuti)
- ⚠️ Può sovraccaricare il server del sito
- ⚠️ Consuma più risorse su Railway
- ⚠️ Potresti ricevere troppe notifiche

### Frequenze Consigliate
- ✅ **15-30 minuti**: Bilanciato tra velocità e risorse
- ✅ **5 minuti**: Se vuoi monitoraggio molto frequente
- ✅ **1 ora**: Se vuoi un buon compromesso

---

## 🎯 Raccomandazione

Per "tempo reale" consiglio:
- **15 minuti**: Buon compromesso
- **5 minuti**: Se vuoi essere il primo a sapere

---

## 🔄 Come Cambiare Dopo il Deploy

1. Vai su Railway → Variables
2. Modifica `CHECK_INTERVAL_MINUTES`
3. Redeploy (Railway rileva automaticamente le nuove variabili)

**Non serve modificare il codice!**

---

## ✅ Variabili Finali per Railway

Ecco tutte le variabili da configurare:

```
TELEGRAM_BOT_TOKEN = 8037950581:AAFbYsxTE9tkk32z0qKO_30dE5BMgupm0m4
TELEGRAM_CHAT_ID = 152494821
DATABASE_URL = sqlite:///profumi_prices.db
CHECK_INTERVAL_MINUTES = 15
PRICE_DROP_THRESHOLD = 0.15
REQUEST_DELAY = 2.0
EMAIL_ENABLED = False
```

**Nota:** Usa `CHECK_INTERVAL_MINUTES` invece di `CHECK_INTERVAL_HOURS`!

---

**Ora il sistema controllerà ogni 15 minuti (o il valore che imposti)!** ⚡
