#!/usr/bin/env python3
"""
QR Kod Oluşturma Testi - Yeni kullanıcı senaryosunu test et
PythonAnywhere console'da çalıştır: python3 test_qr_creation.py
"""

from app import create_app
from app.utils.qr_generator import generate_event_qr_code
import os

app = create_app()

with app.app_context():
    print("=" * 60)
    print("QR KOD OLUŞTURMA TESTİ")
    print("=" * 60)
    
    # Test verileri
    test_user_id = 999
    test_event_id = 999
    test_registration_id = 999
    
    print("\n📝 Test Senaryosu:")
    print(f"   User ID: {test_user_id}")
    print(f"   Event ID: {test_event_id}")
    print(f"   Registration ID: {test_registration_id}")
    
    print("\n🔧 QR Kod Oluşturuluyor...")
    
    try:
        # QR kod oluştur
        code, qr_image_path = generate_event_qr_code(
            test_user_id,
            test_event_id,
            test_registration_id
        )
        
        print(f"\n✅ QR Kod Başarıyla Oluşturuldu!")
        print(f"   Code: {code}")
        print(f"   Path: {qr_image_path}")
        
        # Dosya kontrolü
        full_path = os.path.join('app', 'static', qr_image_path)
        
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            print(f"\n✅ Dosya Kaydedildi:")
            print(f"   Konum: {full_path}")
            print(f"   Boyut: {file_size} bytes")
            
            # Test dosyasını temizle
            os.remove(full_path)
            print(f"\n🗑️  Test dosyası temizlendi")
        else:
            print(f"\n❌ HATA: Dosya bulunamadı!")
            print(f"   Beklenen konum: {full_path}")
        
        print("\n" + "=" * 60)
        print("TEST SONUCU: ✅ BAŞARILI")
        print("=" * 60)
        print("\n💡 Yeni kullanıcılar sorunsuz QR kod oluşturabilir!")
        
    except Exception as e:
        print(f"\n❌ HATA OLUŞTU!")
        print(f"   Hata: {e}")
        
        import traceback
        print("\n📋 Detaylı Hata:")
        traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("TEST SONUCU: ❌ BAŞARISIZ")
        print("=" * 60)
        print("\n⚠️  QR kod oluşturma sistemi düzeltilmeli!")
