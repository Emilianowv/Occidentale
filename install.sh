#!/bin/sh
# Instala una versión publicada de RomanceScript en Debian/Ubuntu.
set -eu

if [ "$(id -u)" -eq 0 ]; then
    echo "Ejecuta este script sin sudo; pedirá permisos cuando los necesite." >&2
    exit 1
fi
for command in curl sha256sum apt-get sudo; do
    command -v "$command" >/dev/null 2>&1 || { echo "Falta $command." >&2; exit 1; }
done
version="${ROMANCESCRIPT_VERSION:-8.0.0}"
case "$version" in *[!0-9.]*|'') echo "Versión no válida." >&2; exit 1;; esac
package="romancescript_${version}_all.deb"
url="https://github.com/Emilianowv/RomanceScript/releases/download/v${version}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
curl -fL "$url/$package" -o "$tmp/$package"
curl -fL "$url/SHA256SUMS" -o "$tmp/SHA256SUMS"
(
    cd "$tmp"
    grep "  $package\$" SHA256SUMS > selected.sha256
    sha256sum -c selected.sha256
)
sudo apt-get install -y "$tmp/$package"
romancescript user-install
romancescript kde-select
romancescript doctor
echo "Instalado. Guarda tu trabajo, cierra sesión y vuelve a entrar."
