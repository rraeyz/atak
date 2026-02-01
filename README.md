# 🌌 ATAK Kulübü - Astronomi ve Uzay Bilimleri Kulübü Web Sitesi

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Modern, responsive ve kullanıcı dostu bir astronomi kulübü yönetim platformu.

[Demo](#) · [Dokümantasyon](GUVENLIK_PANELI.md) · [Katkıda Bulun](#-katkıda-bulunma)

</div>

---

## ✨ Özellikler

### 🎨 Platform Özellikleri
- **🌙 Astronomi Temalı Tasarım:** Dark mode, yıldız animasyonları, uzay temalı renkler
- **📱 Responsive Design:** Mobil, tablet ve masaüstü tam uyumlu
- **✨ Modern UI/UX:** Smooth animasyonlar, interaktif elementler
- **🔒 Güvenlik:** CSRF koruması, güvenli session yönetimi

### 👥 Kullanıcı Yönetimi
- **Kayıt ve Giriş:** E-posta bazlı kimlik doğrulama
- **Profil Sistemi:** Avatar, bio, sosyal medya linkleri
- **Rol Tabanlı Yetkilendirme:** Admin, İçerik Oluşturucu, Üye, Güvenlik
- **Onay Sistemi:** Admin onaylı üyelik
- **Şifre Yönetimi:** Güvenli şifre değiştirme

### 🗓️ Etkinlik Yönetimi
- **Etkinlik Oluşturma:** Detaylı etkinlik bilgileri ve görseller
- **Kayıt Sistemi:** Katılımcı limiti ve otomatik QR kod oluşturma
- **QR Check-in:** Güvenlik paneli ile QR kod okutma
- **Onay Sistemi:** Admin tarafından etkinlik kontrolü
- **Filtreleme:** Geçmiş/yaklaşan/iptal etkinlikleri görüntüleme

### 📝 Blog ve İçerik
- **Blog Yazıları:** Markdown desteği ile zengin içerik
- **Yorum Sistemi:** Kullanıcı etkileşimi
- **Görsel Yönetimi:** Dosya yükleme ve düzenleme
- **Kategori/Etiket:** İçerik organizasyonu

### ⚙️ Admin Paneli
- **📊 Dashboard:** Gerçek zamanlı istatistikler ve grafikler
- **👥 Kullanıcı Yönetimi:** Onaylama, rol atama, yetki kontrolü
- **📅 Etkinlik Yönetimi:** Onay, düzenleme, silme
- **📝 İçerik Yönetimi:** Blog yazıları ve yorumlar
- **⚙️ Site Ayarları:** Genel konfigürasyon
- **📧 Mesaj Yönetimi:** İletişim formundan gelen mesajlar

### 🛡️ Güvenlik Paneli
- **QR Kod Okutma:** Etkinlik girişlerinde QR kontrol
- **Canlı İstatistikler:** Anlık katılımcı takibi
- **Manuel Giriş:** Alternatif kod girişi
- **Ses Efektleri:** Görsel ve işitsel geri bildirim
- **Detaylı Raporlama:** Etkinlik katılım raporları

> 📖 Detaylı güvenlik paneli kullanımı için [GUVENLIK_PANELI.md](GUVENLIK_PANELI.md) dosyasına bakın.

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.8 veya üzeri
- pip (Python package manager)

### Kurulum

**1. Projeyi Klonlayın:**
```bash
git clone https://github.com/rraeyz/atak.git
cd atak
```

**2. Virtual Environment Oluşturun:**
```bash
python -m venv venv
```

**3. Virtual Environment'ı Aktifleştirin:**

Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

Windows (CMD):
```cmd
venv\Scripts\activate.bat
```

Linux/Mac:
```bash
source venv/bin/activate
```

**4. Bağımlılıkları Yükleyin:**
```bash
pip install -r requirements.txt
```

**5. Veritabanını Başlatın:**
```bash
flask init-db
```

**6. Demo Verileri Ekleyin (Opsiyonel):**
```bash
flask seed-db
```

Bu komut demo kullanıcılar oluşturur:
- **Admin:** `admin` / `admin123`
- **İçerik Oluşturucu:** `ayse_yildiz` / `password123`
- **Üye:** `mehmet_ay` / `password123`

**7. Uygulamayı Çalıştırın:**
```bash
python run.py
```

🎉 Uygulama `http://127.0.0.1:5000` adresinde çalışacaktır!

## 📁 Proje Yapısı

```
atak/
├── app/
│   ├── __init__.py              # Uygulama factory
│   ├── models.py                # Veritabanı modelleri (User, Event, Blog, Role)
│   ├── forms.py                 # WTForms formları
│   ├── routes/
│   │   ├── main.py              # Ana sayfa ve genel route'lar
│   │   ├── auth.py              # Kimlik doğrulama (login, register)
│   │   ├── events.py            # Etkinlik yönetimi
│   │   ├── blog.py              # Blog sistemi
│   │   ├── admin.py             # Admin paneli
│   │   └── security.py          # Güvenlik paneli (QR kod)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Ana stil dosyası (dark theme)
│   │   ├── js/
│   │   │   └── main.js          # JavaScript (QR scanner, animations)
│   │   └── uploads/             # Kullanıcı yüklemeleri
│   ├── templates/
│   │   ├── base.html            # Ana template (navbar, footer)
│   │   ├── main/                # Ana sayfa template'leri
│   │   ├── auth/                # Giriş/kayıt template'leri
│   │   ├── events/              # Etkinlik template'leri
│   │   ├── blog/                # Blog template'leri
│   │   ├── admin/               # Admin paneli template'leri
│   │   ├── security/            # Güvenlik paneli template'leri
│   │   └── errors/              # 404, 500 hata sayfaları
│   └── utils/
│       ├── decorators.py        # Custom decorator'lar (role_required)
│       ├── helpers.py           # Yardımcı fonksiyonlar
│       └── template_filters.py  # Jinja2 filtreleri
├── migrations/                  # Alembic veritabanı migration'ları
├── config.py                    # Uygulama konfigürasyonu
├── run.py                       # Uygulama başlatıcı
├── requirements.txt             # Python bağımlılıkları
├── README.md                    # Bu dosya
└── GUVENLIK_PANELI.md          # Güvenlik paneli dokümantasyonu
```

## 🛠️ Teknoloji Stack

### Backend
- **Framework:** Flask 3.0+
- **Database:** SQLAlchemy (SQLite/PostgreSQL/MySQL)
- **Migration:** Flask-Migrate (Alembic)
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF
- **Security:** Werkzeug (password hashing)

### Frontend
- **Template Engine:** Jinja2
- **CSS Framework:** Bootstrap 5
- **Icons:** Font Awesome
- **Animations:** Custom CSS3 animations
- **QR Code:** jsQR library

### Features
- **QR Code Generation:** qrcode library
- **File Upload:** Flask file handling
- **Session Management:** Flask-Session
- **CSRF Protection:** Flask-WTF

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

Sorularınız için issue açabilirsiniz.

## 🙏 Teşekkürler

Bu proje aşağıdaki harika açık kaynak projeler sayesinde mümkün oldu:

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Font Awesome](https://fontawesome.com/) - Icon library
- [jsQR](https://github.com/cozmo/jsQR) - QR code scanner
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**

**🌌 ATAK Kulübü** - Yıldızlara ulaşmak için birlikte yükseliyoruz! 🚀

Made with ❤️ by [rraeyz](https://github.com/rraeyz)

</div>
