# 🔑 Come Creare Token GitHub (5 Minuti)

## ⚠️ Problema
GitHub non accetta più password normali. Devi usare un **Personal Access Token**.

---

## 📝 PASSO 1: Crea il Token

1. **Apri il browser**
2. **Vai su:** https://github.com/settings/tokens
3. **Se non sei loggato:** fai login con il tuo account GitHub
4. **Clicca "Generate new token"** → **"Generate new token (classic)"**

---

## 📝 PASSO 2: Configura il Token

1. **Note:** Scrivi `railway-deploy` (o qualsiasi nome)
2. **Expiration:** Scegli `90 days` (o `No expiration` se vuoi)
3. **Scorri in basso e seleziona:**
   - ✅ **`repo`** (tutti i permessi repo)
     - Questo include automaticamente: repo:status, repo_deployment, public_repo, repo:invite, security_events
4. **Clicca "Generate token"** (in fondo alla pagina)

---

## 📝 PASSO 3: COPIA IL TOKEN

⚠️ **IMPORTANTE:** Il token viene mostrato **UNA SOLA VOLTA**!

1. **COPIA SUBITO IL TOKEN** (è una stringa lunga tipo: `ghp_xxxxxxxxxxxxxxxxxxxx`)
2. **Salvalo da qualche parte** (Note, TextEdit, ecc.)
3. **Non perderlo!** (se lo perdi, devi crearne uno nuovo)

---

## 📝 PASSO 4: Usa il Token

Ora nel Terminale, esegui di nuovo:

```zsh
git push -u origin main
```

Quando ti chiede:
- **Username:** `sickn33` (il tuo username)
- **Password:** **INCOLLA IL TOKEN** (non la password normale!)

**IMPORTANTE:** 
- Non vedrai caratteri mentre incolli il token (normale, è per sicurezza)
- Premi Invio dopo aver incollato

---

## ✅ Dovrebbe Funzionare!

Se tutto va bene, vedrai:
```
Enumerating objects: ...
Writing objects: ...
To https://github.com/sickn33/profumo-monitor.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## 🔄 Se Non Funziona

### Opzione 1: Usa SSH invece di HTTPS

Se il token non funziona, puoi usare SSH:

1. **Genera chiave SSH** (se non ce l'hai):
```zsh
ssh-keygen -t ed25519 -C "tua-email@example.com"
```
Premi Invio 3 volte (non mettere passphrase)

2. **Copia la chiave pubblica:**
```zsh
cat ~/.ssh/id_ed25519.pub
```
Copia tutto l'output

3. **Aggiungi su GitHub:**
   - Vai su: https://github.com/settings/keys
   - Clicca "New SSH key"
   - Incolla la chiave
   - Salva

4. **Cambia remote a SSH:**
```zsh
git remote set-url origin git@github.com:sickn33/profumo-monitor.git
git push -u origin main
```

### Opzione 2: Usa GitHub CLI

Installa GitHub CLI:
```zsh
brew install gh
gh auth login
```

Poi:
```zsh
git push -u origin main
```

---

## 💡 Suggerimento

Salva il token in un file sicuro per usarlo in futuro:
```zsh
echo "ghp_IL_TUO_TOKEN_QUI" > ~/.github_token
chmod 600 ~/.github_token
```

Poi quando serve, leggi:
```zsh
cat ~/.github_token
```

---

## 🎯 Riepilogo Veloce

1. Vai su: https://github.com/settings/tokens
2. Generate new token (classic)
3. Seleziona `repo`
4. Genera e COPIA il token
5. Usa il token come password quando git chiede

**Fatto!** ✅
