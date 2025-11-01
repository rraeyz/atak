from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_mail import Mail  # Gerektiğinde eklenecek
from flask_migrate import Migrate
from config import config
import os

# Extension'ları başlat
db = SQLAlchemy()
login_manager = LoginManager()
# mail = Mail()  # Gerektiğinde eklenecek
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Yapılandırmayı yükle
    app.config.from_object(config[config_name])
    
    # Extension'ları uygulamaya bağla
    db.init_app(app)
    login_manager.init_app(app)
    # mail.init_app(app)  # Gerektiğinde eklenecek
    migrate.init_app(app, db)
    
    # Login manager ayarları
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'
    login_manager.login_message_category = 'warning'
    
    # Upload klasörünü oluştur
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Blueprint'leri kaydet
    from app.routes import main, auth, admin, events, blog, security
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(security.bp)
    
    # Bakım modu kontrolü - TÜM isteklerde çalışır
    @app.before_request
    def check_maintenance():
        from app.models import SiteSetting
        from flask import render_template, request
        from flask_login import current_user
        
        # Static dosyalar ve admin/auth route'larını atla
        if request.endpoint and (
            request.endpoint.startswith('admin.') or 
            request.endpoint.startswith('auth.') or
            request.endpoint == 'static'
        ):
            return None
        
        # Bakım modu kontrolü
        maintenance_setting = SiteSetting.query.filter_by(key='maintenance_mode').first()
        if maintenance_setting and maintenance_setting.value == 'true':
            # Root kullanıcıları bakım modunda da erişebilir
            if current_user.is_authenticated and current_user.has_role('root'):
                return None
            
            # Bakım modu mesajı ve süresi
            message_setting = SiteSetting.query.filter_by(key='maintenance_message').first()
            message = message_setting.value if message_setting else 'Site şu anda bakımdadır. Lütfen daha sonra tekrar ziyaret edin.'
            
            duration_setting = SiteSetting.query.filter_by(key='maintenance_duration').first()
            duration = duration_setting.value if duration_setting else 'Kısa bir süre'
            
            return render_template('errors/maintenance.html', message=message, duration=duration), 503
        
        return None
    
    # Context processor'ları kaydet
    from app.utils import template_filters
    app.jinja_env.filters['datetime'] = template_filters.format_datetime
    
    # Site ayarlarını tüm template'lerde kullanılabilir yap
    @app.context_processor
    def inject_site_settings():
        from app.models import SiteSetting
        from datetime import datetime
        settings = SiteSetting.query.all()
        settings_dict = {s.key: s.value for s in settings}
        return dict(site_settings=settings_dict, now=datetime.utcnow())
    
    # Hata işleyicileri
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app
