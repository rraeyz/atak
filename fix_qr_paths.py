"""
QR kod yollarını düzelt
Çalıştırma: python fix_qr_paths.py
"""
import sys
import os

# Proje dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import QRCode

app = create_app()

with app.app_context():
    # Tüm QR kodları al
    qr_codes = QRCode.query.all()
    
    updated = 0
    for qr in qr_codes:
        if qr.qr_image_path and qr.qr_image_path.startswith('/static/'):
            # /static/uploads/... → uploads/...
            new_path = qr.qr_image_path.replace('/static/', '')
            qr.qr_image_path = new_path
            updated += 1
            print(f"QR {qr.id}: {qr.qr_image_path}")
    
    if updated > 0:
        db.session.commit()
        print(f"\n✅ {updated} QR kod yolu güncellendi!")
    else:
        print("Güncellenecek QR kod yolu bulunamadı.")
