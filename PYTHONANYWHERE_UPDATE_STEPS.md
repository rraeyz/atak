# PythonAnywhere Güncelleme Adımları

## 1. Kodu Güncelle (PythonAnywhere Console'da)

```bash
cd ~/atak
git pull origin master
```

**Beklenen çıktı:**
```
From https://github.com/rraeyz/atak
 * branch            master     -> FETCH_HEAD
Updating efdbf85..5e17a77
Fast-forward
 app/routes/events.py | 58 ++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 58 insertions(+)
```

## 2. Web Uygulamasını Yeniden Başlat

### Yöntem A: Web Interface (Daha Kolay)
1. PythonAnywhere Dashboard'a git: https://www.pythonanywhere.com/user/rraeyz/
2. **Web** sekmesine tıkla
3. **rraeyz.pythonanywhere.com** bul
4. Yeşil **"Reload"** butonuna tıkla
5. "Reloaded successfully" mesajını bekle

### Yöntem B: Console'dan
```bash
touch /var/www/rraeyz_pythonanywhere_com_wsgi.py
```

## 3. Test Et

### A. Yeni Kayıt (En İyisi)
1. Siteye git: https://rraeyz.pythonanywhere.com/etkinlikler
2. Henüz kaydolmadığın bir etkinliğe kayıt ol
3. "Kayıt Ol" butonuna tıkla

### B. Veya Mevcut Kaydı İptal Edip Yeniden Kayıt Ol
1. https://rraeyz.pythonanywhere.com/etkinlikler/kayitlarim
2. Bir etkinliği iptal et
3. Etkinlik sayfasına geri dön
4. Tekrar kayıt ol

## 4. Logları Kontrol Et

```bash
tail -50 /var/log/rraeyz.pythonanywhere.com.error.log | grep -A 5 "QR Kod"
```

**Beklenen çıktı:**
```
🔧 QR Kod Debug:
  Code: ATAK-20251019154500-xxxxx
  Image Path: uploads/qr_codes/event_X_user_Y_timestamp.png
✅ QR kod veritabanına kaydedildi: uploads/qr_codes/...
```

## 5. Sorun Çözme

### Eğer hala debug log yok:
- Web uygulaması reload edilmemiş olabilir → Adım 2'yi tekrar yap
- Eski kod çalışıyor olabilir → `git log -1` ile son commit'i kontrol et

### Eğer debug log var ama path yanlış:
- Bana log çıktısını gönder, düzelteceğim

### Eğer debug log var ve path doğru ama 404 hatası:
- Template sorunu, qr_code.html'i inceleyeceğim
