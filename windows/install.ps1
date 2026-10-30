# RomanceScript para Windows: asistente de descarga.
# Validación estática; no se ha compilado ni probado en Windows.
param(
    [string]$Source = "https://github.com/Emilianowv/RomanceScript/releases/latest/download/RomanceScript.klc",
    [string]$OutFile = "$env:USERPROFILE\Downloads\RomanceScript.klc"
)

$ErrorActionPreference = 'Stop'

Write-Host "Descargando RomanceScript.klc ..."
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutFile) | Out-Null
Invoke-WebRequest -Uri $Source -OutFile $OutFile

Write-Host ""
Write-Host "Descargado: $OutFile"
Write-Host ""
Write-Host "Siguiente paso: abre el archivo en Microsoft Keyboard Layout Creator"
Write-Host "para validar el diseno y compilar la DLL y el paquete de instalacion."
Write-Host "MSKLC: https://www.microsoft.com/en-us/download/details.aspx?id=102134"
