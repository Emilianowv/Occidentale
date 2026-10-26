# Occidentale 6.2.0

Tres posiciones más cómodas para escribir:

- Debajo de Escape: **¿** sin Mayús y **¡** con Mayús.
- **Mayús+punto**: carón muerto **ˇ**. Seguido de c/s/z/e/d/t/n/r/l produce **č š ž ě ď ť ň ř ľ**, también en mayúsculas.
- Los **:** permanecen en Mayús+antigua tecla Ñ. El punto normal, · y ÷ no cambian.

El grave y la tilde literales siguen disponibles con grave o Mayús+grave a la derecha de P, seguidos de Espacio. También se conserva el acceso anterior al carón. La comparación del inventario confirma que se mantienen todos los caracteres accesibles en la 6.1.

Se conservan las combinaciones de acentos anteriores:

- Grave+c/s/n/d → ç/ß/ñ/đ, con sus mayúsculas.
- La antigua tecla Ñ → ;/:.
- Shift+grave → tilde muerta; Shift+6 → circunflejo muerto.
- Agudo+s/t → ș/ț; Shift+coma seguido de s/S → ś/Ś.
- Antigua tecla +/* → anillo/macrón. Anillo+a/o/u → å/ø/ů; con Shift, las vocales con macrón.
- Se conservan œ/Œ, æ/Æ, + y * de la fila numérica, corchetes y llaves AltGr.

El inventario Unicode CLDR comprueba 55 de 57 repertorios principales completos; bretón y sami skolt conservan huecos documentados. No se declara cobertura total de caracteres auxiliares o aplicaciones.

Para actualizar: instalar el nuevo .deb, ejecutar `occidentale user-install` desde cada usuario y salir/entrar en la sesión. Actualizar solo el archivo XKB no basta para las reglas Compose personalizadas. Backup, restore y desinstalación permanecen disponibles.

La fuente Windows se actualiza y verifica estáticamente; sigue sin un instalador compilado o probado en Windows.
