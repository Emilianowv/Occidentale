# Occidentale · wst

Tastiera latina multilingue, derivata da **EMI / Europeo Keyboard V5**. Il nome visibile è **Occidentale**, l'identificatore XKB e l'abbreviazione sono **wst**. La versione 6.0 ha introdotto un'installazione Linux nativa, selezionabile anche in KDE Plasma 6. La 6.1 introduce il nuovo reparto di accenti concordato: ñ/đ via grave, ș/ț via agudo, ś via Shift+virgola e anello/macrón sulla vecchia posizione +/*.

| Combinazione | Risultato |
|---|---|
| Grave morto + n / N | ñ / Ñ |
| Ex tasto Ñ, con/senza Shift | ; / : |
| Acuto morto + vocale | á é í ó ú, anche maiuscole |
| Grave morto + vocale | à è ì ò ù, anche maiuscole |
| Grave morto + c / C | ç / Ç |
| Grave morto + s / S | ß / ẞ |
| Grave morto + d / D | đ / Đ |
| Agudo morto + s/S, t/T | ș/Ș, ț/Ț |
| Shift + virgola, poi s/S | ś/Ś |
| Ex tasto +, poi a/A, o/O, u/U | å/Å, ø/Ø, ů/Ů |
| Shift + ex tasto +, poi vocale | ā ē ī ō ū / Ā Ē Ī Ō Ū |
| AltGr + O, con Shift | œ / Œ |
| AltGr + A, con Shift | æ / Æ |
| Shift + acuto, poi vocale | dieresi |
| Shift + grave, poi vocale | tilde: ã õ (anche ñ) |
| Shift + 6, poi vocale | circonflesso: â ê î ô û |
| AltGr + E | € |

Il **grave morto** è il tasto subito a destra della P, ereditato dalla base spagnola; il tasto US in alto a sinistra produce invece un grave letterale. La tastiera mantiene numeri e molti simboli nelle posizioni US, con ñ tramite Compose e tasti morti spagnoli. La mappa completa verificata è in [docs/layout-manifest.json](docs/layout-manifest.json).

## Debian 13 e KDE Plasma 6: installazione consigliata

Scarica e verifica il pacchetto `.deb` con il file `SHA256SUMS` della stessa release, quindi dalla cartella del download:

```bash
sha256sum -c SHA256SUMS
sudo apt install ./occidentale_6.1.0_all.deb
occidentale user-install
occidentale kde-select
occidentale doctor
```

Esegui i comandi `user-*` e `kde-select` **dal tuo utente**, senza sudo. Per sostituire il precedente identificatore EMI nella lista KDE, usa `occidentale kde-select --replace emius` al posto di `kde-select`. Gli altri layout e le relative varianti rimangono come alternative. Non viene superato il limite di quattro layout di X11.

**Esci dalla sessione KDE e accedi nuovamente**, anche su X11: ciò ricarica la configurazione del compositore/desktop e le tabelle Compose nelle applicazioni. Il programma prepara la configurazione persistente; non dichiara di avere attivato istantaneamente il layout nella sessione aperta.

In alternativa alla selezione da terminale, riapri le Impostazioni di sistema di KDE, cerca **Tastiera → Disposizioni**, abilita la gestione delle disposizioni e aggiungi **Occidentale**. Se è impostato un filtro di lingua, scegli tutte le lingue o una delle lingue occidentali registrate. `user-install` è necessario per le sequenze personalizzate, incluse ș/ț, ś/Ś e anello+o → ø.

## Installazione dal sorgente o archivio ZIP/TAR

```bash
sudo apt install python3 xkb-data libxkbcommon0 libxkbcommon-tools x11-xkb-utils
./occidentale test
sudo ./occidentale system-install
./occidentale user-install
./occidentale kde-select --replace emius
./occidentale doctor
```

Ometti `--replace emius` se non hai quel vecchio layout. L'installazione dal sorgente richiede di conservare la cartella per usare successivamente gli stessi comandi. Il pacchetto Debian installa invece il comando `occidentale` nel sistema.

## Aggiornamenti, backup e ripristino

Per aggiornare, installa il nuovo `.deb` e ripeti `occidentale user-install`. Dal sorgente, usa `system-install` della nuova versione e poi `user-install`. Operazioni ripetute non duplicano le voci. Sono conservati snapshot prima delle modifiche effettive, con contenuto precedente, permessi e assenza originaria dei file.

```bash
occidentale backups
occidentale restore
sudo occidentale backups --scope system
sudo occidentale restore --scope system
```

`restore` annulla **l'ultima transazione** del relativo ambito; `--backup ID` sceglie uno snapshot preciso. Per esempio, dopo `user-install` e `kde-select`, il primo restore annulla la selezione KDE e il secondo le aggiunte Compose. Un ripristino che sovrascriverebbe modifiche successive viene annullato con una spiegazione. Dettagli in [docs/LINUX.md](docs/LINUX.md).

## Disinstallazione

Prima, ogni utente interessato esegue:

```bash
occidentale user-remove
```

Esci e rientra con un layout alternativo, poi:

```bash
sudo apt remove occidentale
```

Per l'installazione dal sorgente, usa `sudo ./occidentale system-remove`. Le configurazioni precedenti vengono recuperate se sono ancora inalterate. Se hai aggiunto altre regole Compose o modificato KDE nel frattempo, vengono rimosse soltanto le parti gestite da Occidentale. I backup restano disponibili anche dopo `apt purge`.

## Verifiche e distribuzione

```bash
make check
make build
python3 scripts/test_deb.py
```

Il build genera ZIP, TAR.GZ, pacchetto Debian `all` e checksum in `dist/`. Il test Debian usa **dpkg reale in una radice temporanea**, compresi gli script di installazione/rimozione. Per verificare KWin e il protocollo X11 in una sessione isolata: `python3 scripts/test_kwin.py` (dipendenze in [docs/VERIFICA.md](docs/VERIFICA.md)). Nessuno di questi test seleziona la tastiera nel desktop dell'utente.

Risultati e limiti dei test sono in [docs/VERIFICA.md](docs/VERIFICA.md). Il sorgente Windows rinominato [Occidentale.klc](windows/Occidentale.klc) resta una bozza MSKLC: non viene distribuito un installer Windows non collaudato.

Destinazione GitHub: **Emilianowv/Occidentale**. [Guida alla pubblicazione](docs/PUBBLICAZIONE.md). I pacchetti escludono configurazioni personali, backup locali e cronologia Git; un audit impedisce email personali. Per attribuzioni e condizioni di distribuzione, leggi [COPYRIGHT](COPYRIGHT).

## Diseño y cobertura lingüística

[Inventario de lenguas y caracteres faltantes](docs/LENGUAS.md), calculado con Unicode CLDR y las tablas XKB/Compose reales. El reparto aprobado se describe en [docs/DISENO-6.1.md](docs/DISENO-6.1.md). Shift+punto conserva los dos puntos como posición reservada. El inventario comprueba 55 de 57 repertorios principales completos, sin prometer cobertura tipográfica o de aplicaciones total.
