# Integración Linux

[Instalación](INSTALACION.md) · [Teclas](TECLAS.md) · [Pruebas](VERIFICA.md)

RomanceScript utiliza XKB y Compose. `system-install` compila la distribución antes de instalarla. `user-install` prepara los acentos de cada usuario y `kde-select` la coloca primero en KDE, conservando las alternativas existentes.

## Archivos e identificadores

| Ruta | Contenido |
|---|---|
| `/usr/share/X11/xkb/symbols/wst` | Distribución nativa para X11 y libxkbcommon |
| `/etc/xkb/rules/evdev.xml` | Entrada de catálogo para KDE Plasma 6 |
| `/var/lib/occidentale/` | Estado y respaldos del sistema |
| `~/.XCompose` | Reglas personales de composición, salvo que se use XCOMPOSEFILE |
| `~/.config/kxkbrc` | Selección de teclado en KDE |
| `~/.local/state/occidentale/` | Estado y respaldos del usuario, salvo XDG_STATE_HOME |

Se mantienen el identificador `wst`, el paquete Debian `occidentale` y las rutas y marcadores anteriores para actualizar desde Occidentale sin cambiar las referencias ni perder las copias. El nombre visible es RomanceScript. `romancescript` es el comando principal; `occidentale` funciona como alias.

El paquete instala ambos comandos y sus datos en `/usr/share/occidentale`. Sus scripts de instalación y retirada gestionan los archivos XKB mediante el mismo mecanismo de respaldo. No se modifican los catálogos de `/usr/share/X11/xkb/rules`.

## Acentos

Las reglas personales incluyen grave+c → ç, grave+s → ß y coma inferior+s/t → ș/ț, con sus mayúsculas. El breve para ă y los acentos de las vocales utilizan las tablas estándar.

`user-install` sustituye el bloque gestionado de una instalación anterior y conserva el resto del archivo. Las reglas antiguas que asignaban ș/ț al agudo se retiran de ese bloque. Si el archivo es nuevo se incluye `%L`; si ya existe, se respetan sus inclusiones y su semántica.

Se respeta `XCOMPOSEFILE`. Algunos métodos de entrada o aplicaciones pueden utilizar otra tabla de composición. Por eso las pruebas del motor no sustituyen la escritura en cada aplicación después de cerrar sesión y volver a entrar.

## KDE, X11 y Wayland

`kde-select` conserva variantes, opciones, modelo, comentarios y otras secciones del archivo. Valida la combinación completa y rechaza más de cuatro distribuciones. `--replace ID` permite retirar explícitamente una distribución anterior.

Los archivos personales `symbols/wst` o `rules/evdev` pueden ocultar la versión del sistema. Los conflictos se señalan antes de sobrescribir configuraciones. Los enlaces simbólicos y las claves KDE inmutables también se rechazan.

Hace falta cerrar sesión y volver a entrar para cargar los cambios en el escritorio y las aplicaciones. `setxkbmap` permite una prueba temporal en X11; no configura KWin Wayland. Otros escritorios pueden no mostrar la entrada del catálogo. No se cambia SDDM, la consola de texto ni initramfs.

## Respaldos y retirada

Antes de cada modificación efectiva se guarda el contenido anterior, los permisos y la ausencia original de los archivos. Las operaciones repetidas no duplican entradas. Los respaldos tienen permisos privados y no deben publicarse.

Las escrituras son atómicas por archivo; los errores gestionados provocan una reversión. Un corte de corriente o SIGKILL puede dejar una transacción pendiente: no se promete atomicidad entre varios archivos ante esas interrupciones.

`restore` deshace una transacción cuando los archivos todavía coinciden con su estado posterior. Si hay cambios más recientes, se detiene. `user-remove` conserva añadidos personales y elimina las partes gestionadas cuando puede hacerlo sin perderlos. Los respaldos permanecen después de retirar el paquete.

Los pasos de actualización, recuperación y desinstalación están en [Instalación](INSTALACION.md).
