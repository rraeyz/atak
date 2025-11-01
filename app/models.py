from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Kullanıcı-Rol ilişkisi için ara tablo
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

# Rol-İzin ilişkisi için ara tablo
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    """Kullanıcı modeli"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255), default='default-avatar.png')
    
    # Hesap durumu
    is_active = db.Column(db.Boolean, default=False)  # Admin onayı bekliyor
    is_approved = db.Column(db.Boolean, default=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    
    # Tarih bilgileri
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    event_registrations = db.relationship('EventRegistration', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Şifreyi hashle ve kaydet"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Şifreyi kontrol et"""
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        """Kullanıcının belirli bir rolü var mı?"""
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, permission_name):
        """Kullanıcının belirli bir izni var mı?"""
        for role in self.roles:
            if any(perm.name == permission_name for perm in role.permissions):
                return True
        return False
    
    def can(self, permission_name):
        """has_permission için alias (şablon kullanımı için)"""
        return self.has_permission(permission_name)
    
    def is_admin(self):
        """Kullanıcı admin mi?"""
        return self.has_role('admin')
    
    def get_highest_role_level(self):
        """Kullanıcının en yüksek rol seviyesini döndür"""
        if not self.roles:
            return 0
        return max(role.hierarchy_level for role in self.roles)
    
    def can_manage_user(self, target_user):
        """Bu kullanıcı hedef kullanıcıyı yönetebilir mi?"""
        # Root her zaman yönetebilir
        if self.has_role('root'):
            return True
        
        # Kendini yönetemez
        if self.id == target_user.id:
            return False
        
        # Hedef kullanıcının en yüksek rolü, yöneten kullanıcıdan düşük olmalı
        my_level = self.get_highest_role_level()
        target_level = target_user.get_highest_role_level()
        
        return my_level > target_level
    
    def can_assign_role(self, role):
        """Bu kullanıcı belirli bir rolü atayabilir mi?"""
        # Root her rolü atayabilir
        if self.has_role('root'):
            return True
        
        # Root rolü sadece root atayabilir
        if role.name == 'root':
            return False
        
        # Kullanıcının en yüksek rolü, atanacak rolden yüksek olmalı
        my_level = self.get_highest_role_level()
        return my_level > role.hierarchy_level
    
    @property
    def full_name(self):
        """Tam adı döndür"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model):
    """Rol modeli"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    is_system = db.Column(db.Boolean, default=False)  # Sistem rolleri silinemez
    hierarchy_level = db.Column(db.Integer, default=0)  # Rol hiyerarşisi (yüksek = daha güçlü)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    permissions = db.relationship('Permission', secondary=role_permissions, 
                                 backref=db.backref('roles', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(db.Model):
    """İzin modeli"""
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(32))  # blog, event, user, admin vb.
    
    def __repr__(self):
        return f'<Permission {self.name}>'


class Event(db.Model):
    """Etkinlik modeli"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)  # Detaylı açıklama
    location = db.Column(db.String(200))
    organizer = db.Column(db.String(100))  # Organizatör adı
    notes = db.Column(db.Text)  # Notlar/Uyarılar
    
    # Tarih ve zaman
    event_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    registration_deadline = db.Column(db.DateTime)
    
    # Katılımcı bilgileri
    max_participants = db.Column(db.Integer)
    is_registration_open = db.Column(db.Boolean, default=True)
    
    # Görsel ve medya
    image = db.Column(db.String(255))
    gallery_images = db.Column(db.Text)  # JSON formatında birden fazla resim
    
    # Durum
    is_published = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    event_type = db.Column(db.String(32))  # gözlem, seminer, atölye vb.
    
    # Oluşturan kullanıcı
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    registrations = db.relationship('EventRegistration', backref='event', lazy='dynamic', cascade='all, delete-orphan')
    creator = db.relationship('User', foreign_keys=[created_by])
    
    @property
    def start_date(self):
        """Geriye uyumluluk için alias"""
        return self.event_date
    
    @property
    def is_past(self):
        """Etkinlik geçmiş mi?"""
        return self.event_date < datetime.utcnow()
    
    @property
    def registration_count(self):
        """Kayıtlı katılımcı sayısı"""
        return self.registrations.filter_by(status='approved').count()
    
    @property
    def is_full(self):
        """Etkinlik dolu mu?"""
        if self.max_participants:
            return self.registration_count >= self.max_participants
        return False
    
    def __repr__(self):
        return f'<Event {self.title}>'


class EventRegistration(db.Model):
    """Etkinlik kayıt modeli"""
    __tablename__ = 'event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Kayıt bilgileri
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, cancelled
    notes = db.Column(db.Text)
    attendance = db.Column(db.Boolean, default=False)  # Katıldı mı?
    
    # Tarih
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<EventRegistration {self.user_id} - {self.event_id}>'


class Post(db.Model):
    """Blog/Haber yazısı modeli"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    summary = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    
    # Görsel
    featured_image = db.Column(db.String(255))
    
    # Kategori ve etiketler
    category = db.Column(db.String(64))  # haber, makale, duyuru vb.
    tags = db.Column(db.String(200))  # Virgülle ayrılmış
    
    # Durum
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    
    # Yazar
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Tarih
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def published(self):
        """Geriye uyumluluk için alias"""
        return self.is_published
    
    def __repr__(self):
        return f'<Post {self.title}>'


