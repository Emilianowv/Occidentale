# Provenienza e fedeltà V5

La base è l'archivio fornito dall'utente `Europeo-Keyboard-repository(1).zip`.

SHA256: `b7df76e307ce35307f2781cfe5dc975e2aa65b1b40b00909a02cd67025a1960c`.

Il file `linux/symbols/emius` è stato rinominato `xkb/symbols/wst`. Sono cambiati i commenti descrittivi e il nome del gruppo, ora `Occidentale`. Nella 6.0 le definizioni dei tasti sono rimaste invariate. La 6.1 modifica AC10, AE06, AD11, AD12 e AB08 secondo il reparto documentato in DISENO-6.1.md; le composizioni personalizzate sono state ampliate. Il confronto di 196 risultati qui sotto documenta la versione 6.0.

Il 26 ottobre 2026, con xkb-data 2.42 e libxkbcommon 1.7 su Debian 13, sono state compilate la mappa V5 originale e quella rinominata. Il confronto tramite libxkbcommon ha confermato la coincidenza di tutti i 49 tasti alfanumerici nei quattro stati normale, Shift, AltGr e AltGr+Shift: **196 risultati uguali**.

Il manifesto originale ometteva quattro simboli effettivamente ereditati da `es(basic)`, anche se i commenti li descrivevano come assenti:

| Tasto | Livello 3 | Livello 4 |
|---|---|---|
| AE12, `=` | dead_cedilla | dead_ogonek |
| BKSL, `\` | braceright | dead_breve |

Il nuovo manifesto rappresenta i risultati reali. Le tabelle di tastiera non sono state modificate per adeguarle ai vecchi commenti. Gli accenti dipendono anche dalla base spagnola del pacchetto xkb-data: i test completi del manifesto rendono visibili eventuali cambiamenti futuri a monte.

L'installer precedente riusava lo stato EMI V4 e configurava soltanto la cediglia. Il nuovo gestore usa un ambito `occidentale` separato e definisce esplicitamente anche ß/ẞ. I backup e i file di tastiera delle versioni precedenti non vengono cancellati.

Il sorgente MSKLC è stato rinominato in `windows/Occidentale.klc`, con nome interno `WST` e versione 6.1. La sua validazione rimane statica; non è un port Windows collaudato e mantiene i limiti della trasposizione preliminare originale.
