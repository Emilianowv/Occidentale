# Occidentale 6.1.0

Reparto de acentos acordado para facilitar la escritura de lenguas europeas con alfabeto latino:

- Grave+c/s/n/d → ç/ß/ñ/đ, con sus mayúsculas.
- La antigua tecla Ñ → ;/:.
- Shift+grave → tilde muerta; Shift+6 → circunflejo muerto.
- Agudo+s/t → ș/ț; Shift+coma seguido de s/S → ś/Ś.
- Antigua tecla +/* → anillo/macrón. Anillo+a/o/u → å/ø/ů; con Shift, las vocales con macrón.
- Se conservan œ/Œ, æ/Æ, + y * de la fila numérica, corchetes y llaves AltGr. Shift+punto no cambia.

El inventario Unicode CLDR comprueba 55 de 57 repertorios principales completos; bretón y sami skolt conservan huecos documentados. No se declara cobertura total de caracteres auxiliares o aplicaciones.

Para actualizar: instalar el nuevo .deb, ejecutar `occidentale user-install` desde cada usuario y salir/entrar en la sesión. Actualizar solo el archivo XKB no basta para las reglas Compose personalizadas. Backup, restore y desinstalación permanecen disponibles.

La fuente Windows se actualiza y verifica estáticamente; sigue sin un instalador compilado o probado en Windows.
