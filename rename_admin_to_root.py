"""
admin rolünün adını root olarak değiştir
Template'lerde has_role('root') kontrolü var, rol adı uyuşmuyor
"""
from app import create_app, db
from app.models import Role

app = create_app()

with app.app_context():
    print("=" * 60)
    print("ADMİN ROLÜNÜ ROOT OLARAK YENİDEN ADLANDIRMA")
    print("=" * 60 + "\n")
    
    # admin rolünü bul
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        print("❌ admin rolü bulunamadı!")
        exit()
    
    print(f"Mevcut rol:")
    print(f"  İsim: {admin_role.name}")
    print(f"  Görünen Ad: {admin_role.display_name}")
    print(f"  Seviye: {admin_role.hierarchy_level}")
    
    # root adında rol var mı kontrol et
    existing_root = Role.query.filter_by(name='root').first()
    if existing_root:
        print("\n⚠️  'root' adında bir rol zaten var!")
        print(f"  İsim: {existing_root.name}")
        print(f"  Görünen Ad: {existing_root.display_name}")
        print(f"  Seviye: {existing_root.hierarchy_level}")
        print("\nÖnce bu rolü silmeniz veya yeniden adlandırmanız gerekiyor.")
        exit()
    
    # İsmi değiştir
    admin_role.name = 'root'
    admin_role.display_name = 'Root'
    admin_role.hierarchy_level = 100  # Emin olmak için
    
    db.session.commit()
    
    print("\n✅ ROL BAŞARIYLA GÜNCELLENDİ!")
    print("\nGüncellenmiş rol:")
    print(f"  İsim: {admin_role.name}")
    print(f"  Görünen Ad: {admin_role.display_name}")
    print(f"  Seviye: {admin_role.hierarchy_level}")
    
    print("\n" + "=" * 60)
    print("ℹ️  Şimdi siteden çıkış yapıp tekrar giriş yapın!")
    print("=" * 60)