class Comment(db.Model):
    """Yorum modeli"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Üst yorum (yanıt için)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    
    # Durum
    is_approved = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Tarih
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), 
                             lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Comment {self.id}>'


class SiteSetting(db.Model):
    """Site ayarları modeli"""
    __tablename__ = 'site_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.Text)
    data_type = db.Column(db.String(20), default='string')  # string, int, bool, json
    category = db.Column(db.String(32))  # general, contact, social vb.
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SiteSetting {self.key}>'


class ContactMessage(db.Model):
    """İletişim mesajları modeli"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    
    # Durum
    is_read = db.Column(db.Boolean, default=False)
    is_replied = db.Column(db.Boolean, default=False)
    reply = db.Column(db.Text)
    
    # Tarih
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    replied_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<ContactMessage {self.name} - {self.subject}>'


class Announcement(db.Model):
    """Duyuru modeli"""
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Görünürlük ayarları (JSON formatında rol ID'leri saklanacak)
    target_roles = db.Column(db.String(255))  # Örn: "1,2,3" veya "all"
    
    # Durum
    is_published = db.Column(db.Boolean, default=True)
    send_email = db.Column(db.Boolean, default=False)
    email_sent = db.Column(db.Boolean, default=False)
    
    # Kimlik
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Tarih
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    creator = db.relationship('User', backref='announcements')
    
    def __repr__(self):
        return f'<Announcement {self.title}>'
    
    def is_visible_to_user(self, user):
        """Duyuru bu kullanıcıya görünür mü?"""
        if not self.is_published:
            return False
        
        if self.target_roles == 'all':
            return True
        
        if not user.is_authenticated:
            return False
        
        # Kullanıcının rol ID'lerini al
        user_role_ids = [str(role.id) for role in user.roles]
        
        # Hedef rolleri kontrol et
        target_role_ids = self.target_roles.split(',') if self.target_roles else []
        
        return any(role_id in target_role_ids for role_id in user_role_ids)


class QRCode(db.Model):
    """Etkinlik QR kod modeli"""
    __tablename__ = 'qr_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey('event_registrations.id'), nullable=False)
    
    # QR kod bilgileri
    code = db.Column(db.String(255), unique=True, nullable=False, index=True)  # Benzersiz kod
    qr_image_path = db.Column(db.String(255))  # QR kod resmi yolu
    
    # Durum
    is_active = db.Column(db.Boolean, default=True)
    used = db.Column(db.Boolean, default=False)  # Giriş yapıldı mı?
    
    # Tarih
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime)
    
    # İlişkiler
    user = db.relationship('User', backref='qr_codes')
    event = db.relationship('Event', backref='qr_codes')
    registration = db.relationship('EventRegistration', backref='qr_code', uselist=False)
    check_ins = db.relationship('CheckIn', backref='qr_code', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QRCode {self.code}>'


class CheckIn(db.Model):
    """Etkinlik giriş kayıt modeli"""
    __tablename__ = 'check_ins'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    qr_code_id = db.Column(db.Integer, db.ForeignKey('qr_codes.id'))
    
    # Giriş bilgileri
    status = db.Column(db.String(20), default='checked_in')  # checked_in, not_registered
    checked_in_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Güvenlik görevlisi
    
    # Notlar
    notes = db.Column(db.Text)
    
    # Tarih
    checked_in_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    event = db.relationship('Event', foreign_keys=[event_id], backref='check_ins')
    user = db.relationship('User', foreign_keys=[user_id], backref='check_ins')
    security_staff = db.relationship('User', foreign_keys=[checked_in_by])
    # Template uyumluluğu için alias
    @property
    def checked_in_by_user(self):
        return self.security_staff
    
    def __repr__(self):
        return f'<CheckIn {self.user_id} - {self.event_id}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login için kullanıcı yükleyici"""
    return User.query.get(int(user_id))
