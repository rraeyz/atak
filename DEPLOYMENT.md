# Deployment Guide - ATAK Kulübü

## 🚀 Render.com ile Ücretsiz Deployment

### Adım 1: GitHub'a Yükle
```bash
cd c:\Users\rraey\OneDrive\Desktop\Projeler\atak
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<username>/atak.git
git push -u origin main
```

### Adım 2: Render.com'a Bağla
1. https://render.com → Kayıt ol (GitHub ile)
2. "New" → "Blueprint"
3. GitHub repo seç → `atak`
4. `render.yaml` otomatik algılanır
5. "Create New Resources" → Bekle (5-10 dakika)
6. Hazır! ✅

**URL:** `https://atak-kulubu.onrender.com`

### Adım 3: Custom Domain Bağla (Opsiyonel)
1. Render dashboard → Settings → Custom Domains
2. Domain adınızı girin: `atakkulubu.com`
3. DNS kayıtlarını Poyraz Hosting'de ayarla:
   - CNAME: `www` → `atak-kulubu.onrender.com`
   - ALIAS: `@` → `atak-kulubu.onrender.com`

---

## 🌟 PythonAnywhere ile Deployment

### Adım 1: Hesap Oluştur
1. https://www.pythonanywhere.com → Sign up
2. Beginner account (ücretsiz)

### Adım 2: Kod Yükle
```bash
# PythonAnywhere Bash Console
git clone https://github.com/<username>/atak.git
cd atak
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Adım 3: Web App Ayarla
1. Web tab → Add a new web app
2. Manual configuration → Python 3.11
3. Virtual environment: `/home/<username>/atak/venv`
4. WSGI file düzenle:

```python
import sys
path = '/home/<username>/atak'
if path not in sys.path:
    sys.path.append(path)

from run import app as application
```

5. Reload web app
6. URL: `https://<username>.pythonanywhere.com`

### Adım 4: Database Setup
```bash
cd ~/atak
source venv/bin/activate
flask init-db
flask seed-db
```

---

## 💰 Maliyet Karşılaştırması

| Platform | Ücretsiz | Ücretli | Domain | Database |
|----------|----------|---------|--------|----------|
| **Render.com** | ✅ (750 saat/ay) | $7/ay | ✅ Ücretsiz | ✅ PostgreSQL |
| **PythonAnywhere** | ✅ (sınırlı) | $5/ay | 💰 Ücretli planda | ✅ MySQL |
| **Heroku** | ❌ (artık yok) | $5/ay | ✅ Ücretsiz | ✅ PostgreSQL |
| **Vercel** | ✅ | $20/ay | ✅ Ücretsiz | ⚠️ Serverless |
| **Railway** | ✅ ($5 kredi) | $5/ay | ✅ Ücretsiz | ✅ PostgreSQL |

---

## 🎯 ÖNERİM

### **Başlangıç İçin:**
1. **Render.com** (tamamen ücretsiz, kolay)
   - Proje GitHub'a → Render'a bağla → Bitti!
   - 15 dk hareketsizlikten sonra uyur (ilk istek 30sn sürer)

### **Profesyonel İçin:**
1. **Domain:** Poyraz Hosting (.com.tr = ~50 TL/yıl)
2. **Hosting:** PythonAnywhere ($5/ay = ~150 TL/ay)
   - Hızlı, Türkiye'den iyi erişim
   - Custom domain bağlanır

### **En Ucuz:**
1. **Render.com** (ücretsiz) + **Freenom** domain (ücretsiz .tk, .ml)
2. Toplam: **0 TL/ay** 🎉

---

## 📝 Deployment Öncesi Checklist

- [ ] `SECRET_KEY` güçlü bir şifre olmalı
- [ ] `DEBUG = False` production'da
- [ ] Database production için (PostgreSQL/MySQL)
- [ ] Static files için CDN (opsiyonel)
- [ ] HTTPS aktif (render/pythonanywhere otomatik verir)
- [ ] Environment variables ayarla
- [ ] Backup planı

---

## 🆘 Sorun Giderme

### "Application Error" hatası:
```bash
# Render logs kontrol et
heroku logs --tail  # Heroku için
```

### Database bağlantı hatası:
```bash
# Environment variables kontrol et
echo $DATABASE_URL
```

### Static files yüklenmiyor:
```python
# config.py
SEND_FILE_MAX_AGE_DEFAULT = 0  # Development
# Production'da nginx kullan
```

---

**🎉 Başarılar!** Sorularınız için her zaman buradayım!
