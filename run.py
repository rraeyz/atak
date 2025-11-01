from app import create_app, db
from app.models import User, Role, Permission, Event, Post, Comment, EventRegistration, SiteSetting, ContactMessage, Announcement

app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    """Shell context için modelleri ekle"""
    return dict(db=db, User=User, Role=Role, Permission=Permission, 
                Event=Event, Post=Post, Comment=Comment, 
                EventRegistration=EventRegistration, SiteSetting=SiteSetting,
                ContactMessage=ContactMessage)


@app.cli.command()
def init_db():
    """Veritabanını başlat"""
    db.create_all()
    print('✅ Veritabanı tabloları oluşturuldu.')


@app.cli.command()
def reset_db():
    """Veritabanını sıfırla ve yeniden oluştur"""
    db.drop_all()
    db.create_all()
    print('✅ Veritabanı sıfırlandı ve yeniden oluşturuldu.')


@app.cli.command()
def setup():
    """Veritabanını oluştur ve örnek verileri ekle"""
    print('🔄 Veritabanı oluşturuluyor...')
    db.create_all()
    print('✅ Veritabanı tabloları oluşturuldu.')
    
    print('🔄 Örnek veriler ekleniyor...')
    seed_db.callback()
    print('✅ Kurulum tamamlandı!')


