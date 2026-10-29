# Publicación

Repositorio: [Emilianowv/RomanceScript](https://github.com/Emilianowv/RomanceScript).

Los commits del proyecto utilizan la identidad pública de GitHub. No deben incluirse correos personales, credenciales, archivos de configuración de usuarios ni respaldos. `scripts/audit.py` comprueba los archivos distribuidos.

```bash
make check
make build
python3 scripts/test_deb.py
```

El build genera en `dist/`:

- `RomanceScript-7.0.0.zip`
- `RomanceScript-7.0.0.tar.gz`
- `occidentale_7.0.0_all.deb`
- `SHA256SUMS`

El paquete conserva su nombre interno por compatibilidad con instalaciones anteriores. Instala los comandos `romancescript` y `occidentale`.

El workflow de verificación construye y prueba el paquete en un contenedor Debian 13. El workflow de etiquetas crea una **versión en borrador** después de comprobar que la etiqueta coincide con VERSION:

```bash
git tag v7.0.0
git push origin v7.0.0
```

Revisa los resultados, los archivos y las sumas antes de publicar una versión. Un resultado local no implica que el workflow remoto haya pasado. No se distribuye un instalador Windows sin compilarlo y probarlo en ese sistema.
