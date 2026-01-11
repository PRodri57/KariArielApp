param(
  [Parameter(Mandatory = $true)][string]$HostIp,
  [int]$Port = 5173,
  [int]$ApiPort = 8000
)

if (-not $env:VITE_API_BASE_URL) {
  $env:VITE_API_BASE_URL = "http://${HostIp}:${ApiPort}"
}
if (-not $env:VITE_USE_MOCKS) {
  $env:VITE_USE_MOCKS = "false"
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Resolve-Path (Join-Path $scriptDir "..")
Set-Location (Join-Path $rootDir "Frontend")

Write-Host "Starting frontend on 0.0.0.0:$Port"
Write-Host "VITE_API_BASE_URL=$env:VITE_API_BASE_URL"

if (-not (Test-Path (Join-Path $rootDir "Frontend\node_modules\.bin\vite"))) {
  Write-Error "Falta node_modules/.bin/vite. Ejecuta: (cd Frontend; npm install)"
  Write-Error "Nota: el paquete Python 'vite' no sirve para el frontend."
  exit 1
}

$viteJs = Join-Path $rootDir "Frontend\node_modules\vite\bin\vite.js"
if ((Test-Path $viteJs) -and (Get-Command node -ErrorAction SilentlyContinue)) {
  node $viteJs --host 0.0.0.0 --port $Port
} elseif (Get-Command npm -ErrorAction SilentlyContinue) {
  npm run dev -- --host 0.0.0.0 --port $Port
} else {
  Write-Error "No se encontro npm en PATH."
  exit 1
}
