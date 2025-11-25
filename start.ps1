# 花費紀錄系統啟動腳本

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   花費紀錄系統 - 啟動中..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 檢查是否已安裝所需套件
Write-Host "檢查 Python 套件..." -ForegroundColor Yellow
$packages = @("Flask", "Flask-SQLAlchemy", "Werkzeug")
$needInstall = $false

foreach ($package in $packages) {
    $installed = python -m pip show $package 2>$null
    if (-not $installed) {
        Write-Host "  ✗ $package 未安裝" -ForegroundColor Red
        $needInstall = $true
    } else {
        Write-Host "  ✓ $package 已安裝" -ForegroundColor Green
    }
}

if ($needInstall) {
    Write-Host ""
    Write-Host "正在安裝所需套件..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
    Write-Host ""
}

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "啟動 Flask 應用程式..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "請在瀏覽器中訪問: http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host "按 Ctrl+C 停止伺服器" -ForegroundColor Yellow
Write-Host ""

# 啟動 Flask
python app.py
