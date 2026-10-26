# Occidentale per Windows: sorgente preliminare

`Occidentale.klc` è il sorgente MSKLC rinominato dalla bozza Europeo V5: nome interno `WST`, descrizione `Occidentale`, versione 6.0. Le 49 posizioni e le combinazioni essenziali sono controllate da `scripts/check_windows_klc.py`.

Non sono state eseguite compilazione con Microsoft Keyboard Layout Creator, installazione o prove di digitazione su Windows. Non viene prodotto né incluso un `setup.exe`.

La bozza non è equivalente in ogni livello al risultato XKB reale: per AE12 e BKSL non rappresenta i quattro simboli ereditati da `es(basic)` descritti in [PROVENIENZA.md](../docs/PROVENIENZA.md). Anche alcuni accenti morti complessi richiedono una verifica con MSKLC. Questi limiti non vengono mascherati dalla rinomina.

Per completare il port, aprire il sorgente in MSKLC su Windows, validarlo, correggere le differenze e compilare DLL e pacchetto di installazione. Provare poi accenti, ç/Ç, ß, œ/Œ, æ/Æ, Caps Lock, Ctrl+lettera e interferenze AltGr/Ctrl+Alt in applicazioni reali. Distribuire binari Windows solo dopo questo collaudo.

La bozza 6.1 aggiorna anche anello/macrón, agudo romeno, prefisso polacco e grave+d. Le tabelle di accenti morti vengono controllate per duplicati; questa verifica resta statica e non sostituisce MSKLC su Windows.
