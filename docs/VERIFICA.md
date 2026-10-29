# Pruebas de RomanceScript 7.0

Las comprobaciones usan el motor real libxkbcommon y las tablas Compose de Linux. El entorno de referencia es Debian 13 con KDE Plasma 6. Las pruebas no instalan el teclado en el escritorio abierto.

## Qué se comprueba

- Las 49 posiciones en cuatro niveles: 196 estados contra el manifiesto.
- ñ/Ñ, ;/:, ¿/¡ y los niveles AltGr conservados.
- Los acentos de vocales, las ligaduras œ/Œ y æ/Æ, ç/Ç y ß/ẞ.
- Breve+a/A → ă/Ă y Mayús+esa tecla seguido de s/S o t/T → ș/Ș y ț/Ț.
- Bloq Mayús, Control y los símbolos literales mediante acento seguido de Espacio.
- Las letras principales de español, portugués, francés, italiano, rumano y catalán, incluidas las mayúsculas. La puntuación y los caracteres auxiliares se muestran aparte.
- Instalación, repetición, actualización del bloque anterior, respaldo, recuperación, conflictos y retirada en directorios temporales.
- Compilación X11 y comparación del mapa exportado por un KWin Wayland aislado y de un mapa cargado y releído en un servidor Xwayland independiente.
- Instalación, reinstalación y retirada del paquete con dpkg en una raíz temporal. El workflow Debian añade un ciclo en un contenedor desechable.
- Las posiciones y tablas principales del archivo Windows, mediante controles estáticos.

## Reproducir las pruebas

```bash
sudo apt install make python3 libxkbcommon-tools xkb-data x11-xkb-utils dpkg-dev fakeroot
make check
make build
python3 scripts/test_deb.py
```

El test dpkg temporal utiliza fakeroot y las herramientas del sistema anfitrión. El modo `--live` está reservado a contenedores desechables: no debe ejecutarse en el sistema del usuario.

Para KWin y X11 aislados:

```bash
sudo apt install kwin-wayland xwayland dbus gcc pkg-config libwayland-dev fuse3
python3 scripts/test_kwin.py
```

Estos tests necesitan sockets e IPC que algunos entornos aislados bloquean. Los procesos y los archivos temporales se retiran al terminar.

## Límites

No se ha abierto una sesión completa Plasma Xorg para estas pruebas: X11 se comprueba mediante un servidor Xwayland independiente. El catálogo se comprueba con libxkbregistry; esto no equivale a completar una selección manual en cada interfaz de escritorio.

La compilación y el mapa correcto no garantizan la escritura en todas las aplicaciones, especialmente si utilizan su propio método de entrada. Tras instalar, cerrar sesión y volver a entrar, conviene escribir en las aplicaciones habituales:

```text
ñ Ñ ç Ç ß ẞ œ Œ æ Æ
á é í ó ú À È Ì Ò Ù
ã õ â ê î ô û ä ë ï ö ü ÿ
ă Ă ș Ș ț Ț l·l ¿ ¡ ; :
```

El archivo Windows no está compilado, instalado ni probado escribiendo en Windows. Sus controles estáticos no sustituyen ese trabajo.

Los resultados remotos se consultan en [GitHub Actions](https://github.com/Emilianowv/RomanceScript/actions). El [informe de idiomas](LENGUAS.md) se regenera sin red mediante `python3 scripts/language_audit.py --write`.
