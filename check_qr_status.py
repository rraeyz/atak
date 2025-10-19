#!/usr/bin/env python3
"""
PythonAnywhere'de QR Kod Durumunu Kontrol Et
Bu scripti PythonAnywhere console'da çalıştır: python3 check_qr_status.py
"""

from app import create_app, db
from app.models import QRCode, EventRegistration, Event, User

app = create_app()

with app.app_context():
    print("=" * 60)
    print("QR KOD DURUM RAPORU")
    print("=" * 60)
    
    # Toplam QR kodları
    total_qr = QRCode.query.count()
    print(f"\n📊 Toplam QR Kod: {total_qr}")
    
    # Toplam kayıtlar
    total_reg = EventRegistration.query.count()
    print(f"📊 Toplam Kayıt: {total_reg}")
    
    # QR kodu olmayan kayıtlar
    registrations = EventRegistration.query.all()
    missing_qr = []
    
    for reg in registrations:
        qr = QRCode.query.filter_by(registration_id=reg.id).first()
        if not qr and reg.status != 'cancelled':
            missing_qr.append(reg)
    
    print(f"\n⚠️  QR Kodu Olmayan Aktif Kayıt: {len(missing_qr)}")
    
    if missing_qr:
        print("\n" + "=" * 60)
        print("QR KODU EKSİK KAYITLAR:")
        print("=" * 60)
        for reg in missing_qr:
            user = User.query.get(reg.user_id)
            event = Event.query.get(reg.event_id)
            print(f"\n📌 Kayıt ID: {reg.id}")
            print(f"   Kullanıcı: {user.get_full_name()} (ID: {user.id})")
            print(f"   Etkinlik: {event.title} (ID: {event.id})")
            print(f"   Durum: {reg.status}")
            print(f"   Kayıt Tarihi: {reg.registered_at}")
    
    # Son 5 QR kodu
    print("\n" + "=" * 60)
    print("SON 5 QR KOD:")
    print("=" * 60)
    recent_qrs = QRCode.query.order_by(QRCode.id.desc()).limit(5).all()
    
    for qr in recent_qrs:
        reg = EventRegistration.query.get(qr.registration_id)
        event = Event.query.get(qr.event_id)
        user = User.query.get(qr.user_id)
        
        print(f"\n🎫 QR ID: {qr.id}")
        print(f"   Kod: {qr.code}")
        print(f"   Path: {qr.qr_image_path}")
        print(f"   Kullanıcı: {user.get_full_name()}")
        print(f"   Etkinlik: {event.title}")
        print(f"   Oluşturulma: {qr.generated_at}")
    
    print("\n" + "=" * 60)
    print("PATH KONTROL")
    print("=" * 60)
    
    # Path formatını kontrol et
    all_qrs = QRCode.query.all()
    wrong_paths = []
    
    for qr in all_qrs:
        if qr.qr_image_path and not qr.qr_image_path.startswith('uploads/'):
            wrong_paths.append(qr)
    
    if wrong_paths:
        print(f"\n❌ Yanlış Path Formatı: {len(wrong_paths)} adet")
        for qr in wrong_paths:
            print(f"   ID {qr.id}: {qr.qr_image_path}")
    else:
        print("\n✅ Tüm QR kod pathları doğru formatta (uploads/qr_codes/...)")
    
    print("\n" + "=" * 60)
    print("DOSYA KONTROLÜ")
    print("=" * 60)
    
    import os
    qr_dir = os.path.join('app', 'static', 'uploads', 'qr_codes')
    
    if os.path.exists(qr_dir):
        files = os.listdir(qr_dir)
        print(f"\n📁 QR Kod Klasöründeki Dosya Sayısı: {len(files)}")
        
        if len(files) > 0:
            print("\nİlk 5 dosya:")
            for f in files[:5]:
                file_path = os.path.join(qr_dir, f)
                size = os.path.getsize(file_path)
                print(f"   {f} ({size} bytes)")
    else:
        print(f"\n❌ QR Kod klasörü bulunamadı: {qr_dir}")
    
    print("\n" + "=" * 60)
