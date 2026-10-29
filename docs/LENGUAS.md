# Cobertura de RomanceScript

RomanceScript 7.0.0 · datos Unicode CLDR release-49 · Compose en_US.UTF-8.

El alcance prioritario es español, portugués, francés, italiano, rumano y catalán. Se conserva ß/ẞ como compatibilidad adicional.

Se han probado teclas directas, Shift/AltGr y un acento muerto seguido de una tecla imprimible. Las mayúsculas también se comprueban. Los dígrafos se evalúan como cadenas. “Falta” significa que no apareció en esas rutas; puede existir otra vía con varios acentos, entrada Unicode o una tecla Compose configurada aparte.

Los repertorios principales, auxiliares y de puntuación se mantienen separados. Un repertorio principal cubierto no equivale a soporte ortográfico completo ni a pruebas de aplicaciones. CLDR no es una medida de frecuencia de uso.

## Romances

| Lengua | Caracteres especiales principales (ambos casos) | Faltan en las rutas probadas |
|---|---|---|
| Español | Á É Í Ñ Ó Ú Ü á é í ñ ó ú ü | — |
| Francés | À Â Æ Ç È É Ê Ë Î Ï Ô Ù Û Ü à â æ ç è é ê ë î ï ô ù û ü ÿ Œ œ Ÿ | — |
| Italiano | À È É Ì Ò Ù à è é ì ò ù | — |
| Portugués | À Á Â Ã Ç É Ê Í Ó Ô Õ Ú à á â ã ç é ê í ó ô õ ú | — |
| Catalán | · À Ç È É Í Ï Ò Ó Ú Ü à ç è é í ï ò ó ú ü | — |
| Rumano | Â Î â î Ă ă Ș ș Ț ț | — |

## Rutas actuales de interés

| Carácter | Cómo se obtiene |
|---|---|
| ñ | Ñ |
| Ñ | Shift+Ñ |
| ç | tecla de grave → C |
| Ç | tecla de grave → Shift+C |
| ß | AltGr+S |
| ẞ | Shift+AltGr+S |
| ă | tecla de breve → A |
| Ă | tecla de breve → Shift+A |
| ș | Shift+tecla de breve → S |
| Ș | Shift+tecla de breve → Shift+S |
| ț | Shift+tecla de breve → T |
| Ț | Shift+tecla de breve → Shift+T |
| œ | AltGr+O |
| Œ | Shift+AltGr+O |
| æ | AltGr+A |
| Æ | Shift+AltGr+A |
| ã | Shift+tecla de grave → A |
| Ã | Shift+tecla de grave → Shift+A |
| õ | Shift+tecla de grave → O |
| Õ | Shift+tecla de grave → Shift+O |
| à | tecla de grave → A |
| è | tecla de grave → E |
| ì | tecla de grave → I |
| ò | tecla de grave → O |
| ù | tecla de grave → U |
| á | tecla de agudo → A |
| é | tecla de agudo → E |
| í | tecla de agudo → I |
| ó | tecla de agudo → O |
| ú | tecla de agudo → U |
| â | Shift+6 → A |
| ê | Shift+6 → E |
| î | Shift+6 → I |
| ô | Shift+6 → O |
| û | Shift+6 → U |
| ä | Shift+tecla de agudo → A |
| ë | Shift+tecla de agudo → E |
| ï | Shift+tecla de agudo → I |
| ö | Shift+tecla de agudo → O |
| ü | Shift+tecla de agudo → U |
| ÿ | Shift+tecla de agudo → Y |
| Ÿ | Shift+tecla de agudo → Shift+Y |
| · | AltGr+. |
| ¿ | ¿ |
| ¡ | Shift+¿ |

## Auxiliares y puntuación

Estos huecos se muestran aparte: incluyen grafías extranjeras, históricas y tipografía que no forman el alfabeto principal.

| Lengua | Auxiliares ausentes | Puntuación ausente |
|---|---|---|
| Español | Å Ø å ø Ā ā Ē ē Ī ī Ō ō Ū ū | ‐ ‑ – — † ‡ … ′ ″ |
| Francés | Å Ø å ø Ā ā Ē ē Ī ī Ĳ ĳ | ‐ ‑ – — † ‡ … |
| Italiano | Å Ø å ø | ‑ — … |
| Portugués | Å Ø å ø Ā ā Ē ē Ī ī Ō ō Ū ū | ‐ ‑ – — † ‡ … ′ ″ |
| Catalán | Å Ø å ø Ā ā Ē ē Ī ī Ō ō Ū ū | ‐ ‑ – — † ‡ … ′ ″ |
| Rumano | Å å | ‐ ‑ – — … |

## Datos pendientes


## Fuentes y reproducción

- [CLDR: definición de repertorios principales y auxiliares](https://cldr.unicode.org/translation/core-data/exemplars).
- [Datos CLDR 49](https://github.com/unicode-org/cldr/tree/release-49/common/main). Cada lengua del JSON conserva el URL y SHA256 de su fuente.
- `python3 scripts/language_audit.py --write` regenera este informe usando XKB y Compose reales, sin red.
- `python3 scripts/update_language_data.py` actualiza la instantánea fijada; requiere red e ICU solo para esa tarea.
- Datos de Unicode bajo Unicode-3.0; véase `UNICODE-LICENSE.txt`.
