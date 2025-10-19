# 🌌 ATAK Kulübü - Astronomi ve Uzay Bilimleri Kulübü Web Sitesi

Modern, responsive ve kullanıcı dostu bir astronomi kulübü web sitesi. Flask framework'ü ile geliştirilmiştir.

## ✨ Özellikler

### 🎨 Genel Özellikler
- **Astronomi Temalı Tasarım**: Dark mode, yıldız animasyonları, uzay temalı renkler
- **Responsive Design**: Mobil, tablet ve masaüstü uyumlu
- **Modern UI/UX**: Smooth animasyonlar, interaktif elementler

### 👥 Kullanıcı Sistemi
- Kullanıcı kaydı ve girişi
- Profil yönetimi (avatar, bio, bilgiler)
- Rol tabanlı yetkilendirme (Admin, Content Creator, Member)
- Admin onay sistemi
- Şifre değiştirme

### 🗓️ Etkinlik Yönetimi
- Etkinlik oluşturma ve düzenleme
- Etkinliklere kayıt olma
- Katılımcı limit kontrolü
- Etkinlik onay sistemi
- Geçmiş ve yaklaşan etkinlik filtreleme

### 📝 Blog Sistemi
- Blog yazısı oluşturma ve yayınlama
- Yorum yapma sistemi
- Görsel yükleme desteği
- Markdown formatı desteği

### ⚙️ Admin Paneli
- Dashboard ile istatistikler
- Kullanıcı yönetimi ve onaylama
- Rol ve yetki yönetimi
- Etkinlik yönetimi
- Blog yazısı yönetimi
- Site ayarları
- İletişim mesajları yönetimi

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- pip (Python package manager)

### Adım 1: Depoyu Klonlayın veya İndirin

```bash
cd c:\Users\rraey\OneDrive\Desktop\Projeler\atak
```

### Adım 2: Virtual Environment Oluşturun (Önerilen)

```bash
python -m venv venv
```

### Adım 3: Virtual Environment'ı Aktifleştirin

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

### Adım 4: Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 5: Veritabanını Oluşturun

```bash
flask init-db
```

### Adım 6: Demo Verileri Ekleyin (Opsiyonel)

```bash
flask seed-db
```

Bu komut şu demo kullanıcıları oluşturur:
- **Admin**: `admin` / `admin123`
- **İçerik Oluşturucu**: `ayse_yildiz` / `password123`
- **Üye**: `mehmet_ay` / `password123`

### Adım 7: Uygulamayı Çalıştırın

**Development Mode:**
```bash
python run.py
```

Uygulama `http://127.0.0.1:5000` adresinde çalışacaktır.

## 📁 Proje Yapısı

```
atak/
├── app/
│   ├── __init__.py              # Uygulama factory
│   ├── models.py                # Veritabanı modelleri
│   ├── forms.py                 # WTForms formları
│   ├── routes/
│   │   ├── main.py              # Ana sayfa route'ları
│   │   ├── auth.py              # Authentication route'ları
│   │   ├── events.py            # Etkinlik route'ları
│   │   ├── blog.py              # Blog route'ları
│   │   └── admin.py             # Admin panel route'ları
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Ana stil dosyası
│   │   ├── js/
│   │   │   └── main.js          # JavaScript dosyası
│   │   └── uploads/             # Yüklenen dosyalar
│   ├── templates/
│   │   ├── base.html            # Ana template
│   │   ├── main/                # Ana sayfa template'leri
│   │   ├── auth/                # Authentication template'leri
│   │   ├── events/              # Etkinlik template'leri
│   │   ├── blog/                # Blog template'leri
│   │   ├── admin/               # Admin template'leri
│   │   └── errors/              # Hata sayfaları
│   └── utils/
│       ├── decorators.py        # Custom decorator'lar
│       ├── helpers.py           # Yardımcı fonksiyonlar
│       └── template_filters.py  # Jinja2 filtreleri
├── config.py                    # Konfigürasyon ayarları
├── run.py                       # Uygulama başlatıcı
├── requirements.txt             # Python bağımlılıkları
└── README.md                    # Bu dosya
```

## 🔧 Konfigürasyon

### Ortam Değişkenleri

`.env` dosyası oluşturup şu değişkenleri ekleyebilirsiniz:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///atak.db

# E-posta Ayarları (Opsiyonel)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Veritabanı

Varsayılan olarak SQLite kullanılır. Production'da PostgreSQL veya MySQL kullanımı önerilir.

## 👤 Demo Kullanıcılar

`flask seed-db` komutuyla oluşturulan demo kullanıcılar:

| Kullanıcı Adı | Şifre | Rol |
|---------------|-------|-----|
| admin | admin123 | Administrator |
| ayse_yildiz | password123 | Content Creator |
| mehmet_ay | password123 | Member |

## 🛠️ Geliştirme

### Flask CLI Komutları

```bash
# Veritabanını başlat
flask init-db

# Demo verileri ekle
flask seed-db

# Development server başlat
flask run

# Debug mode ile çalıştır
flask run --debug
```

### Yeni Özellik Ekleme

1. `app/models.py` - Yeni model ekleyin
2. `app/routes/` - Yeni route oluşturun
3. `app/templates/` - Template'leri ekleyin
4. `app/forms.py` - Form'ları tanımlayın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için iletişim formunu kullanabilirsiniz.

## 🎯 Özellik Roadmap

- [ ] E-posta bildirimleri
- [ ] SMS entegrasyonu
- [ ] Sosyal medya entegrasyonu
- [ ] Gelişmiş arama
- [ ] Kullanıcı rozetleri
- [ ] Etkinlik takvimi görünümü
- [ ] Export/Import özellikleri
- [ ] API endpoint'leri

---

**🌌 ATAK Kulübü** - Yıldızlara ulaşmak için birlikte yükseliyoruz! 🚀
