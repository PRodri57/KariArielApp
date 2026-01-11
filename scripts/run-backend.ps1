param(
  [Parameter(Mandatory = $true)][string]$HostIp,
  [int]$Port = 8000,
  [string]$CorsOrigins
)

$defaultCors = "http://localhost:5173,http://127.0.0.1:5173,http://$($HostIp):5173"
if ($CorsOrigins) {
  $env:CORS_ORIGINS = $CorsOrigins
} else {
  $env:CORS_ORIGINS = $defaultCors
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Resolve-Path (Join-Path $scriptDir "..")
Set-Location (Join-Path $rootDir "Backend")

Write-Host "Starting backend on 0.0.0.0:$Port"
Write-Host "CORS_ORIGINS=$env:CORS_ORIGINS"

$venvPython = Join-Path $rootDir ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
  & $venvPython -m uvicorn App.main:app --host 0.0.0.0 --port $Port
} elseif (Get-Command uvicorn -ErrorAction SilentlyContinue) {
  uvicorn App.main:app --host 0.0.0.0 --port $Port
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  python -m uvicorn App.main:app --host 0.0.0.0 --port $Port
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
  python3 -m uvicorn App.main:app --host 0.0.0.0 --port $Port
} else {
  Write-Error "No se encontro uvicorn ni python en PATH."
  exit 1
}
