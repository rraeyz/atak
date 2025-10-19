#!/usr/bin/env python3
"""
QR Kod Template Test - Gerçek URL'leri görmek için
PythonAnywhere console'da çalıştır: python3 test_qr_url.py
"""

from app import create_app
from app.models import QRCode
from flask import url_for

app = create_app()

with app.app_context():
    print("=" * 60)
    print("QR KOD URL TEST")
    print("=" * 60)
    
    qr_codes = QRCode.query.order_by(QRCode.id.desc()).limit(3).all()
    
    for qr in qr_codes:
        print(f"\n🎫 QR ID: {qr.id}")
        print(f"   Path (DB): {qr.qr_image_path}")
        
        # url_for ile gerçek URL
        try:
            url = url_for('static', filename=qr.qr_image_path, _external=False)
            print(f"   URL (url_for): {url}")
            
            # Tam URL
            full_url = url_for('static', filename=qr.qr_image_path, _external=True)
            print(f"   Full URL: {full_url}")
        except Exception as e:
            print(f"   ❌ URL Hatası: {e}")
        
        # Dosya kontrolü
        import os
        file_path = os.path.join('app', 'static', qr.qr_image_path)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ Dosya var ({size} bytes): {file_path}")
        else:
            print(f"   ❌ Dosya yok: {file_path}")
    
    print("\n" + "=" * 60)
    print("BEKLENEN vs GERÇEK")
    print("=" * 60)
    
    if qr_codes:
        qr = qr_codes[0]
        print(f"\nDB Path: {qr.qr_image_path}")
        print(f"Beklenen URL: /static/uploads/qr_codes/event_X_user_Y_timestamp.png")
        print(f"Gerçek URL: {url_for('static', filename=qr.qr_image_path)}")
        
        # Browser'ın istediği vs. Flask'ın sunduğu
        print(f"\nBrowser isteği (hata): /static/event_1_user_1_20251019143221.png")
        print(f"Flask sunması gereken: /static/uploads/qr_codes/event_1_user_1_20251019143221.png")
    
    print("\n" + "=" * 60)
