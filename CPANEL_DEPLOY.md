# cPanel / Geleneksel Hosting Deployment

## Gereksinimler
- Python 3.11+ desteği olan hosting
- SSH erişimi
- Python app setup özelliği

## Türkiye'deki Uygun Hostingler
1. **NİGDE Bilişim** - Python desteği var
2. **HostRaptor** - Python app setup
3. **Turhost** - SSH + Python
4. **Radore** - VPS önerilir

## Deployment Adımları

### 1. Dosyaları Yükleyin
FTP ile tüm dosyaları `public_html/atak` klasörüne yükleyin

### 2. Python App Setup (cPanel)
- Setup Python App bölümüne gidin
- Python version: 3.11
- Application root: `/home/KULLANICI/atak`
- Application URL: `atak.siteniz.com`
- Application startup file: `run.py`
- Application Entry point: `app`

### 3. Requirements Yükleyin
Terminal'de:
```bash
cd ~/atak
source /home/KULLANICI/virtualenv/atak/3.11/bin/activate
pip install -r requirements.txt
```

### 4. .htaccess Oluşturun
`public_html/.htaccess`:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /passenger_wsgi.py [L]
```

### 5. passenger_wsgi.py
`public_html/passenger_wsgi.py`:
```python
import sys
import os

INTERP = "/home/KULLANICI/virtualenv/atak/3.11/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '/home/KULLANICI/atak')

from run import app as application
```

### 6. Veritabanı
```bash
cd ~/atak
python seed_database.py
```

### 7. Restart
cPanel'de Python App'i restart edin

## Önemli Notlar
- SQLite yerine MySQL kullanın (production için)
- Static files için ayrı klasör yapılandırın
- Log dosyalarını kontrol edin: `~/logs/`
