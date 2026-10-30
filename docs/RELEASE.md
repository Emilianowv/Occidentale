# RomanceScript 8.0.0

El proyecto adopta el nombre RomanceScript y el identificador XKB `rom`. El paquete Debian pasa a llamarse `romancescript` y el comando es `romancescript`.

- La nueva versión utiliza `rom` y el paquete `romancescript`; la selección KDE sustituye wst. El paquete anterior puede conservarse durante la transición de las otras cuentas.
- El teclado se instala en `/usr/share/X11/xkb/symbols/rom`; el estado y los respaldos usan `romancescript`.
- Instalación en Linux con un comando: `curl -fsSL https://raw.githubusercontent.com/Emilianowv/RomanceScript/main/install.sh | sh`, o descargando el `.deb`.
- Windows incluye `RomanceScript.klc` y un asistente `install.ps1`, ambos con validación estática; no hay un instalador compilado.

La distribución de teclas no cambia respecto a 7.0: ñ/Ñ en su posición española, Mayús+coma → ;, Mayús+punto → :, ¿/¡ bajo Escape, breve y coma inferior en la antigua tecla +/*, ç/ß con grave, œ/æ con AltGr y los acentos muertos a la derecha de P y de Ñ.

Descargas: paquete Linux `.deb`, código fuente ZIP/TAR.GZ, ZIP Windows con KLC y asistente de descarga, archivos KLC/PowerShell individuales e instalador Linux `install.sh`. Todas las descargas tienen su SHA256 en SHA256SUMS.
