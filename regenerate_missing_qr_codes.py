#!/usr/bin/env python3
"""
Veritabanında var ama dosya sistemi eksik olan QR kodları yeniden oluştur
PythonAnywhere console'da çalıştır: python3 regenerate_missing_qr_codes.py
"""

from app import create_app, db
from app.models import QRCode
import qrcode
import os

app = create_app()

with app.app_context():
    print("=" * 60)
    print("EKSİK QR KOD DOSYALARINI YENİDEN OLUŞTUR")
    print("=" * 60)
    
    all_qr_codes = QRCode.query.all()
    
    missing_count = 0
    regenerated_count = 0
    already_exists_count = 0
    
    for qr_code in all_qr_codes:
        # Flask app root kullanarak mutlak yol oluştur
        from flask import current_app
        file_path = os.path.join(current_app.root_path, 'static', qr_code.qr_image_path)
        
        if not os.path.exists(file_path):
            missing_count += 1
            print(f"\n❌ Eksik: {qr_code.qr_image_path}")
            print(f"   QR ID: {qr_code.id}")
            print(f"   Code: {qr_code.code}")
            
            # QR kodu yeniden oluştur
            try:
                # QR kod nesnesini oluştur
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_code.code)
                qr.make(fit=True)
                
                # Görüntüyü oluştur
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Klasörü oluştur (yoksa)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Dosyayı kaydet
                img.save(file_path)
                
                print(f"   ✅ Yeniden oluşturuldu: {file_path}")
                regenerated_count += 1
                
                # Dosya boyutunu kontrol et
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    print(f"   📁 Dosya boyutu: {size} bytes")
            except Exception as e:
                print(f"   ❌ HATA: {e}")
                import traceback
                traceback.print_exc()
        else:
            already_exists_count += 1
    
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    print(f"Toplam QR Kod: {len(all_qr_codes)}")
    print(f"✅ Zaten var: {already_exists_count}")
    print(f"❌ Eksikti: {missing_count}")
    print(f"🔧 Yeniden oluşturuldu: {regenerated_count}")
    
    if regenerated_count > 0:
        print("\n🎉 Tüm eksik QR kodlar başarıyla oluşturuldu!")
        print("\nŞimdi siteyi tarayıcıda yenileyin ve QR kodlarınız görünmeli!")
    elif missing_count == 0:
        print("\n✅ Tüm QR kod dosyaları zaten mevcut!")
    else:
        print("\n⚠️ Bazı QR kodlar oluşturulamadı. Lütfen hataları kontrol edin.")
    
    print("=" * 60)
