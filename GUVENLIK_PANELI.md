# 🛡️ Güvenlik Paneli - Kullanım Kılavuzu

## 📋 Özellikler

Güvenlik rolüne sahip kullanıcılar için özel bir panel sistemi eklendi. Bu sistem sayede etkinlik girişlerinde QR kod okutma işlemleri kolayca yapılabilir.

---

## 🎯 Erişim Noktaları

Güvenlik rolüne sahip kullanıcılar **4 farklı yerden** güvenlik paneline erişebilir:

### 1️⃣ **Navbar (Üst Menü)**
- Giriş yaptıktan sonra üst menüde "🛡️ Güvenlik Paneli" linki görünür
- Tüm sayfalarda erişilebilir
- Aktif sayfa renklendirmesi ile kolay navigasyon

### 2️⃣ **Ana Sayfa**
- Ana sayfanın üst kısmında öne çıkan bir kart ile gösterilir
- Mavi gradient tasarım ile dikkat çeker
- "Panele Git" butonu ile direkt erişim

### 3️⃣ **Profil Sayfası**
- Profil sayfasında "İstatistikler" kartının altında özel kart
- Detaylı açıklama ve kullanım bilgisi içerir
- Büyük buton ile kolay erişim

### 4️⃣ **Direkt URL**
- `http://localhost:5000/guvenlik`
- Tarayıcı favorilerine eklenebilir

---

## ⚙️ Kurulum ve Yapılandırma

### 1. İzinleri ve Rolü Oluşturma

```powershell
cd atak
python init_permissions.py
```

Bu script:
- ✅ Tüm izinleri oluşturur (açıklamalarıyla)
- ✅ `scan_qr_codes` iznini ekler
- ✅ `view_event_reports` iznini ekler
- ✅ **Güvenlik** rolünü otomatik oluşturur
- ✅ Güvenlik rolüne QR okuma iznini verir

### 2. Uygulamayı Başlatma

```powershell
flask run
```

### 3. Kullanıcıya Güvenlik Rolü Verme

1. Admin olarak giriş yapın: `http://localhost:5000/admin`
2. **Kullanıcılar** sayfasına gidin
3. Güvenlik görevlisi olacak kullanıcıyı seçin
4. "**Rol Ekle**" bölümünden "**Güvenlik**" rolünü seçin
5. "**Ekle**" butonuna tıklayın

---

## 🚀 Kullanım

### Güvenlik Paneli Ana Sayfa (`/guvenlik`)

- **Bugünün Etkinlikleri**: Aktif etkinlikler listesi
- **İstatistikler**: 
  - Toplam kayıtlı kişi sayısı
  - Giriş yapan kişi sayısı
  - Katılım oranı (%)
- **QR Okut Butonu**: Her etkinlik için QR okutma sayfasına yönlendirme

### QR Kod Okutma Sayfası (`/guvenlik/etkinlik/<id>`)

- **Kamera ile Okutma**: Otomatik QR kod tarama
- **Manuel Giriş**: QR kodu elle yazma seçeneği
- **Canlı İstatistikler**: Anlık güncellenen sayaçlar
- **Son Girişler**: Gerçek zamanlı giriş listesi
- **Ses Efektleri**: Başarılı/hatalı okutma için ses

---

## 🎨 Tasarım Özellikleri

### Navbar Linki
```html
<i class="fas fa-shield-alt"></i> Güvenlik Paneli
```
- Kalkan ikonu ile görsel vurgu
- Aktif sayfa vurgulama

### Ana Sayfa Kartı
- Cyan gradient arkaplan
- 4rem (64px) büyük emoji ikonu
- Responsive tasarım
- Hover animasyonları

### Profil Sayfası Kartı
- Özel gradient border (2px cyan)
- Detaylı açıklama metni
- Tam genişlik buton (100%)
- Büyük font boyutu (1.1rem)

---

## 🔐 Güvenlik ve İzinler

### `scan_qr_codes` İzni
- **Açıklama**: "Etkinlik girişlerinde QR kod okuma yetkisi"
- **Verdiği Yetkiler**:
  - `/guvenlik` sayfasına erişim
  - `/guvenlik/etkinlik/<id>` QR okutma sayfasına erişim
  - `/guvenlik/qr-okut` API endpoint'ine erişim
  - `/guvenlik/manuel-giris/<id>` manuel giriş yetkisi

