# Integrazione Linux

## Architettura

`system-install` compila il sorgente prima di modificare file, poi installa:

| Percorso | Scopo |
|---|---|
| `/usr/share/X11/xkb/symbols/wst` | Ricerca nativa di Xorg/Xwayland e libxkbcommon |
| `/etc/xkb/rules/evdev.xml` | Voce aggiuntiva nel catalogo libxkbregistry letto da Plasma 6 |
| `/var/lib/occidentale/` | Stato, lock e backup di sistema |

Il catalogo aggiuntivo contiene `name=wst`, `shortDescription=wst`, `description=Occidentale` e le lingue ita/spa/fra/deu/eng/por. Se esiste già, viene aggiunto o aggiornato soltanto il blocco con marcatori Occidentale. Un identificatore `wst` appartenente a un'altra installazione produce un conflitto esplicito.

I cataloghi Debian in `/usr/share/X11/xkb/rules/` non vengono modificati. Le regole standard hanno già una corrispondenza generica da nome layout a file symbols: non occorre duplicare o sostituire `rules/evdev`. Il nome `wst` non viene aggiunto al vecchio `evdev.lst`: Plasma 6 usa libxkbregistry, non quel catalogo testuale. Per vecchi desktop che leggono soltanto il catalogo XML principale la selezione grafica potrebbe non comparire; il layout nativo rimane utilizzabile con l'identificatore `wst`.

La directory nativa symbols è necessaria per X11, che non usa i percorsi utente di libxkbcommon. Su Debian 13 libxkbcommon 1.7 non sono disponibili i nuovi percorsi di estensione per pacchetti introdotti in 1.13. Si usa dunque la compatibilità richiesta da X11 e dalla versione effettivamente distribuita in Debian 13.

## Accenti e Compose

XKB associa un tasto a un simbolo; le sequenze di accenti morti vengono composte dalle applicazioni o dal loro sistema di input. `user-install` aggiunge un blocco di regole personalizzate in un blocco identificabile:

```text
grave+c → ç    grave+C → Ç
grave+s → ß    grave+S → ẞ
grave+n → ñ    grave+N → Ñ
grave+d → đ    grave+D → Đ
agudo+s/S → ș/Ș    agudo+t/T → ț/Ț
Shift+virgola, poi s/S → ś/Ś
anello+o/O → ø/Ø
```

Se il file è nuovo, include `%L` per mantenere tutte le composizioni della locale. Se esiste, il contenuto e gli include restano inalterati. Un file personalizzato che deliberatamente non include `%L` mantiene questa scelta: per usare anche le composizioni standard bisogna avere un include adeguato. Le regole locali EMI V4/V5 precedenti non vengono cancellate; il blocco Occidentale viene aggiunto dopo di esse.

Viene rispettato `XCOMPOSEFILE` se è impostato; altrimenti si modifica `~/.XCompose`. La posizione effettivamente modificata è memorizzata per la rimozione. Link simbolici vengono rifiutati, compresi quelli nelle directory superiori, per evitare di scrivere in una destinazione inattesa. Impostazioni immutabili KDE e blocchi Compose incompleti producono un errore senza scritture.

Alcuni sistemi di input (IBus/Fcitx o applicazioni con gestione propria) possono ignorare XCompose o caricare una tabella diversa. `doctor` verifica file, registrazione e compilazione; non dimostra che tutte le applicazioni aperte abbiano ricaricato Compose. Il collaudo nelle applicazioni resta necessario dopo il nuovo accesso.

## Selezione KDE e migrazione

`kde-select` legge `[Layout]` in `kxkbrc`, mette `wst` per primo e conserva i layout esistenti, le varianti, i nomi visualizzati, il modello, le opzioni e le altre sezioni del file. Compila prima la combinazione completa e rifiuta più di quattro layout. `--replace ID` rimuove esplicitamente un vecchio identificatore dalla lista; può essere ripetuto.

I file `emius`, `emisp` e gli altri dati EMI rimangono disponibili per il ripristino. Non vengono spostate regole utente estranee. `doctor` segnala file utente `rules/evdev`, `rules/evdev.xml` e `symbols/wst`; un `wst` utente incompatibile blocca la selezione perché potrebbe nascondere la mappa nativa. Le vecchie regole errate devono essere esaminate e salvate prima di correggerle.

È richiesto un nuovo accesso per applicare la configurazione a tutte le applicazioni. `setxkbmap` può agire su una sessione X11, ma **non configura KWin Wayland**: non viene utilizzato per attivare il layout in Wayland.

## Aggiornamenti del sistema

