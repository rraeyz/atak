"""
Rolleri düzelt - Doğru seviyeleri ata
Mevcut roller: admin, manager, moderator, content_creator, security, member
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
    
    # root rolü - en yüksek
    root_role = Role.query.filter_by(name='root').first()
    if root_role:
        root_role.hierarchy_level = 100
        print(f"✓ {root_role.display_name}: 100 (Root)")
    else:
        print("⚠️  root rolü bulunamadı!")
    
    # manager rolü (Yönetici)
    manager_role = Role.query.filter_by(name='manager').first()
    if manager_role:
        manager_role.hierarchy_level = 50
        print(f"✓ {manager_role.display_name}: 50 (Yönetici)")
    else:
        print("⚠️  manager rolü bulunamadı!")
    
    # moderator rolü (Moderatör)
    moderator_role = Role.query.filter_by(name='moderator').first()
    if moderator_role:
        moderator_role.hierarchy_level = 30
        print(f"✓ {moderator_role.display_name}: 30 (Moderatör)")
    else:
        print("⚠️  moderator rolü bulunamadı!")
    
    # content_creator rolü (İçerik Üreticisi)
    content_creator_role = Role.query.filter_by(name='content_creator').first()
    if content_creator_role:
        content_creator_role.hierarchy_level = 20
        print(f"✓ {content_creator_role.display_name}: 20 (İçerik Üreticisi)")
    else:
        print("⚠️  content_creator rolü bulunamadı!")
    
    # security rolü (Güvenlik)
    security_role = Role.query.filter_by(name='security').first()
    if security_role:
        security_role.hierarchy_level = 15
        print(f"✓ {security_role.display_name}: 15 (Güvenlik)")
    else:
        print("⚠️  security rolü bulunamadı!")
    
    # member rolü (Üye)
    member_role = Role.query.filter_by(name='member').first()
    if member_role:
        member_role.hierarchy_level = 10
        print(f"✓ {member_role.display_name}: 10 (Üye)")
    else:
        print("⚠️  member rolü bulunamadı!")
    
    # Diğer tüm rolleri 5 yap
    other_count = 0
    for role in all_roles:
        if role.name not in ['root', 'manager', 'moderator', 'content_creator', 'member', 'security']:
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
