#!/usr/bin/env python3
"""
Yeni oluşturulan kullanıcının QR kodunu kontrol et
PythonAnywhere console'da çalıştır: python3 debug_new_user_qr.py
"""

from app import create_app, db
from app.models import QRCode, EventRegistration, User
import os

app = create_app()

with app.app_context():
    print("=" * 60)
    print("YENİ KULLANICI QR KOD DEBUG")
    print("=" * 60)
    
    # En son oluşturulan kullanıcıyı bul
    latest_user = User.query.order_by(User.id.desc()).first()
    
    print(f"\n👤 En Son Kullanıcı:")
    print(f"   ID: {latest_user.id}")
    print(f"   Kullanıcı Adı: {latest_user.username}")
    print(f"   Ad Soyad: {latest_user.first_name} {latest_user.last_name}")
    print(f"   Email: {latest_user.email}")
    print(f"   Oluşturulma: {latest_user.created_at}")
    
    # Bu kullanıcının kayıtlarını bul
    registrations = EventRegistration.query.filter_by(user_id=latest_user.id).all()
    
    print(f"\n📋 Kayıtlar: {len(registrations)} adet")
    
    if not registrations:
        print("   ⚠️  Bu kullanıcının hiç etkinlik kaydı yok!")
        print("\n💡 Önce bir etkinliğe kayıt yapmalısınız.")
    else:
        for reg in registrations:
            print(f"\n   📌 Kayıt ID: {reg.id}")
            print(f"      Etkinlik ID: {reg.event_id}")
            print(f"      Durum: {reg.status}")
            print(f"      Kayıt Tarihi: {reg.registered_at}")
            
            # Bu kayıt için QR kod var mı?
            qr = QRCode.query.filter_by(registration_id=reg.id).first()
            
            if qr:
                print(f"      ✅ QR Kod VAR:")
                print(f"         QR ID: {qr.id}")
                print(f"         Code: {qr.code}")
                print(f"         Path (DB): {qr.qr_image_path}")
                
                # Dosya var mı?
                file_path = os.path.join('app', 'static', qr.qr_image_path)
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    print(f"         ✅ Dosya VAR ({size} bytes)")
                else:
                    print(f"         ❌ DOSYA YOK!")
                    print(f"            Aranan: {file_path}")
            else:
                print(f"      ❌ QR KOD YOK!")
    
    # Son 5 kayıt ve QR kodlarını göster
    print("\n" + "=" * 60)
    print("SON 5 KAYIT VE QR KODLARI")
    print("=" * 60)
    
    recent_regs = EventRegistration.query.order_by(EventRegistration.id.desc()).limit(5).all()
    
    for reg in recent_regs:
        user = User.query.get(reg.user_id)
        qr = QRCode.query.filter_by(registration_id=reg.id).first()
        
        print(f"\n📌 Kayıt #{reg.id} - {user.username}")
        print(f"   Etkinlik: {reg.event_id} | Durum: {reg.status}")
        
        if qr:
            file_path = os.path.join('app', 'static', qr.qr_image_path)
            file_exists = "✅" if os.path.exists(file_path) else "❌"
            print(f"   QR: {file_exists} {qr.qr_image_path}")
        else:
            print(f"   QR: ❌ YOK")
    
    print("\n" + "=" * 60)
