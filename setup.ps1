# ATAK Kulübü - Kurulum Scripti
# Bu script projeyi otomatik olarak kurar

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  ATAK Kulübü Kurulum Scripti" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Virtual environment kontrolü
if (Test-Path "venv") {
    Write-Host "[!] Virtual environment zaten mevcut." -ForegroundColor Yellow
    $response = Read-Host "Yeniden oluşturmak ister misiniz? (e/h)"
    if ($response -eq "e") {
        Write-Host "[*] Eski virtual environment siliniyor..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force venv
        Write-Host "[+] Virtual environment oluşturuluyor..." -ForegroundColor Green
        python -m venv venv
    }
} else {
    Write-Host "[+] Virtual environment oluşturuluyor..." -ForegroundColor Green
    python -m venv venv
}

Write-Host ""
Write-Host "[+] Virtual environment aktifleştiriliyor..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "[+] Gerekli paketler yükleniyor..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host ""
Write-Host "[+] Veritabanı oluşturuluyor..." -ForegroundColor Green
flask init-db

Write-Host ""
$seed = Read-Host "Demo verileri eklemek ister misiniz? (e/h)"
if ($seed -eq "e") {
    Write-Host "[+] Demo verileri ekleniyor..." -ForegroundColor Green
    flask seed-db
    Write-Host ""
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "  Demo Kullanıcı Bilgileri:" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "Admin:" -ForegroundColor Yellow
    Write-Host "  Kullanıcı: admin" -ForegroundColor White
    Write-Host "  Şifre: admin123" -ForegroundColor White
    Write-Host ""
    Write-Host "İçerik Oluşturucu:" -ForegroundColor Yellow
    Write-Host "  Kullanıcı: ayse_yildiz" -ForegroundColor White
    Write-Host "  Şifre: password123" -ForegroundColor White
    Write-Host ""
    Write-Host "Üye:" -ForegroundColor Yellow
    Write-Host "  Kullanıcı: mehmet_ay" -ForegroundColor White
    Write-Host "  Şifre: password123" -ForegroundColor White
    Write-Host "================================" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "  Kurulum Tamamlandı!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Uygulamayı başlatmak için:" -ForegroundColor Yellow
Write-Host "  python run.py" -ForegroundColor White
Write-Host ""
Write-Host "Veya:" -ForegroundColor Yellow
Write-Host "  flask run" -ForegroundColor White
Write-Host ""
Write-Host "Uygulama http://127.0.0.1:5000 adresinde çalışacaktır." -ForegroundColor Cyan
Write-Host ""

$run = Read-Host "Uygulamayı şimdi başlatmak ister misiniz? (e/h)"
if ($run -eq "e") {
    Write-Host ""
    Write-Host "[+] Uygulama başlatılıyor..." -ForegroundColor Green
    Write-Host "[*] Durdurmak için CTRL+C yapın" -ForegroundColor Yellow
    Write-Host ""
    python run.py
}
