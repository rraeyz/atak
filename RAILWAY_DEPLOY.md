# Railway Deployment Rehberi

## 1. Hesap Oluşturun
- https://railway.app adresine gidin
- GitHub ile giriş yapın

## 2. Yeni Proje Oluşturun
- "New Project" → "Deploy from GitHub repo"
- Repo'nuzu seçin

## 3. Environment Variables Ekleyin
Settings → Variables:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

## 4. Deploy!
Railway otomatik olarak:
- requirements.txt'den paketleri yükler
- Gunicorn ile uygulamayı başlatır
- HTTPS sertifikası sağlar

Siteniz hazır: `https://atak-kulubu.up.railway.app`

## Özel Domain Bağlama
- Settings → Domains → Add Custom Domain
- DNS kayıtlarını güncelleyin
