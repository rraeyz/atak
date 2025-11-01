"""
Veritabanına hierarchy_level kolonu ekle
"""
import sqlite3
import os

# Veritabanı yolu - PythonAnywhere'de bu path'i değiştir
db_path = 'instance/atak.db'

if not os.path.exists(db_path):
    print(f"❌ Veritabanı bulunamadı: {db_path}")
    print("PythonAnywhere'de path'i kontrol et!")
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
