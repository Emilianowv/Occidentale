# RomanceScript

Distribución de teclado QWERTY para escribir en **español, portugués, francés, italiano, rumano y catalán**. Conserva **ß/ẞ** como compatibilidad adicional con el alemán.

## Descargas

- **[Linux Debian/Ubuntu: paquete .deb](https://github.com/Emilianowv/RomanceScript/releases/latest/download/romancescript_8.0.0_all.deb)**
- **[Windows: ZIP con el archivo de diseño KLC](https://github.com/Emilianowv/RomanceScript/releases/latest/download/RomanceScript-8.0.0-Windows.zip)**. No contiene un instalador compilado.
- [Código fuente ZIP](https://github.com/Emilianowv/RomanceScript/releases/latest/download/RomanceScript-8.0.0.zip), [TAR.GZ](https://github.com/Emilianowv/RomanceScript/releases/latest/download/RomanceScript-8.0.0.tar.gz) y [SHA256SUMS](https://github.com/Emilianowv/RomanceScript/releases/latest/download/SHA256SUMS).

La abreviatura y el identificador XKB son **rom**. Al actualizar desde wst, instala el paquete y ejecuta `romancescript user-install` y `romancescript kde-select` desde cada cuenta KDE. Después cierra sesión y vuelve a entrar.

## Distribución

La **ñ/Ñ** está en su posición española. **Mayús+coma** escribe **;** y **Mayús+punto** escribe **:**.

| Tecla o combinación | Resultado |
|---|---|
| Debajo de Escape, sin/con Mayús | ¿ / ¡ |
| Grave, después c/C | ç / Ç |
| Grave, después s/S | ß / ẞ |
| Mayús+grave, después a/o | ã / õ |
| Mayús+6, después vocal | â ê î ô û |
| Tecla junto a la barra inversa, después a/A | ă / Ă |
| Mayús+esa tecla, después s/S o t/T | ș / Ș / ț / Ț |
| AltGr+O / AltGr+A | œ / æ; con Mayús, Œ / Æ |
| AltGr+punto | · |

El agudo y la diéresis se conservan a la derecha de Ñ. Para formar una letra acentuada, pulsa el acento, suéltalo y pulsa la letra. La [guía de teclas](docs/TECLAS.md) describe las posiciones y las mayúsculas.

## Sistemas

- **Linux:** instalación XKB, reglas Compose para los acentos y selección desde KDE. Se prueba en Debian 13 con KDE Plasma 6, KWin Wayland y un servidor X11 independiente. Incluye copias de seguridad, actualización y desinstalación.
- **Windows:** se incluye [RomanceScript.klc](windows/RomanceScript.klc) y un asistente [install.ps1](windows/install.ps1) para descargarlo y abrirlo en Microsoft Keyboard Layout Creator. Tienen controles estáticos; **no se han compilado ni probado en Windows y no hay un instalador Windows compilado**.

[Descargar el código en ZIP](https://github.com/Emilianowv/RomanceScript/archive/refs/heads/main.zip) · [Instalar en Linux con un comando](docs/INSTALACION.md) · [Archivo Windows](windows/README.md)

## Alcance y comprobaciones

Las pruebas del motor Linux cubren las letras principales de los seis idiomas indicados, incluidas sus mayúsculas. Esto no implica cobertura de todos los signos tipográficos ni pruebas de escritura en todas las aplicaciones. Los caracteres que faltan se indican en el [informe de idiomas](docs/LENGUAS.md).

[Pruebas y límites](docs/VERIFICA.md) · [Diseño](docs/DISENO.md) · [Cambios](docs/CHANGELOG.md) · [Problemas y propuestas](https://github.com/Emilianowv/RomanceScript/issues)

## Desarrollo

```bash
make check
make build
python3 scripts/test_deb.py
```

El build genera archivos ZIP y TAR.GZ, un paquete Debian y sus sumas de comprobación. Los detalles de instalación están en [Integración Linux](docs/LINUX.md); los de distribución, en [Publicación](docs/PUBBLICAZIONE.md). Los derechos y la procedencia se describen en [COPYRIGHT](COPYRIGHT) y [Procedencia](docs/PROVENIENZA.md).
