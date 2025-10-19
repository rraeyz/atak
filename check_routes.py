"""Flask route'larını kontrol etmek için basit script"""
from app import create_app

app = create_app()

print("\n" + "="*80)
print("ETKİNLİK İLE İLGİLİ TÜM ROUTE'LAR:")
print("="*80)

with app.app_context():
    for rule in app.url_map.iter_rules():
        if 'etkinlik' in rule.rule or 'event' in rule.endpoint:
            print(f"\n📌 Endpoint: {rule.endpoint}")
            print(f"   URL: {rule.rule}")
            print(f"   Methods: {', '.join(rule.methods - {'HEAD', 'OPTIONS'})}")

print("\n" + "="*80)
