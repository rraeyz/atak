# GitHub'a Proje Yükleme Rehberi

## Adım 1: Git Kurulumu
Eğer Git yüklü değilse: https://git-scm.com/download/win

## Adım 2: GitHub'da Yeni Repo Oluşturun
1. https://github.com adresine gidin
2. Sağ üstteki **+** → **New repository**
3. Repository name: `atak-kulubu` (veya istediğiniz isim)
4. Description: `Astronomi ve Uzay Bilimleri Kulübü Web Sitesi`
5. **Public** veya **Private** seçin
6. ❌ **Initialize this repository with a README** - İŞARETLEMEYİN
7. **Create repository** butonuna basın

## Adım 3: Proje Klasöründe Terminal Açın

PowerShell'de:
```powershell
cd C:\Users\rraey\OneDrive\Desktop\Projeler\atak
```

## Adım 4: Git Başlatın

```powershell
# Git repository başlat
git init

# Git kullanıcı bilgilerinizi ayarlayın (ilk kez ise)
git config --global user.name "İsminiz"
git config --global user.email "github@email.com"

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: ATAK Kulübü web sitesi"
```

## Adım 5: GitHub'a Bağlayın

GitHub'da oluşturduğunuz repo'nun sayfasında gösterilen komutları kullanın:

```powershell
# Remote ekle (URL'i kendi repo URL'inizle değiştirin)
git remote add origin https://github.com/KULLANICI_ADINIZ/atak-kulubu.git

# Ana branch'i main olarak ayarla
git branch -M main

# GitHub'a push et
git push -u origin main
```

## Adım 6: GitHub Kimlik Doğrulama

İlk push'ta GitHub şifrenizi isteyecek. Artık **Personal Access Token** kullanılıyor:

### Token Oluşturma:
1. GitHub → Settings (sağ üst profil) → Developer settings
2. Personal access tokens → Tokens (classic)
3. **Generate new token (classic)**
4. Note: `atak-kulubu-deploy`
5. Expiration: **No expiration** veya 90 days
6. Select scopes: ✅ **repo** (tüm repo checkbox'larını işaretle)
7. **Generate token**
8. 🔴 **Token'ı kopyalayın** (bir daha gösterilmeyecek!)

### Token ile Push:
```powershell
git push -u origin main
```
- Username: GitHub kullanıcı adınız
- Password: **Token'ı yapıştırın** (şifrenizi değil!)

## Adım 7: Token'ı Kaydedin (İsteğe Bağlı)

Her seferinde token girmemek için:

```powershell
git config credential.helper store
```

Bir sonraki push'ta token kaydedilecek.

## Adım 8: Doğrulayın

GitHub repo sayfanızı yenileyin - dosyalarınız orada olmalı! 🎉

---

## Gelecekte Değişiklik Yüklemek

```powershell
# Değişiklikleri ekle
git add .

# Commit yap
git commit -m "Yaptığınız değişikliğin açıklaması"

# GitHub'a yükle
git push
```

---

## Sorun Giderme

### "Author identity unknown" hatası:
```powershell
git config --global user.name "İsminiz"
git config --global user.email "email@example.com"
```

### "Permission denied" hatası:
Token'ınızın geçerli olduğundan emin olun.

### OneDrive senkronizasyon sorunu:
OneDrive klasöründen çıkarın:
```powershell
# Projeyi başka yere kopyalayın
xcopy /E /I C:\Users\rraey\OneDrive\Desktop\Projeler\atak C:\Projeler\atak
cd C:\Projeler\atak
git init
# ... devam edin
```

---

## Hızlı Komutlar

```powershell
# Proje klasörüne git
cd C:\Users\rraey\OneDrive\Desktop\Projeler\atak

# Git başlat ve yükle
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI_ADINIZ/atak-kulubu.git
git branch -M main
git push -u origin main
```

Hazır! 🚀
