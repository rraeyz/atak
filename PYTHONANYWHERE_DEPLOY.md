# PythonAnywhere Deployment Rehberi

## 1. Hesap Oluşturun
- https://www.pythonanywhere.com adresine gidin
- Ücretsiz hesap oluşturun (Beginner account)

## 2. Dosyaları Yükleyin

### Yöntem A: Git ile (Önerilen)
```bash
# PythonAnywhere Bash Console'da:
cd ~
git clone https://github.com/KULLANICI_ADINIZ/atak-kulubu.git
cd atak-kulubu
```

### Yöntem B: Manuel Upload
- Files sekmesine gidin
- Dosyaları tek tek yükleyin (zip olarak da yükleyebilirsiniz)

## 3. Virtual Environment Oluşturun
```bash
mkvirtualenv --python=/usr/bin/python3.11 atak-env
pip install -r requirements.txt
```

## 4. Web App Oluşturun
- Web sekmesine gidin
- "Add a new web app"
- Manual configuration → Python 3.11
- Virtualenv path: `/home/KULLANICI_ADINIZ/.virtualenvs/atak-env`

## 5. WSGI Dosyasını Düzenleyin
Web sekmesinde WSGI configuration file linkine tıklayın:

```python
import sys
import os

# Proje yolunu ekle
path = '/home/KULLANICI_ADINIZ/atak-kulubu'
if path not in sys.path:
    sys.path.insert(0, path)

# Flask app'i import et
from run import app as application
```

## 6. Static Files Ayarları
Web sekmesinde Static files bölümüne:

| URL | Directory |
|-----|-----------|
| /static/ | /home/KULLANICI_ADINIZ/atak-kulubu/app/static/ |

## 7. Veritabanını Başlatın
Bash console'da:
```bash
cd ~/atak-kulubu
python seed_database.py
```

## 8. Reload!
Web sekmesinde yeşil "Reload" butonuna basın

Siteniz hazır: `https://KULLANICI_ADINIZ.pythonanywhere.com`