### `view_event_reports` İzni (Admin için)
- **Açıklama**: "Etkinlik katılım raporlarını görüntüleme yetkisi"
- **Verdiği Yetkiler**:
  - `/admin/etkinlikler/<id>/rapor` sayfa erişimi
  - `/admin/etkinlikler/<id>/rapor/indir` CSV indirme

---

## 📊 Veritabanı Yapısı

### `permissions` Tablosu
```sql
INSERT INTO permissions (name, display_name, description)
VALUES 
  ('scan_qr_codes', 'QR Kod Okuma', 'Etkinlik girişlerinde QR kod okuma yetkisi'),
  ('view_event_reports', 'Etkinlik Raporları', 'Etkinlik katılım raporlarını görüntüleme yetkisi');
```

### `roles` Tablosu
```sql
INSERT INTO roles (name, display_name, description, is_system)
VALUES ('security', 'Güvenlik', 'Etkinlik girişlerinde QR kod okuma yetkisi olan personel', 0);
```

### `role_permissions` İlişkisi
```sql
-- Güvenlik rolüne scan_qr_codes iznini ver
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id 
FROM roles r, permissions p 
WHERE r.name = 'security' AND p.name = 'scan_qr_codes';
```

---

## 🧪 Test Senaryosu

### 1. Tam Senaryo Testi

```
1. Admin ile giriş yap
2. python init_permissions.py çalıştır
3. Kullanıcılar > Kullanıcı seç > Güvenlik rolü ver
4. O kullanıcı ile giriş yap
5. Üst menüde "Güvenlik Paneli" linkini gör ✓
6. Ana sayfada mavi kartı gör ✓
7. Profil sayfasında güvenlik kartını gör ✓
8. Güvenlik paneline git (/guvenlik) ✓
9. Bugünün etkinliklerini gör ✓
10. Bir etkinliğin "QR Okut" butonuna tıkla ✓
11. Kamera açılsın ✓
12. QR kod okut veya manuel gir ✓
13. Başarılı giriş mesajı al ✓
14. İstatistiklerin güncellendiğini gör ✓
```

### 2. Yetki Kontrolü Testi

```
1. Normal kullanıcı ile giriş yap
2. Üst menüde "Güvenlik Paneli" linki GÖRMEME ✓
3. Ana sayfada kart GÖRMEME ✓
4. Profil sayfasında kart GÖRMEME ✓
5. /guvenlik URL'sine git → 403 Forbidden ✓
```

---

## 📱 Mobil Uyumluluk

- **Navbar**: Hamburger menüde görünür
- **Ana Sayfa Kartı**: Responsive grid (mobilde tek sütun)
- **Profil Kartı**: Tam genişlik, mobil optimize
- **QR Scanner**: Mobil kamera desteği
- **Touch-friendly**: Büyük butonlar ve kolay dokunma

---

## 🎯 Sonuç

Bu sistem sayede:
- ✅ Güvenlik görevlileri 4 farklı yerden panele erişebilir
- ✅ URL elle girilmesine gerek kalmaz
- ✅ Görsel olarak öne çıkan tasarım
- ✅ Kolay ve hızlı kullanım
- ✅ Mobil uyumlu
- ✅ Yetki bazlı erişim kontrolü

---

## 🛠️ Teknik Detaylar

### Değiştirilen Dosyalar

1. **app/templates/base.html** (Satır 38-42)
   - Navbar'a güvenlik paneli linki eklendi

2. **app/templates/auth/profile.html** (Satır 109-127)
   - Profil sayfasına güvenlik kartı eklendi

3. **app/templates/main/index.html** (Satır 32-51)
   - Ana sayfaya güvenlik quick access kartı eklendi

4. **app/routes/security.py** (Satır 9, 18-21)
   - Eager loading eklendi (performans optimizasyonu)

5. **app/templates/security/index.html** (Satır 63-75)
   - `.count()` metodu ile düzeltme yapıldı

6. **init_permissions.py** (YENİ)
   - İzinleri ve rolleri otomatik oluşturan script

---

## 💡 İpuçları

- Güvenlik paneli linkini tarayıcı favorilerine ekleyin
- Mobil cihazda ana ekrana kısayol olarak ekleyin
- QR okutma sayfasını tam ekran modda kullanın
- Karanlık ortamlarda ekran parlaklığını artırın

---

**Hazırlayan**: GitHub Copilot  
**Tarih**: 19 Ekim 2025  
**Versiyon**: 1.0