`xkb-data` non possiede `symbols/wst`, quindi i suoi normali aggiornamenti non dovrebbero sostituirlo. Il registro Occidentale risiede separatamente in `/etc/xkb`. Non si usano copie integrali del catalogo Debian, diversion o patch da riapplicare dopo ogni aggiornamento. Se una pulizia esterna elimina la mappa, reinstallare Occidentale la ricrea. Se qualcuno l'ha modificata, l'aggiornamento si ferma per evitare di perderne il contenuto.

Il `.deb` distribuisce il payload in `/usr/share/occidentale`, il comando in `/usr/bin/occidentale` e la documentazione in `/usr/share/doc/occidentale`. `postinst configure` installa i due file nativi tramite il gestore transazionale; `prerm remove` li rimuove/ripristina. `prerm upgrade` lascia lo stato per il nuovo `postinst`. I file nativi gestiti e i backup sono quindi registrati dal gestore Occidentale, non nell'elenco dei file payload di dpkg.

## Backup, ripristino e conflitti

- Utente: `${XDG_STATE_HOME:-~/.local/state}/occidentale/backups/`.
- Sistema: `/var/lib/occidentale/backups/`.
- Ogni snapshot ha un ID temporale UTC e un suffisso casuale, un manifesto JSON con byte codificati e permessi, più lo stato della transazione.
- I backup contengono configurazioni personali: non vanno caricati su GitHub o inclusi in release. La directory e i manifesti sono privati.
- Un lock serializza le operazioni dello stesso ambito. Le sostituzioni dei singoli file sono atomiche; un errore di scrittura gestito ripristina i file già modificati.
- Un'interruzione improvvisa del sistema può lasciare uno snapshot `pending`: conservarlo e usare il suo `before` per recuperare i file. Non viene dichiarata atomicità tra più file in caso di spegnimento o `SIGKILL`.

`restore` è conservativo: prima controlla tutti i file e annulla l'operazione se qualcuno è cambiato. `user-remove` è più selettivo: ripristina byte per byte i file ancora uguali all'ultima versione gestita; altrimenti elimina il blocco Compose o la voce `wst` da KDE mantenendo le altre aggiunte. `system-remove` conserva altre voci aggiunte al registro; una modifica esterna al file symbols blocca la rimozione. Dopo la rimozione dello stato, i backup restano consultabili.

## Diagnostica e recupero

```bash
occidentale doctor
occidentale backups
sudo occidentale backups --scope system
```

Se KDE era già aperto quando hai installato, chiudi e riapri le Impostazioni di sistema per ricaricare il catalogo. Se una singola app non compone ç/ß, riavviala e controlla il suo sistema di input e `XCOMPOSEFILE`.

Per tornare alla configurazione precedente: `occidentale user-remove`, poi nuovo accesso. In una sessione X11, un eventuale recupero temporaneo della base spagnola si può fare con `setxkbmap es`. In Wayland cambia layout tramite KDE o ripristina `kxkbrc` da una console e accedi nuovamente. Prima di rimuovere il pacchetto di sistema, ogni utente deve deselezionare wst: la rimozione amministrativa non modifica le home altrui.

Non vengono cambiati `/etc/default/keyboard`, la tastiera della console Linux, initramfs o la configurazione della schermata di login SDDM.

## Fonti tecniche

- [libxkbcommon 1.5: percorsi utente e sistema e registri aggiuntivi](https://xkbcommon.org/doc/1.5.0/md_doc_user_configuration.html).
- [Plasma 6.3: lettura del catalogo tramite libxkbregistry](https://github.com/KDE/plasma-desktop/blob/Plasma/6.3/kcms/keyboard/xkb_rules.cpp).
- [KDE: configurazione XKB Wayland in kxkbrc](https://community.kde.org/Plasma/Wayland#Custom_keyboard_maps_(XKB)).
- [libxkbcommon: limiti X11 e compatibilità](https://xkbcommon.github.io/libxkbcommon/doc/compatibility.html).
- [Packaging XKB: estensioni moderne e requisiti di versione](https://xkbcommon.org/doc/current/packaging-keyboard-layouts.html).

## Distinzione fra ș romena e ś polacca nella 6.1

L'agudo morto mantiene `dead_acute` e le composizioni vocaliche standard; solo s/S e t/T ricevono le regole romene concordate. Shift+virgola usa internamente `dead_abovecomma` come prefisso distinto, con regole esplicite per ś/Ś e spazio → ´. Usare `dead_acute` su entrambe le posizioni renderebbe impossibile distinguere le due s. La tabella Compose personalizzata è quindi parte necessaria dell'installazione.

L'ex tasto +/* ora produce `dead_abovering` e `dead_macron`: le composizioni standard å/Å, ů/Ů e vocali con macrón restano disponibili, mentre ø/Ø sono aggiunte esplicitamente al prefisso anello. Le parentesi AltGr sullo stesso tasto sono conservate; + e * rimangono sulla fila numerica.
