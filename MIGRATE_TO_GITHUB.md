# 🚀 Migrazione a GitHub Actions

Questa guida ti aiuta a migrare il monitoraggio dei prezzi da Railway a GitHub Actions (completamente gratuito).

## 1. Prepara i Secrets su GitHub

Vai sul tuo repository GitHub:

1. Clicca su **Settings**
2. Nella barra laterale sinistra, clicca su **Secrets and variables** -> **Actions**
3. Clicca sul pulsante **New repository secret** per ognuna delle seguenti variabili (copia i valori dal tuo file `.env` locale):

| Nome Secret          | Descrizione                              |
| -------------------- | ---------------------------------------- |
| `TELEGRAM_BOT_TOKEN` | Il token del tuo bot Telegram            |
| `TELEGRAM_CHAT_ID`   | Il tuo Chat ID Telegram                  |
| `EMAIL_ENABLED`      | `True` o `False`                         |
| `EMAIL_USER`         | (Opzionale) La tua email Gmail           |
| `EMAIL_PASSWORD`     | (Opzionale) La tua App Password di Gmail |
| `EMAIL_TO`           | (Opzionale) Email destinatario           |

## 2. Pusha il Codice

Ora devi inviare le modifiche al repository:

```bash
git add .
git commit -m "Migrazione a GitHub Actions"
git push
```

## 3. Verifica il Funzionamento

1. Vai sul tab **Actions** del tuo repository GitHub.
2. Vedrai un workflow chiamato "Monitor Prezzi Profumi".
3. Se non parte da solo (è programmato ogni 6 ore), puoi avviarlo manualmente:
   - Clicca su "Monitor Prezzi Profumi" nella lista a sinistra.
   - Clicca sul pulsante **Run workflow** a destra.
4. Attendi che finisca (diventa verde ✅).
5. Controlla che il file `profumi_prices.db` sia stato aggiornato nel repository (vedrai un nuovo commit automatico del bot).

## ⚠️ Nota Importante

Il database (`profumi_prices.db`) viene salvato all'interno della repository Git stessa. Questo significa che la cronologia dei commit conterrà aggiornamenti automatici ogni 6 ore. È una soluzione semplice e gratuita, ma se preferisci non "sporcare" la history, in futuro potrai passare a un database esterno (come Supabase o Neon).
