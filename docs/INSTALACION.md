# Instalar RomanceScript en Linux

[← Inicio](../README.md) · [Guía de teclas](TECLAS.md) · [¿Buscas Windows?](../windows/README.md)

La instalación está verificada en **Debian 13 con KDE Plasma 6**. Incluye el teclado, las combinaciones de acentos y una copia de tu configuración anterior.

## Instalación rápida (un comando)

En Debian 13 con KDE Plasma 6, abre una terminal y ejecuta:

```bash
curl -fsSL https://raw.githubusercontent.com/Emilianowv/RomanceScript/main/install.sh | sh
```

El script descarga el paquete de la versión 8.0.0, comprueba su SHA256, lo instala con sus dependencias y configura tus acentos y la selección KDE. El comando queda instalado en el sistema. Después guarda tu trabajo, cierra sesión y vuelve a entrar. Si prefieres revisarlo antes, descarga [`install.sh`](../install.sh), ábrelo y ejecútalo como `./install.sh`.

También puedes [descargar el paquete `.deb`](#si-tienes-un-paquete-debian-deb) e instalarlo con un solo archivo.

## 1. Descarga y abre la carpeta

[Descarga el ZIP del proyecto](https://github.com/Emilianowv/RomanceScript/archive/refs/heads/main.zip), extráelo y abre una terminal dentro de la carpeta **RomanceScript-main**. En muchos gestores de archivos puedes hacerlo con clic derecho → «Abrir terminal aquí».

## 2. Instala el teclado

En Debian 13, copia estos comandos en la terminal, uno tras otro:

```bash
sudo apt install python3 xkb-data libxkbcommon0 libxkbcommon-tools x11-xkb-utils
./romancescript test
sudo ./romancescript system-install
./romancescript user-install
```

La contraseña que puede pedir `sudo` es la de tu equipo. Al escribirla en la terminal no aparecen caracteres: es normal.

`system-install` añade el teclado al sistema. `user-install` prepara tus acentos personalizados; este último comando se ejecuta **sin sudo**, desde tu usuario. Si el equipo tiene varios usuarios, cada uno necesita ejecutar `user-install`.

**Conserva la carpeta:** la necesitarás para actualizar, consultar las copias o desinstalar si utilizas este método.

## 3. Selecciónalo en KDE Plasma

```bash
./romancescript kde-select
./romancescript doctor
```

RomanceScript queda primero y tus teclados actuales siguen disponibles como alternativas. Si ya tienes cuatro distribuciones configuradas, el programa pedirá que retires una antes de añadir otra.

Si estás sustituyendo el antiguo teclado `emius`, usa `./romancescript kde-select --replace emius` en lugar del primer comando.

También puedes abrir **Preferencias del sistema → Teclado → Distribuciones**, habilitar la gestión de distribuciones y añadir **RomanceScript**. Si hay un filtro por idioma, muestra todos los idiomas. Las reglas de acentos del paso 2 siguen siendo necesarias.

**Guarda tu trabajo, cierra sesión y vuelve a entrar.** Así el escritorio y las aplicaciones cargan el teclado y sus acentos. No hace falta reiniciar el equipo.

## 4. Prueba tus primeras palabras

Abre tu editor habitual y prueba:

```text
español · português · français · italiano · română · català
ñ Ñ · ç Ç · œ Œ · æ Æ · ă Ă · ș Ș · ț Ț · ß ẞ
```

La [guía de teclas](TECLAS.md) explica las combinaciones. `doctor` comprueba la instalación, pero esta pequeña prueba confirma cómo se comporta tu aplicación.

## ¿Ubuntu, Xfce u otro escritorio?

El teclado usa el formato nativo de Linux y los pasos de instalación desde el ZIP sirven como base para sistemas compatibles. **El entorno comprobado es Debian 13/KDE Plasma 6:** Ubuntu, Xfce y otros escritorios aún necesitan pruebas propias.

`kde-select` configura solamente KDE. Otros escritorios pueden no mostrar RomanceScript en su selector aunque el archivo esté instalado. En una sesión **X11**, puedes probarlo temporalmente con:

```bash
setxkbmap rom
```

Antes de probar, anota el identificador de tu distribución habitual para poder volver a ella. Este comando no configura la selección persistente del escritorio ni funciona como selector de Wayland. En **Wayland** la selección depende del escritorio: estas instrucciones automatizan KDE. No se modifican la consola de texto ni la pantalla de inicio de sesión.

## Si tienes un paquete Debian `.deb`

El paquete se llama `romancescript`. Instala el teclado y el comando `romancescript` en el sistema.

Descarga [romancescript_8.0.0_all.deb](https://github.com/Emilianowv/RomanceScript/releases/latest/download/romancescript_8.0.0_all.deb) y su [SHA256SUMS](https://github.com/Emilianowv/RomanceScript/releases/latest/download/SHA256SUMS). Desde la carpeta de descarga, verifica el archivo antes de instalar:

```bash
grep '  romancescript_8.0.0_all.deb$' SHA256SUMS | sha256sum -c -
sudo apt install ./romancescript_8.0.0_all.deb
romancescript user-install
romancescript kde-select
romancescript doctor
```

Continúa solo si la comprobación muestra **OK** para el paquete. Este método instala el comando `romancescript` en el sistema: ya no necesita el prefijo `./` ni conservar la carpeta del proyecto. Después, cierra sesión y vuelve a entrar.

La página de Releases contiene también los archivos del código fuente y el ZIP de Windows.

## Actualizar

Con el ZIP: descarga la nueva versión, extráela en una carpeta aparte y repite `system-install` con sudo y `user-install` sin sudo desde esa carpeta. Conserva la nueva carpeta para gestionar esa instalación.

Con el `.deb`: instala el nuevo paquete y ejecuta `romancescript user-install` y `romancescript kde-select` desde cada usuario.

La versión 8 utiliza `rom`. La selección KDE sustituye automáticamente el antiguo `wst` y conserva los otros teclados. Las reglas Compose anteriores se sustituyen sin borrar las reglas personales. Cada operación guarda una copia para volver atrás.

El paquete antiguo `occidentale`, si está instalado, puede permanecer durante la transición para que las otras cuentas sigan utilizando wst hasta que se actualicen. La versión nueva solo instala el comando `romancescript`; el paquete anterior y sus respaldos no se eliminan automáticamente.

Después cierra sesión y vuelve a entrar. Repetir estos pasos no duplica las entradas y las modificaciones efectivas generan copias de seguridad.

## Volver atrás

Si instalaste desde el ZIP, abre una terminal en su carpeta:

```bash
./romancescript backups
./romancescript restore
```

`restore` deshace **la última operación**. Si primero instalaste los acentos y después seleccionaste el teclado en KDE, el primer `restore` deshace la selección y el segundo deshace los acentos. Puedes elegir una copia concreta con `--backup ID`. Si hay cambios posteriores que podrían perderse, el programa se detiene y lo explica.

Las copias del sistema se consultan y restauran por separado:

```bash
sudo ./romancescript backups --scope system
sudo ./romancescript restore --scope system
```

Con el paquete `.deb`, utiliza los mismos comandos sin `./`.

## Desinstalar

Desde la carpeta del ZIP, cada usuario que lo utiliza ejecuta:

```bash
./romancescript user-remove
```

Selecciona un teclado alternativo, cierra sesión y vuelve a entrar. Después elimina la instalación del sistema:

```bash
sudo ./romancescript system-remove
```

Con el paquete `.deb`, usa `romancescript user-remove`, cambia de teclado y vuelve a entrar; después ejecuta `sudo apt remove romancescript`.

Las copias de seguridad se conservan. Los cambios ajenos a RomanceScript se respetan; si hay un conflicto, el programa lo indica antes de sobrescribirlos.

## Si algo no funciona

- **No aparece en KDE:** cierra y vuelve a abrir Preferencias del sistema; comprueba el filtro de idioma y ejecuta `doctor`.
- **Aparece, pero siguen las teclas anteriores:** guarda tu trabajo, cierra sesión y vuelve a entrar.
- **Fallan ç, ß, ș o ț en una aplicación:** comprueba que ejecutaste `user-install` sin sudo y vuelve a abrir la aplicación después del nuevo acceso. Algunos métodos de entrada gestionan sus propios acentos.
- **Necesitas ayuda:** [abre una incidencia](https://github.com/Emilianowv/RomanceScript/issues) con tu distribución, escritorio, X11/Wayland, aplicación y combinación que falla. Revisa cualquier salida antes de compartirla para no incluir información personal.

Para los detalles del sistema y del respaldo, consulta [Integración Linux](LINUX.md). Los resultados y límites de las pruebas están en [Verificaciones](VERIFICA.md).
