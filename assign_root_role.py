"""
rraeyz kullanıcısına admin (root) rolünü ata
"""
from app import create_app, db
from app.models import User, Role

app = create_app()

with app.app_context():
    print("=" * 60)
    print("KULLANICIYA ADMİN (ROOT) ROLÜ ATANIYOR")
    print("=" * 60 + "\n")
    
    # Kullanıcıyı bul
    user = User.query.filter_by(username='rraeyz').first()
    if not user:
        print("❌ Kullanıcı bulunamadı!")
        exit()
    
    print(f"Kullanıcı: {user.username}")
    print(f"Mevcut roller: {', '.join([r.display_name for r in user.roles])}\n")
    
    # Admin rolünü bul
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        print("❌ admin rolü bulunamadı!")
        exit()
    
    # Admin rolü zaten var mı?
    if admin_role in user.roles:
        print(f"✓ {admin_role.display_name} rolü zaten mevcut!")
    else:
        # Admin rolünü ekle
        user.roles.append(admin_role)
        db.session.commit()
        print(f"✅ {admin_role.display_name} rolü eklendi!")
    
    print("\n" + "=" * 60)
    print("Güncellenmiş roller:")
    user = User.query.filter_by(username='rraeyz').first()
    for role in user.roles:
        print(f"  - {role.display_name} (Seviye {role.hierarchy_level})")
    print("=" * 60)
