# Diseño de RomanceScript 8.0

El alcance prioritario es español, portugués, francés, italiano, rumano y catalán. Se conserva ß/ẞ como compatibilidad adicional con el alemán. Otros caracteres heredados pueden seguir disponibles, pero no se declara cobertura de sus lenguas.

Respecto a Occidentale 6.2:

- Ñ vuelve a su posición española, con ñ/Ñ.
- Mayús+coma vuelve a producir ; y Mayús+punto, :.
- El anillo y el macrón se sustituyen por breve y coma inferior muertos.
- Breve+a/A produce ă/Ă. Mayús+esa tecla, seguido de s/S o t/T, produce ș/Ș o ț/Ț.
- Se retiran las reglas que obtenían ș/ț con agudo y el prefijo de ś/Ś de Mayús+coma.
- Se conservan los signos ¿/¡ bajo Escape, la tilde en Mayús+grave, el circunflejo en Mayús+6, ç con grave+c y las ligaduras œ/æ en AltGr.

La [guía de teclas](TECLAS.md) muestra las secuencias. El manifiesto contiene 49 posiciones por cuatro niveles: 196 estados comprobados.

El identificador XKB pasa a `rom` y el paquete Debian se llama `romancescript`. El comando es `romancescript`. Las rutas de estado (`/var/lib/romancescript` y `~/.local/state/romancescript`) y los marcadores de bloques (`ROMANCESCRIPT ROM`) usan el nuevo nombre.

La cobertura de letras principales se mide con los datos guardados de Unicode CLDR y el motor real XKB/Compose. Los caracteres auxiliares y la puntuación se muestran aparte. La fuente Windows recibe el mismo reparto previsto, con los límites de su validación estática.
