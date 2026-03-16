# start-dev.ps1 — Liga backend (Python) + frontend (Node) em janelas separadas
# Não requer admin. Roda do diretório raiz do projeto.

$root    = $PSScriptRoot
$nodeDir = "$env:LOCALAPPDATA\Programs\nodejs\node-v22.14.0-win-x64"

# ── Backend ──────────────────────────────────────────────────────────────────
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$root\backend'; Write-Host '=== Backend RAG (porta 8000) ===' -ForegroundColor Cyan; .\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"
)

# ── Frontend ─────────────────────────────────────────────────────────────────
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$root'; `$env:Path = '$nodeDir;' + `$env:Path; Write-Host '=== Frontend (porta 3000) ===' -ForegroundColor Green; pnpm exec tsx watch server/_core/index.ts"
)

Write-Host ""
Write-Host "Iniciando serviços..." -ForegroundColor Yellow
Write-Host "  Backend : http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Aguarde ~5s e abra http://localhost:3000 no browser."

Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"
