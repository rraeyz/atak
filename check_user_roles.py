"""
Kullanıcı rollerini kontrol et
"""
from app import create_app, db
from app.models import User, Role

app = create_app()

with app.app_context():
    print("=" * 70)
    print("KULLANICI ROL KONTROLÜ")
    print("=" * 70)
    
    users = User.query.all()
    
    for user in users:
        print(f"\n👤 {user.username} ({user.email})")
        print(f"   Aktif: {user.is_active} | Onaylı: {user.is_approved}")
        
        if user.roles:
            print(f"   Roller:")
            for role in user.roles:
                print(f"     - {role.display_name} (seviye: {role.hierarchy_level})")
            
            highest = user.get_highest_role_level()
            print(f"   ⭐ En yüksek seviye: {highest}")
            
            # Root kontrolü
            if user.has_role('root'):
                print(f"   👑 ROOT KULLANICI")
        else:
            print(f"   ⚠️  Rolü yok!")
    
    print("\n" + "=" * 70)
