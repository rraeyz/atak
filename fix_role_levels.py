"""
Rolleri düzelt - Doğru seviyeleri ata
"""
from app import create_app, db
from app.models import Role

app = create_app()

with app.app_context():
    print("Rollerin seviyeleri güncelleniyor...\n")
    
    # Tüm rolleri listele
    all_roles = Role.query.all()
    print("Mevcut roller:")
    for r in all_roles:
        print(f"  - {r.name} ({r.display_name})")
    
    print("\n" + "=" * 60)
    
    # Root rolü (en yüksek)
    root_role = Role.query.filter_by(name='root').first()
    if root_role:
        root_role.hierarchy_level = 100
        print(f"✓ {root_role.display_name}: 100 (Root)")
    else:
        print("⚠️  Root rolü bulunamadı!")
    
    # Admin/Yönetici rolü
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role:
        admin_role.hierarchy_level = 50
        print(f"✓ {admin_role.display_name}: 50 (Yönetici)")
    else:
        print("⚠️  Admin rolü bulunamadı!")
    
    # Moderatör rolü
    moderator_role = Role.query.filter_by(name='moderator').first()
    if moderator_role:
        moderator_role.hierarchy_level = 30
        print(f"✓ {moderator_role.display_name}: 30 (Moderatör)")
    else:
        print("⚠️  Moderatör rolü bulunamadı!")
    
    # Editor/İçerik Üreticisi rolü
    editor_role = Role.query.filter_by(name='editor').first()
    if editor_role:
        editor_role.hierarchy_level = 20
        print(f"✓ {editor_role.display_name}: 20 (İçerik Üreticisi)")
    else:
        print("⚠️  Editor rolü bulunamadı!")
    
    # Member/Üye rolü
    member_role = Role.query.filter_by(name='member').first()
    if member_role:
        member_role.hierarchy_level = 10
        print(f"✓ {member_role.display_name}: 10 (Üye)")
    else:
        print("⚠️  Member rolü bulunamadı!")
    
    # Diğer tüm rolleri 5 yap
    other_count = 0
    for role in all_roles:
        if role.name not in ['root', 'admin', 'moderator', 'editor', 'member']:
            if not role.hierarchy_level or role.hierarchy_level == 0:
                role.hierarchy_level = 5
                other_count += 1
    
    if other_count > 0:
        print(f"✓ {other_count} diğer rol: 5")
    
    db.session.commit()
    
    print("\n" + "=" * 60)
    print("✅ GÜNCELLEME TAMAMLANDI!")
    print("=" * 60)
    
    # Doğrulama
    print("\nGüncellenmiş hali:")
    roles = Role.query.order_by(Role.hierarchy_level.desc()).all()
    for role in roles:
        print(f"  {role.display_name:25} → Seviye {role.hierarchy_level}")
