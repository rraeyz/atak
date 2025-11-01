"""
Veritabanına hierarchy_level kolonu ekle
"""
import sqlite3
import os

# Olası veritabanı yolları
possible_paths = [
    'instance/atak.db',
    '/home/rraeyz/atak/instance/atak.db',
    '/home/rraeyz/mysite/instance/atak.db',
    'atak.db',
    '/tmp/atak.db',
]

# Veritabanını bul
db_path = None
for path in possible_paths:
    if os.path.exists(path):
        db_path = path
        print(f"✓ Veritabanı bulundu: {db_path}")
        break

if not db_path:
    print("❌ Veritabanı bulunamadı!")
    print("\nManuel olarak veritabanı yolunu belirtin:")
    print("Python konsolunda şunu çalıştırın:")
    print("  from run import app")
    print("  with app.app_context():")
    print("      print(app.config['SQLALCHEMY_DATABASE_URI'])")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Kolonu ekle
try:
    cursor.execute('ALTER TABLE roles ADD COLUMN hierarchy_level INTEGER DEFAULT 0')
    conn.commit()
    print("✅ hierarchy_level kolonu eklendi!")
except sqlite3.OperationalError as e:
    if 'duplicate column' in str(e).lower():
        print("✓ Kolon zaten mevcut")
    else:
        print(f"❌ Hata: {e}")
        exit(1)

# Rolleri güncelle
updates = [
    ('root', 100),
    ('admin', 50),
    ('moderator', 30),
    ('editor', 20),
    ('member', 10),
]

for role_name, level in updates:
    cursor.execute('UPDATE roles SET hierarchy_level = ? WHERE name = ?', (level, role_name))
    if cursor.rowcount > 0:
        print(f"✓ {role_name}: {level}")

# Diğer rolleri 5 yap
cursor.execute('UPDATE roles SET hierarchy_level = 5 WHERE hierarchy_level = 0')
print(f"✓ Diğer roller: 5")

conn.commit()
conn.close()

print("\n✅ Veritabanı güncellendi!")
print("\nWeb app'i reload etmeyi unutma!")
