# Occidentale 6.0.0

Europeo Keyboard V5 diventa **Occidentale (wst)**. La mappa resta invariata; l'installazione Linux ora usa XKB nativo e un registro aggiuntivo leggibile da KDE Plasma 6.

Conservati accenti, grave+c → ç, grave+s → ß, AltGr+O → œ/Œ e AltGr+A → æ/Æ. Aggiunti backup, selezione KDE da terminale, aggiornamento, ripristino e rimozione.

Su Debian 13 installare il `.deb`, poi dal proprio utente:

```bash
occidentale user-install
occidentale kde-select --replace emius
```

Omettere `--replace emius` per una nuova installazione. Uscire e rientrare in KDE. Verificare i download con SHA256SUMS.

Il rapporto in `docs/VERIFICA.md` distingue test automatici, sessione KWin isolata e limiti ancora da collaudare nelle applicazioni. La bozza Windows è inclusa come sorgente, senza installer Windows.
