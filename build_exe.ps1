Write-Host "🚀 Building ClawdBot Control Panel..." -ForegroundColor Cyan

# Clean previous builds
Write-Host "🧹 Cleaning up previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Path "build" -Recurse -Force | Out-Null }
if (Test-Path "dist") { Remove-Item -Path "dist" -Recurse -Force | Out-Null }

# Create dist directory
New-Item -ItemType Directory -Force -Path "dist" | Out-Null

# Run PyInstaller build
uv run pyinstaller `
    --name "ClawdBot-Control-Panel" `
    --onefile `
    --windowed `
    --icon="assets/clawdbot.png" `
    --add-data="assets;assets" `
    --noconfirm `
    --clean `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Build complete! Executable is in dist/ClawdBot-Control-Panel.exe" -ForegroundColor Green
} else {
    Write-Host "`n❌ Build failed!" -ForegroundColor Red
}
