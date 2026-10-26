# Verifiche del 26 ottobre 2026

Ambiente reale: Debian GNU/Linux 13, Plasma/KWin 6.3.6, libxkbcommon 1.7.0, xkb-data 2.42, x11-xkb-utils 7.7.

| Controllo | Esito |
|---|---|
| Confronto V5 originale → wst, 49 tasti × 4 stati | 196 risultati identici |
| Test automatici di layout e gestore | 21 test superati |
| Accenti gravi, acuti, circonflessi e dieresi | 40 combinazioni maiuscole/minuscole verificate tramite libxkbcommon Compose |
| Grave+c/C e grave+s/S | ç/Ç e ß/ẞ verificati da sequenze di tasti fisici |
| Legature, ñ, ASCII, livelli AltGr | Inclusi nei 196 controlli del manifesto |
| Caps Lock, Control e accenti seguiti da spazio | Superati |
| Compilazione X11 con xkbcomp | File XKM generato e riletto |
| Scoperta KDE tramite libxkbregistry | Occidentale/wst presente nell'elenco xkbcli usando il registro aggiuntivo |
| KWin 6 isolato su Wayland | Avviato; letta tramite wl_keyboard la mappa inviata dal compositore; 196 stati corretti |
| Server X11 temporaneo | Xwayland indipendente con -nokeymap; mappa caricata con xkbcomp e riletta dal server; 196 stati corretti |
| Backup, reinstallazione, aggiornamento, restore, rimozione | Verificati in directory temporanee, con confronto dei byte |
| Modifiche successive personali | Compose, opzioni KDE e altre voci del registro conservate |
| Conflitti, link simbolici e blocchi incompleti | Rifiutati senza sovrascrivere i dati |
| Errore di scrittura simulato | Rollback dei file già modificati verificato |
| Pacchetto Debian con dpkg reale e fakeroot | Installazione, reinstallazione, rimozione, purge e compilazione del payload installato superati in radice temporanea |
| Archivi ZIP/TAR e pacchetto .deb | Build deterministico e checksum verificati |
| Sorgente Windows | 49 posizioni e combinazioni essenziali controllate staticamente |

La sessione KWin dei test usa home, configurazione, runtime e bus D-Bus temporanei; non è stata modificata la disposizione del desktop aperto. Il test Wayland verifica il caricamento di `kxkbrc` nel compositore e il contenuto esportato al client. Compose viene poi verificato con la tabella dell'utente di prova; non è una simulazione di digitazione in ogni applicazione grafica.

## Riprodurre i test

```bash
sudo apt install make python3 libxkbcommon-tools xkb-data x11-xkb-utils dpkg-dev fakeroot
make check
make build
python3 scripts/test_deb.py
```

Il test dpkg opera in una radice temporanea con gli script di manutenzione reali, eseguiti in modalità chrootless e con le librerie dell'host; la dipendenza dal database di pacchetti vuoto viene esclusa soltanto per quel test. Il workflow Debian esegue inoltre `scripts/test_deb.py --live` in un container usa e getta, senza queste esclusioni.

Per KWin e X11 isolati servono anche:

```bash
sudo apt install kwin-wayland xwayland dbus gcc pkg-config libwayland-dev fuse3
python3 scripts/test_kwin.py
```

I test KWin e fakeroot richiedono risorse IPC vietate da alcuni sandbox. In quel caso vanno eseguiti nel normale terminale; non servono privilegi root. I file temporanei e i processi vengono rimossi al termine.

## Limiti del collaudo

- Non è stata aperta una sessione completa Plasma **Xorg**: il protocollo X11 è stato provato con un server Xwayland indipendente e il formato XKB con xkbcomp.
- La ricerca nel catalogo è stata verificata attraverso la stessa libreria usata da KDE; non è stata completata una selezione manuale nella finestra del KCM.
- Firefox, Chromium, LibreOffice, applicazioni Qt/GTK con IBus/Fcitx, login SDDM e console Linux non sono dichiarati collaudati con digitazione reale. Il progetto non cambia SDDM né console.
- Il sorgente Windows non è compilato o installato e mantiene le differenze descritte nella sua guida.
- I workflow GitHub preparati non si considerano eseguiti finché non compare un risultato remoto effettivo.

Per il collaudo finale nelle applicazioni, dopo il nuovo accesso scrivere:

```text
à è ì ò ù À È Ì Ò Ù
á é í ó ú Á É Í Ó Ú
ä ë ï ö ü Ä Ë Ï Ö Ü
â ê î ô û Â Ê Î Ô Û
ç Ç ß ẞ œ Œ æ Æ ñ Ñ
[] {} / ? \ | @ # €
```

Controllare inoltre copia/incolla/annulla, Alt+Tab, Caps Lock, cambio tra layout alternativi e recupero della configurazione precedente.
