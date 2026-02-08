# Build and create installer
Write-Host "Building EmojiPad..." -ForegroundColor Green

# Step 1: Install dependencies
Write-Host "`nStep 1: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
pip install pyinstaller

# Step 2: Build executable
Write-Host "`nStep 2: Building executable with PyInstaller..." -ForegroundColor Yellow
pyinstaller EmojiPad.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Executable built successfully!" -ForegroundColor Green
    Write-Host "Location: dist\EmojiPad.exe" -ForegroundColor Cyan
} else {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

# Step 3: Create installer (if Inno Setup is installed)
$innoPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (Test-Path $innoPath) {
    Write-Host "`nStep 3: Creating installer with Inno Setup..." -ForegroundColor Yellow
    & $innoPath installer.iss
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Installer created successfully!" -ForegroundColor Green
        Write-Host "Location: installer_output\EmojiPad_Setup.exe" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Installer creation failed!" -ForegroundColor Red
    }
} else {
    Write-Host "`nInno Setup not found. Skipping installer creation." -ForegroundColor Yellow
    Write-Host "Download from: https://jrsoftware.org/isdl.php" -ForegroundColor Cyan
}

Write-Host "`n✨ Build process complete!" -ForegroundColor Green