@app.cli.command()
def seed_db():
    """Örnek verileri ekle"""
    from datetime import datetime, timedelta
    
    # Rolleri oluştur
    admin_role = Role(name='root', display_name='Root', 
                     description='Tüm yetkilere sahip sistem yöneticisi', is_system=True, hierarchy_level=100)
    manager_role = Role(name='manager', display_name='Yönetici',
                       description='Admin paneline erişimi ve tüm yetkileri olan yönetici', hierarchy_level=50)
    moderator_role = Role(name='moderator', display_name='Moderatör',
                         description='Yorumları ve içerikleri denetleyebilir', hierarchy_level=30)
    content_creator_role = Role(name='content_creator', display_name='İçerik Üreticisi',
                                description='Blog yazısı ve etkinlik paylaşabilir', hierarchy_level=20)
    security_role = Role(name='security', display_name='Güvenlik',
                        description='Etkinlik girişlerinde QR kod okutabilir', hierarchy_level=15)
    member_role = Role(name='member', display_name='Üye',
                      description='Standart kullanıcı', hierarchy_level=10)
    
    db.session.add_all([admin_role, manager_role, moderator_role, content_creator_role, security_role, member_role])
    
    # İzinleri oluştur
    permissions = [
        Permission(name='admin_access', display_name='Admin Paneline Erişim', category='admin'),
        Permission(name='manage_users', display_name='Kullanıcı Yönetimi', category='admin'),
        Permission(name='manage_roles', display_name='Rol Yönetimi', category='admin'),
        Permission(name='manage_settings', display_name='Site Ayarları', category='admin'),
        Permission(name='create_post', display_name='Yazı Oluşturma', category='blog'),
        Permission(name='edit_post', display_name='Yazı Düzenleme', category='blog'),
        Permission(name='delete_post', display_name='Yazı Silme', category='blog'),
        Permission(name='moderate_comments', display_name='Yorum Moderasyonu', category='blog'),
        Permission(name='create_event', display_name='Etkinlik Oluşturma', category='event'),
        Permission(name='edit_event', display_name='Etkinlik Düzenleme', category='event'),
        Permission(name='delete_event', display_name='Etkinlik Silme', category='event'),
        Permission(name='manage_registrations', display_name='Kayıt Yönetimi', category='event'),
        Permission(name='scan_qr_codes', display_name='QR Kod Okutma', category='security'),
        Permission(name='view_event_reports', display_name='Etkinlik Raporları', category='admin'),
    ]
    db.session.add_all(permissions)
    db.session.commit()
    
    # İzinleri rollere ata
    admin_role.permissions = permissions  # root: tüm yetkiler
    manager_role.permissions = permissions  # Yönetici: tüm yetkiler
    content_creator_role.permissions = [p for p in permissions if p.category in ['blog', 'event']]
    moderator_role.permissions = [p for p in permissions if p.name == 'moderate_comments']
    security_role.permissions = [p for p in permissions if p.name == 'scan_qr_codes']
    
    # Root kullanıcı oluştur
    admin = User(
        username='root',
        email='root@atakkulubu.com',
        first_name='Root',
        last_name='Admin',
        is_active=True,
        is_approved=True,
        email_confirmed=True
    )
    admin.set_password('Senveben12*')
    admin.roles.append(admin_role)
    db.session.add(admin)
    
    # Örnek kullanıcılar
    user1 = User(
        username='ayse_yildiz',
        email='ayse@example.com',
        first_name='Ayşe',
        last_name='Yıldız',
        is_active=True,
        is_approved=True,
        email_confirmed=True
    )
    user1.set_password('password123')
    user1.roles.append(content_creator_role)
    db.session.add(user1)
    
    user2 = User(
        username='mehmet_ay',
        email='mehmet@example.com',
        first_name='Mehmet',
        last_name='Ay',
        is_active=True,
        is_approved=True,
        email_confirmed=True
    )
    user2.set_password('password123')
    user2.roles.append(member_role)
    db.session.add(user2)
    
    db.session.commit()
    
    # Site ayarları
    settings = [
        # Genel Bilgiler
        SiteSetting(key='site_name', value='ATAK Kulübü', category='general'),
        SiteSetting(key='site_description', value='Astronomi ve Uzay Bilimleri Kulübü', category='general'),
        SiteSetting(key='site_logo', value='/static/uploads/logo_20251019_133051.png', category='general'),
        
        # İletişim Bilgileri
        SiteSetting(key='contact_email', value='info@atakkulubu.com', category='contact'),
        SiteSetting(key='contact_phone', value='+90 555 123 45 67', category='contact'),
        SiteSetting(key='address', value='İstanbul Üniversitesi Astronomi Bölümü, İstanbul, Türkiye', category='contact'),
        
        # Sosyal Medya
        SiteSetting(key='social_facebook', value='https://facebook.com/atakkulubu', category='social'),
        SiteSetting(key='social_instagram', value='https://instagram.com/atakkulubu', category='social'),
        SiteSetting(key='social_twitter', value='https://twitter.com/atakkulubu', category='social'),
        SiteSetting(key='social_youtube', value='', category='social'),
        SiteSetting(key='social_linkedin', value='', category='social'),
        SiteSetting(key='social_whatsapp', value='', category='social'),
        SiteSetting(key='social_telegram', value='', category='social'),
        SiteSetting(key='social_discord', value='', category='social'),
        
        # SEO ve Meta
        SiteSetting(key='meta_keywords', value='atak, astronomi, uzay, kulüp, teleskop, gözlem', category='seo'),
        SiteSetting(key='google_analytics', value='', category='seo'),
        
        # Blog Ayarları
        SiteSetting(key='comment_auto_approve', value='false', category='blog', description='Yorumlar otomatik onaylansın mı?'),
        SiteSetting(key='comment_blacklist', value='spam,reklam,kötü,hakaret', category='blog', description='Yasaklı kelimeler (virgülle ayrılmış)'),
        
        # Genel Ayarlar
        SiteSetting(key='items_per_page', value='10', category='general'),
        SiteSetting(key='user_approval_required', value='true', category='general'),
        SiteSetting(key='maintenance_mode', value='false', category='general'),
        SiteSetting(key='maintenance_message', value='Site şu anda bakımdadır. Lütfen daha sonra tekrar ziyaret edin.', category='general'),
    ]
    db.session.add_all(settings)
    
    # Örnek etkinlikler
    event1 = Event(
        title='Ay Gözlemi Gecesi',
        description='Teleskoplarımızla Ay\'ın kraterleri ve detaylarını gözlemleyeceğiz.',
        content='Bu özel etkinlikte, profesyonel teleskoplarımız ile Ay\'ın yüzeyini detaylı olarak inceleyeceğiz. Deneyimli gözlemcilerimiz eşliğinde Ay\'ın kraterlerini, dağlarını ve diğer formasyonlarını keşfedeceğiz.',
        location='ATAK Kulübü Gözlemevi',
        event_date=datetime.now() + timedelta(days=7),
        registration_deadline=datetime.now() + timedelta(days=5),
        max_participants=30,
        is_registration_open=True,
        is_published=True,
        event_type='gözlem',
        created_by=admin.id
    )
    
    event2 = Event(
        title='Astrofotografçılık Atölyesi',
        description='Gece gökyüzü fotoğrafçılığı tekniklerini öğrenin.',
        content='Bu atölyede, uzay fotoğrafçılığının temellerini öğrenecek, ekipman seçimi, kamera ayarları ve post-processing tekniklerini keşfedeceksiniz.',
        location='ATAK Kulübü Eğitim Salonu',
        event_date=datetime.now() + timedelta(days=14),
        registration_deadline=datetime.now() + timedelta(days=12),
        max_participants=20,
        is_registration_open=True,
        is_published=True,
        event_type='atölye',
        created_by=user1.id
    )
    
    event3 = Event(
        title='Perseid Meteor Yağmuru Gözlemi',
        description='Yılın en görkemli meteor yağmurunu birlikte izleyelim!',
        content='Perseid meteor yağmuru, her yıl Ağustos ayında gerçekleşen muhteşem bir göksel olaydır. Bu özel gece, şehir ışıklarından uzakta, meteor yağmurunu birlikte izleyeceğiz.',
        location='Şile Kamp Alanı',
        event_date=datetime.now() - timedelta(days=30),
        max_participants=50,
        is_registration_open=False,
        is_published=True,
        event_type='gözlem',
        created_by=admin.id
    )
    
    db.session.add_all([event1, event2, event3])
    
    # Örnek blog yazıları
    post1 = Post(
        title='Güneş Sistemimizin En Büyük Gezegeni: Jüpiter',
        slug='gunes-sistemimizin-en-buyuk-gezegeni-jupiter',
        summary='Jüpiter hakkında bilmeniz gereken her şey.',
        content='''
        Jüpiter, Güneş Sistemimizin en büyük gezegenidir. Kütlesi, diğer tüm gezegenlerin toplamından 2,5 kat daha fazladır.
        
        ## Jüpiter'in Özellikleri
        
        - Çapı: 142,984 km
        - Kütlesi: 1.898 × 10^27 kg
        - Uydu Sayısı: 79 bilinen uydu
        - Orbital Periyot: 11.86 Dünya yılı
        
        Jüpiter'in en belirgin özelliği, yüzeyindeki Büyük Kırmızı Leke'dir. Bu dev fırtına, en az 300 yıldır devam etmektedir.
        ''',
        category='makale',
        tags='jüpiter, gezegenler, güneş sistemi',
        is_published=True,
        published_at=datetime.utcnow() - timedelta(days=5),
        author_id=user1.id,
        views=150
    )
    
    post2 = Post(
        title='Yeni Teleskopumuz Kulübe Geldi!',
        slug='yeni-teleskopumuz-kulube-geldi',
        summary='Kulübümüze yeni bir Celestron teleskop katıldı.',
        content='''
        Heyecan verici haberler! Kulübümüze yeni bir Celestron NexStar 8SE teleskopu katıldı.
        
        Bu profesyonel teleskop ile artık daha detaylı gözlemler yapabileceğiz. 8 inçlik aynası sayesinde,
        gezegenleri, nebula'ları ve galaksileri daha net görebileceğiz.
        
        İlk gözlem etkinliğimiz gelecek hafta sonu. Herkesi bekliyoruz!
        ''',
        category='duyuru',
        tags='teleskop, ekipman, duyuru',
        is_published=True,
        is_featured=True,
        published_at=datetime.utcnow() - timedelta(days=2),
        author_id=admin.id,
        views=89
    )
    
    db.session.add_all([post1, post2])
    db.session.commit()
    
    # Örnek yorumlar
    comment1 = Comment(
        content='Harika bir yazı olmuş, teşekkürler!',
        post_id=post1.id,
        author_id=user2.id,
        is_approved=True
    )
    
    comment2 = Comment(
        content='Jüpiter\'i geçen ay gözlemlemiştik, gerçekten muhteşem bir gezegen.',
        post_id=post1.id,
        author_id=admin.id,
        is_approved=True
    )
    
    db.session.add_all([comment1, comment2])
    db.session.commit()
    
    # Örnek duyurular
    announcement1 = Announcement(
        title='Teleskop Bakım Duyurusu',
        content='Kulüp teleskoplarımız periyodik bakıma alınmıştır. 15 Ocak tarihinde tekrar kullanıma açılacaktır.',
        target_roles='all',
        is_published=True,
        send_email=False,
        created_by=admin.id
    )
    
    # Sadece admin ve içerik üreticilerine duyuru
    announcement2 = Announcement(
        title='İçerik Üreticileri Toplantısı',
        content='Bu ay içerik planlama toplantımızı 20 Ocak Cumartesi günü saat 14:00\'te yapacağız. Toplantıya tüm içerik üreticilerimiz davetlidir.',
        target_roles=f'{admin_role.id},{content_creator_role.id}',
        is_published=True,
        send_email=True,
        email_sent=False,
        created_by=admin.id
    )
    
    # Sadece üyelere duyuru
    announcement3 = Announcement(
        title='Yeni Üyelik Avantajları',
        content='Sevgili üyelerimiz, yeni dönem üyelik avantajlarımız yayınlandı! Detaylar için kulübümüze uğrayın.',
        target_roles=f'{member_role.id}',
        is_published=True,
        send_email=False,
        created_by=admin.id
    )
    
    db.session.add_all([announcement1, announcement2, announcement3])
    db.session.commit()
    
    print('Örnek veriler başarıyla eklendi!')
    print('\n' + '=' * 60)
    print('📋 GİRİŞ BİLGİLERİ')
    print('=' * 60)
    print('Root Admin:')
    print('  Kullanıcı adı: root')
    print('  Şifre: Senveben12*')
    print('  E-posta: root@atakkulubu.com')
    print('\nİçerik Üreticisi:')
    print('  Kullanıcı adı: ayse_yildiz')
    print('  Şifre: password123')
    print('\nÜye:')
    print('  Kullanıcı adı: mehmet_ay')
    print('  Şifre: password123')
    print('=' * 60)
    print('\n✅ Roller ve hiyerarşi seviyeleri:')
    print(f'   Root (Seviye 100) - Tüm yetkiler')
    print(f'   Yönetici (Seviye 50) - Tüm yetkiler')
    print(f'   Moderatör (Seviye 30) - Yorum moderasyonu')
    print(f'   İçerik Üreticisi (Seviye 20) - Blog ve etkinlik')
    print(f'   Güvenlik (Seviye 15) - QR kod okutma')
    print(f'   Üye (Seviye 10) - Standart kullanıcı')
    print('=' * 60)


if __name__ == '__main__':
    # Yerel geliştirme için HTTPS (kamera erişimi)
    # PythonAnywhere otomatik olarak HTTPS kullanır
    import os
    use_ssl = os.environ.get('USE_SSL', 'true').lower() == 'true'
    
    if use_ssl:
        try:
            app.run(debug=True, port=5000, ssl_context='adhoc')
        except:
            # pyopenssl kurulu değilse normal HTTP
            print("⚠️  HTTPS başlatılamadı, HTTP kullanılıyor (kamera mobilde çalışmayabilir)")
            app.run(debug=True, port=5000)
    else:
        app.run(debug=True, port=5000)
