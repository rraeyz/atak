"""
İzinleri ve rolleri başlatma scripti
Çalıştırmak için: python init_permissions.py
"""

from app import create_app, db
from app.models import Permission, Role

def init_permissions():
    """Tüm izinleri oluştur veya güncelle"""
    app = create_app()
    
    with app.app_context():
        # İzin tanımları (name, display_name, description)
        permissions_data = [
            # Admin İzinleri
            ('admin_access', 'Admin Erişimi', 'Admin paneline erişim yetkisi'),
            ('manage_users', 'Kullanıcı Yönetimi', 'Kullanıcıları görüntüleme, düzenleme ve silme yetkisi'),
            ('manage_roles', 'Rol Yönetimi', 'Rolleri ve izinleri yönetme yetkisi'),
            ('manage_settings', 'Ayar Yönetimi', 'Site ayarlarını düzenleme yetkisi'),
            
            # İçerik İzinleri
            ('create_post', 'Yazı Oluşturma', 'Blog yazıları oluşturma yetkisi'),
            ('edit_post', 'Yazı Düzenleme', 'Tüm yazıları düzenleme yetkisi'),
            ('delete_post', 'Yazı Silme', 'Yazıları silme yetkisi'),
            ('moderate_comments', 'Yorum Moderasyonu', 'Yorumları onaylama ve silme yetkisi'),
            
            # Etkinlik İzinleri
            ('create_event', 'Etkinlik Oluşturma', 'Yeni etkinlik oluşturma yetkisi'),
            ('edit_event', 'Etkinlik Düzenleme', 'Etkinlikleri düzenleme yetkisi'),
            ('delete_event', 'Etkinlik Silme', 'Etkinlikleri silme yetkisi'),
            ('manage_registrations', 'Kayıt Yönetimi', 'Etkinlik kayıtlarını yönetme yetkisi'),
            
            # QR Kod İzinleri
            ('scan_qr_codes', 'QR Kod Okuma', 'Etkinlik girişlerinde QR kod okuma yetkisi'),
            ('view_event_reports', 'Etkinlik Raporları', 'Etkinlik katılım raporlarını görüntüleme yetkisi'),
        ]
        
        print("İzinler oluşturuluyor/güncelleniyor...")
        
        for name, display_name, description in permissions_data:
            permission = Permission.query.filter_by(name=name).first()
            
            if permission:
                # Varsa güncelle
                permission.display_name = display_name
                permission.description = description
                print(f"  ✓ Güncellendi: {display_name}")
            else:
                # Yoksa oluştur
                permission = Permission(
                    name=name,
                    display_name=display_name,
                    description=description
                )
                db.session.add(permission)
                print(f"  + Oluşturuldu: {display_name}")
        
        db.session.commit()
        print("\n✅ Tüm izinler başarıyla oluşturuldu/güncellendi!")
        
        # Güvenlik rolünü oluştur
        print("\nGüvenlik rolü kontrol ediliyor...")
        security_role = Role.query.filter_by(name='security').first()
        
        if not security_role:
            security_role = Role(
                name='security',
                display_name='Güvenlik',
                description='Etkinlik girişlerinde QR kod okuma yetkisi olan personel',
                is_system=False
            )
            db.session.add(security_role)
            print("  + Güvenlik rolü oluşturuldu")
            
            # QR kod okuma iznini ekle
            scan_permission = Permission.query.filter_by(name='scan_qr_codes').first()
            if scan_permission:
                security_role.permissions.append(scan_permission)
                print("  + 'QR Kod Okuma' izni eklendi")
            
            db.session.commit()
            print("✅ Güvenlik rolü hazır!")
        else:
            print("  ✓ Güvenlik rolü zaten mevcut")
            
            # QR kod izni var mı kontrol et
            scan_permission = Permission.query.filter_by(name='scan_qr_codes').first()
            if scan_permission and scan_permission not in security_role.permissions:
                security_role.permissions.append(scan_permission)
                db.session.commit()
                print("  + 'QR Kod Okuma' izni eklendi")
        
        print("\n" + "="*50)
        print("TÜM İŞLEMLER TAMAMLANDI!")
        print("="*50)
        print("\n📝 Yapılacaklar:")
        print("1. Admin paneline giriş yapın: http://localhost:5000/admin")
        print("2. Roller sayfasına gidin: http://localhost:5000/admin/roller")
        print("3. 'Güvenlik' rolünü görmelisiniz")
        print("4. Kullanıcılar sayfasından bir kullanıcıya 'Güvenlik' rolünü verin")
        print("5. O kullanıcı ile /guvenlik sayfasına erişebilirsiniz")
        print("\n")

if __name__ == '__main__':
    init_permissions()
