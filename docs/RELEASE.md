# RomanceScript 7.0.0

El proyecto pasa de Occidentale a RomanceScript. Su alcance prioritario queda limitado a español, portugués, francés, italiano, rumano y catalán, con ß/ẞ como compatibilidad adicional.

- ñ/Ñ vuelve a su posición española.
- Mayús+coma y Mayús+punto vuelven a producir ; y :.
- La antigua tecla de anillo/macrón pasa a breve y coma inferior: ă/Ă, ș/Ș y ț/Ț.
- Se conservan ¿/¡ bajo Escape, los acentos de las vocales, ç, œ/Œ y æ/Æ.
- La documentación describe el alcance y los límites sin presentar compatibilidad no probada.

El identificador XKB `wst` y el nombre del paquete Debian `occidentale` se conservan para actualizar las instalaciones anteriores. El comando principal pasa a `romancescript`; el comando anterior sigue funcionando.

Para actualizar desde el paquete Debian, instala `occidentale_7.0.0_all.deb`, ejecuta `romancescript user-install` desde cada usuario y cierra sesión y vuelve a entrar. La selección de teclado existente se conserva.

Windows incluye solo el archivo KLC revisado estáticamente. No hay un instalador compilado ni pruebas de escritura en Windows.
