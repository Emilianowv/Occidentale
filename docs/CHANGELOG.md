# Cambios

## 8.0.0 — 29 de octubre de 2026

- El identificador XKB pasa de `wst` a `rom` y el paquete Debian pasa de `occidentale` a `romancescript`.
- Se elimina el alias de comando `occidentale`; el comando único es `romancescript`.
- Rutas de estado y marcadores de bloques actualizados a `romancescript` / `ROMANCESCRIPT ROM`.
- Instalación en Linux con un comando (`install.sh`) o descargando el `.deb`.
- Windows añade un asistente `install.ps1` junto al `.klc`; ambos con validación estática.

## 7.0.0 — 29 de octubre de 2026

- Nombre del proyecto y del teclado: RomanceScript.
- Alcance: español, portugués, francés, italiano, rumano y catalán, con ß/ẞ adicional.
- ñ/Ñ en su posición española; Mayús+coma → ; y Mayús+punto → :.
- Breve y coma inferior en la antigua tecla de anillo/macrón: ă/Ă y ș/Ș, ț/Ț.
- Se conservan el identificador wst, el paquete occidentale y sus respaldos; se añade el comando romancescript.
- README y guías reescritos con el estado real de Linux y Windows.

## 6.2.0 — 26 de octubre de 2026

- La tecla debajo de Escape produce ¿ sin Mayús y ¡ con Mayús.
- Mayús+punto pasa a carón muerto: č š ž ě ď ť ň ř ľ y sus mayúsculas.
- Los dos puntos permanecen en Mayús+antigua tecla Ñ; · y ÷ permanecen en AltGr del punto.
- Se conserva el acceso anterior al carón con Mayús+AltGr+agudo.
- El grave y la tilde literales se escriben con sus acentos muertos seguidos de Espacio.
- Se actualizan Linux, la fuente Windows, el mapa, las guías y el inventario reproducible.

## 6.1.0 — 26 de octubre de 2026

- Grave muerto+n/N produce ñ/Ñ.
- Shift+grave produce tilde muerta para ã/õ; Shift+6 produce circunflejo muerto.
- La antigua tecla Ñ produce ;/:; conserva AltGr para tilde y doble agudo muertos.
- Agudo+s/S y t/T produce ș/Ș y ț/Ț; Shift+coma seguido de s/S conserva ś/Ś.
- Grave+d/D produce đ/Đ. La antigua tecla +/* pasa a anillo/macrón; anillo+o/O añade ø/Ø y anillo+u/U conserva ů/Ů.
- Shift+punto queda reservado, con su función anterior.
- Inventario reproducible de lenguas europeas de alfabeto latino basado en Unicode CLDR.
- Reparto aprobado y verificado; 55/57 repertorios principales revisados completos.

## 6.0.0 — 26 ottobre 2026

- Europeo / EMI Keyboard V5 diventa Occidentale, identificatore e abbreviazione wst.
- Mappa V5 conservata e confrontata in tutti i 196 stati alfanumerici.
- Installazione XKB nativa per X11 e Wayland, catalogo KDE separato da xkb-data.
- Compose esplicito per ç/Ç e ß/ẞ; accenti e legature verificati.
- Configurazione KDE da terminale, migrazione esplicita, alternative conservate.
- Aggiornamento idempotente, backup, rollback, disinstallazione e controlli dei conflitti.
- Pacchetto Debian, archivi riproducibili, checksum e workflow GitHub.
- Manifesto corretto nei quattro livelli ereditati omessi dalla versione precedente.
- Sorgente Windows rinominato, mantenendo esplicito il suo stato preliminare.
