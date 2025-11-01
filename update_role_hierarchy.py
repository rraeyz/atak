"""
Rol hiyerarşisi güncelleme scripti
Root rolü için hierarchy_level = 100
Admin için 50, diğerleri için uygun seviyeler
"""
from app import create_app, db
from app.models import Role

app = create_app()

with app.app_context():
    print("Rollerin hiyerarşi seviyeleri güncelleniyor...")
    
    # Root rolü
    root_role = Role.query.filter_by(name='root').first()
    if root_role:
        root_role.hierarchy_level = 100
        print(f"✓ {root_role.display_name}: Seviye 100 (Root)")
    
    # Manager rolü (Yönetici)
    manager_role = Role.query.filter_by(name='manager').first()
    if manager_role:
        manager_role.hierarchy_level = 50
        print(f"✓ {manager_role.display_name}: Seviye 50 (Yönetici)")
    
    # Moderatör rolü
    moderator_role = Role.query.filter_by(name='moderator').first()
    if moderator_role:
        moderator_role.hierarchy_level = 30
        print(f"✓ {moderator_role.display_name}: Seviye 30 (Moderatör)")
    
    # Editor rolü
    editor_role = Role.query.filter_by(name='editor').first()
    if editor_role:
        editor_role.hierarchy_level = 20
        print(f"✓ {editor_role.display_name}: Seviye 20 (Editör)")
    
    # Member rolü
    member_role = Role.query.filter_by(name='member').first()
    if member_role:
        member_role.hierarchy_level = 10
        print(f"✓ {member_role.display_name}: Seviye 10 (Üye)")
    
    # Diğer tüm rolleri 5 yap
    other_roles = Role.query.filter(
        ~Role.name.in_(['root', 'admin', 'moderator', 'editor', 'member'])
    ).all()
    
    for role in other_roles:
        if not role.hierarchy_level or role.hierarchy_level == 0:
            role.hierarchy_level = 5
            print(f"✓ {role.display_name}: Seviye 5 (Diğer)")
    
    db.session.commit()
    print("\n✅ Rol hiyerarşisi başarıyla güncellendi!")
    print("\nHiyerarşi Yapısı:")
    print("100 - Root (Süper Yönetici)")
    print("50  - Admin (Yönetici)")
    print("30  - Moderatör")
    print("20  - Editör")
    print("10  - Üye")
    print("5   - Diğer roller")
