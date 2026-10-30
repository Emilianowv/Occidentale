# Procedencia

RomanceScript continúa el proyecto llamado Occidentale. La base recibida fue `Europeo-Keyboard-repository(1).zip`, con SHA256 `b7df76e307ce35307f2781cfe5dc975e2aa65b1b40b00909a02cd67025a1960c`.

Occidentale 6.0 conservó las 49 posiciones y sus cuatro niveles de la base, verificados mediante 196 comparaciones. Las versiones 6.1 y 6.2 cambiaron varias posiciones; no se declara identidad con la distribución original para esas versiones ni para RomanceScript.

RomanceScript 7.0 limita el alcance a seis lenguas y adopta el reparto documentado en [Diseño](DISENO.md), conservando los identificadores internos para poder actualizar desde Occidentale. RomanceScript 8.0 adopta el identificador `rom` y el paquete `romancescript`. Las versiones anteriores se consultan en la historia Git y en [Cambios](CHANGELOG.md).

La inclusión `es(basic)` utiliza los archivos de xkeyboard-config ya instalados en Linux. Algunos niveles AltGr se heredan de esa base; el [manifiesto](layout-manifest.json) registra el resultado compilado, no solo los símbolos declarados explícitamente.

El archivo Windows se llama `RomanceScript.klc` y usa el identificador interno ROM. Su validación es estática. No se presenta como una versión Windows compilada o probada.

El archivo original no incluía una licencia de código abierto. Los derechos se mantienen en [COPYRIGHT](../COPYRIGHT). Los datos de Unicode CLDR conservan su licencia Unicode-3.0, incluida en [UNICODE-LICENSE.txt](UNICODE-LICENSE.txt).
