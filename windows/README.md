# RomanceScript para Windows

[Inicio](../README.md) · [Guía de teclas](../docs/TECLAS.md)

[RomanceScript.klc](RomanceScript.klc) es el archivo de diseño para Microsoft Keyboard Layout Creator. Contiene las 49 posiciones y el reparto previsto para español, portugués, francés, italiano, rumano y catalán, con ß/ẞ adicional.

El archivo tiene controles estáticos de posiciones, ligaduras y tablas de acentos. **No se ha compilado, instalado ni probado escribiendo en Windows. No se distribuye un setup.exe.**

## Descargar el archivo de diseño

Descarga el [ZIP para Windows](https://github.com/Emilianowv/RomanceScript/releases/latest/download/RomanceScript-8.0.0-Windows.zip) y extráelo. Contiene RomanceScript.klc, install.ps1 y README.txt. También puedes descargar [RomanceScript.klc directamente](https://github.com/Emilianowv/RomanceScript/releases/latest/download/RomanceScript.klc). También puedes usar el asistente [`install.ps1`](install.ps1), que descarga el `.klc` e indica la página de Microsoft Keyboard Layout Creator:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

El asistente no compila ni instala la distribución: solo facilita la descarga.

## Continuar en MSKLC

Abre el archivo en [Microsoft Keyboard Layout Creator](https://www.microsoft.com/en-us/download/details.aspx?id=102134), valida el diseño y compila la DLL y el paquete de instalación. Quedan por probar la instalación y retirada, los acentos, las mayúsculas, los atajos Ctrl y la interacción AltGr/Ctrl+Alt en aplicaciones reales.

El archivo todavía difiere del resultado Linux en los niveles heredados de las posiciones AE12 y BKSL. Algunos acentos complejos también requieren comprobación. No se declara compatibilidad probada con versiones concretas de Windows.
