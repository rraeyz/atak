"""QR kod resim yollarını düzelt"""
from app import create_app, db
from app.models import QRCode

app = create_app()

with app.app_context():
    # Tüm QR kodları al
    qr_codes = QRCode.query.all()
    
    updated = 0
    for qr in qr_codes:
        # Eğer yol sadece dosya adı ise (uploads/qr_codes/ içermiyor)
        if qr.qr_image_path and 'uploads/qr_codes/' not in qr.qr_image_path:
            # Dosya adını al
            filename = qr.qr_image_path.split('/')[-1]  # Son kısmı al
            
            # Doğru yolu oluştur
            new_path = f"uploads/qr_codes/{filename}"
            
            print(f"Düzeltiliyor: {qr.id}")
            print(f"  Eski: {qr.qr_image_path}")
            print(f"  Yeni: {new_path}")
            
            qr.qr_image_path = new_path
            updated += 1
    
    if updated > 0:
        db.session.commit()
        print(f"\n✅ {updated} QR kod yolu düzeltildi!")
    else:
        print("Düzeltilecek QR kod yolu bulunamadı.")
