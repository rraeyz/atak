"""
Rollerin mevcut durumunu kontrol et
"""
from app import create_app, db
from app.models import Role

app = create_app()

with app.app_context():
    print("=" * 60)
    print("MEVCUT ROLLER VE SEVİYELER")
    print("=" * 60)
    
    roles = Role.query.order_by(Role.hierarchy_level.desc()).all()
    
    for role in roles:
        print(f"{role.display_name:20} | Seviye: {role.hierarchy_level:3} | Sistem: {role.is_system}")
    
    print("\n" + "=" * 60)
    print("GEREKLİ OLMASI GEREKEN:")
    print("=" * 60)
    print("Root               | Seviye: 100")
    print("Yönetici           | Seviye:  50")
    print("Moderatör          | Seviye:  30")
    print("İçerik Üreticisi   | Seviye:  20")
    print("Üye                | Seviye:  10")
