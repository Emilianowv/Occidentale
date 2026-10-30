# Publicación

Repositorio: [Emilianowv/RomanceScript](https://github.com/Emilianowv/RomanceScript).

Los commits del proyecto utilizan la identidad pública de GitHub. No deben incluirse correos personales, credenciales, archivos de configuración de usuarios ni respaldos. `scripts/audit.py` comprueba los archivos distribuidos.

```bash
make check
make build
python3 scripts/test_deb.py
```

El build genera en `dist/`:

- `RomanceScript-8.0.0.zip`
- `RomanceScript-8.0.0.tar.gz`
- `romancescript_8.0.0_all.deb`
- `RomanceScript-8.0.0-Windows.zip`
- `RomanceScript.klc`, `install.ps1` e `install.sh`
- `SHA256SUMS`

El paquete se llama `romancescript` e instala el comando `romancescript`. La versión publicada adjunta también los archivos KLC y PowerShell individuales para su descarga directa; ambos tienen solo validación estática.

El workflow de verificación construye y prueba el paquete en un contenedor Debian 13. El workflow de etiquetas crea una **versión pública** después de comprobar que la etiqueta coincide con VERSION:

```bash
git tag v8.0.0
git push origin v8.0.0
```

Revisa los resultados, los archivos y las sumas antes de publicar una versión. Un resultado local no implica que el workflow remoto haya pasado. No se distribuye un instalador Windows compilado; el `.klc` y el script PowerShell no se han compilado ni probado en ese sistema.
