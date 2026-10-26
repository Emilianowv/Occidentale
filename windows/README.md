# 🪟 Occidentale para Windows

[← Inicio](../README.md) · [Guía de teclas](../docs/TECLAS.md) · [¿Buscas Linux?](../docs/INSTALACION.md)

**Windows también forma parte del proyecto.** El archivo [Occidentale.klc](Occidentale.klc) contiene la distribución del teclado para Microsoft Keyboard Layout Creator (MSKLC), con el reparto de acentos de la versión **6.2**: **¿ / ¡ debajo de Escape** y **carón muerto ˇ en Mayús+punto**.

## ¿Puedo instalarlo ya?

Por ahora está disponible el **archivo de diseño del teclado**. Todavía falta generar y probar el instalador en Windows: **no hay un `setup.exe` listo para el uso cotidiano**. Los controles automáticos del archivo se han realizado, pero no sustituyen una prueba de escritura en Windows.

Si buscas una instalación ya comprobada, la versión disponible para ello es la de [Linux en Debian 13 y KDE Plasma 6](../docs/INSTALACION.md).

## Descargar el archivo de Windows

1. [Descarga el ZIP del proyecto](https://github.com/Emilianowv/Occidentale/archive/refs/heads/main.zip).
2. Extrae el ZIP.
3. Abre la carpeta **windows**: allí encontrarás **Occidentale.klc**.

El archivo `.klc` es un diseño que abre MSKLC; no se instala haciendo doble clic como si fuera un programa.

## Si quieres ayudar a probarlo

Estos pasos son para preparar y comprobar la versión Windows. No se han ejecutado en este proyecto sobre un equipo Windows.

1. Descarga [Microsoft Keyboard Layout Creator desde Microsoft](https://www.microsoft.com/en-us/download/details.aspx?id=102134) y revisa los requisitos que indica el fabricante.
2. Abre `Occidentale.klc` con MSKLC.
3. Valida el diseño y comprueba los acentos y niveles de las teclas antes de generar el paquete.
4. Compila la DLL y el paquete de instalación; después prueba la instalación, selección del teclado y escritura en aplicaciones reales.
5. Comprueba también la desinstalación y la vuelta al teclado anterior antes de distribuir el instalador.

Si encuentras un problema, [comunícalo aquí](https://github.com/Emilianowv/Occidentale/issues), indicando tu versión de Windows, aplicación y combinación. No incluyas contraseñas ni datos personales.

<details>
<summary><strong>Estado técnico del archivo 6.2</strong></summary>

El nombre interno es `WST` y la descripción, `Occidentale`. `scripts/check_windows_klc.py` comprueba estáticamente las 49 posiciones, las combinaciones principales y la ausencia de duplicados en las tablas de acentos muertos.

Incluye el reparto previsto de ñ/đ con grave, ș/ț con agudo, ś con Mayús+coma, anillo para å/ø/ů, macrón con Mayús y las ligaduras œ/æ.

El archivo no es equivalente en todos sus niveles al resultado Linux: las posiciones `AE12` y `BKSL` no contienen los cuatro símbolos heredados de `es(basic)` descritos en [Procedencia](../docs/PROVENIENZA.md). También quedan por comprobar los acentos muertos complejos, Bloq Mayús, Ctrl+letra y la interacción AltGr/Ctrl+Alt. No se declara compatibilidad probada con versiones concretas de Windows.

</details>
