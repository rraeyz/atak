"""
Admin rolüne 'view_event_reports' iznini ekle
Çalıştırmak için: python add_report_permission.py
"""

from app import create_app, db
from app.models import Permission, Role

def add_report_permission():
    """Admin rolüne etkinlik raporu görüntüleme iznini ekle"""
    app = create_app()
    
    with app.app_context():
        print("Root rolü ve izni kontrol ediliyor...")
        
        # Root rolünü bul
        admin_role = Role.query.filter_by(name='root').first()
        if not admin_role:
            print("❌ Root rolü bulunamadı!")
            return
        
        print(f"✓ Root rolü bulundu: {admin_role.display_name}")
        
        # view_event_reports iznini bul
        report_permission = Permission.query.filter_by(name='view_event_reports').first()
        if not report_permission:
            print("❌ 'view_event_reports' izni bulunamadı!")
            print("Önce 'python init_permissions.py' komutunu çalıştırın.")
            return
        
        print(f"✓ İzin bulundu: {report_permission.display_name}")
        
        # İzin zaten var mı kontrol et
        if report_permission in admin_role.permissions:
            print("✓ İzin zaten Admin rolünde mevcut!")
        else:
            # İzni ekle
            admin_role.permissions.append(report_permission)
            db.session.commit()
            print("✅ 'Etkinlik Raporları' izni Admin rolüne eklendi!")
        
        print("\n" + "="*50)
        print("İŞLEM TAMAMLANDI!")
        print("="*50)
        print("\nAdmin kullanıcısı artık etkinlik raporlarını görüntüleyebilir.")
        print("Sayfayı yenileyip tekrar deneyin: /admin/etkinlikler/{id}/rapor")
        print()

if __name__ == '__main__':
    add_report_permission()
