Write-Host "🚀 Building ClawdBot Control Panel..." -ForegroundColor Cyan

# Create dist directory if it doesn't exist
if (-not (Test-Path "dist")) {
    New-Item -ItemType Directory -Force -Path "dist" | Out-Null
}

# Run Nuitka build
python -m nuitka `
    --mode=onefile `
    --enable-plugin=pyqt6 `
    --windows-console-mode=disable `
    --windows-icon-from-ico=assets/clawdbot.png `
    --assume-yes-for-downloads `
    --output-dir=dist `
    --output-file="ClawdBot-Control-Panel" `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Build complete! Executable is in dist/ClawdBot-Control-Panel.exe" -ForegroundColor Green
} else {
    Write-Host "`n❌ Build failed!" -ForegroundColor Red
}
