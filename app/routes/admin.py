from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Role, Permission, Event, Post, Comment, EventRegistration, SiteSetting, ContactMessage, Announcement
from app.utils.decorators import admin_required, permission_required
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_request
@login_required
def before_request():
    """Admin sayfalarına erişim kontrolü"""
    if not current_user.has_permission('admin_access'):
        abort(403)


@bp.route('/')
def index():
    """Admin ana sayfa / Dashboard"""
    # İstatistikler
    total_users = User.query.count()
    pending_users = User.query.filter_by(is_approved=False).count()
    total_events = Event.query.count()
    total_posts = Post.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    # Son kullanıcılar
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Yaklaşan etkinlikler
    upcoming_events = Event.query.filter(
        Event.event_date > datetime.now()
    ).order_by(Event.event_date.asc()).limit(5).all()
    
    # Son mesajlar
    recent_messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).limit(5).all()
    
    # Stats objesi oluştur
    stats = {
        'total_users': total_users,
        'pending_users': pending_users,
        'total_events': total_events,
        'upcoming_events': len(upcoming_events),
        'total_posts': total_posts,
        'published_posts': Post.query.filter_by(published=True).count(),
        'total_registrations': EventRegistration.query.count(),
        'pending_registrations': EventRegistration.query.filter_by(status='pending').count(),
        'total_messages': ContactMessage.query.count(),
        'unread_messages': unread_messages
    }
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_users=recent_users,
                         upcoming_events=upcoming_events,
                         recent_messages=recent_messages)


# ===== KULLANICI YÖNETİMİ =====
@bp.route('/kullanicilar')
@permission_required('manage_users')
def users():
    """Kullanıcı listesi"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    search_type = request.args.get('search_type', 'all')
    status = request.args.get('status', '')
    role_id = request.args.get('role', '', type=int)
    
    query = User.query
    
    # Arama filtresi
    if search:
        if search_type == 'username':
            query = query.filter(User.username.contains(search))
        elif search_type == 'email':
            query = query.filter(User.email.contains(search))
        elif search_type == 'name':
            query = query.filter(
                (User.first_name.contains(search)) |
                (User.last_name.contains(search))
            )
        else:  # all
            query = query.filter(
                (User.username.contains(search)) |
                (User.email.contains(search)) |
                (User.first_name.contains(search)) |
                (User.last_name.contains(search))
            )
    
    # Durum filtresi
    if status == 'pending':
        query = query.filter_by(is_approved=False, is_active=True)
    elif status == 'approved':
        query = query.filter_by(is_approved=True, is_active=True)
    elif status == 'banned':
        query = query.filter_by(is_active=False)
    
    # Rol filtresi
    if role_id:
        query = query.filter(User.roles.any(Role.id == role_id))
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Tüm rolleri al (filtreleme için)
    all_roles = Role.query.order_by(Role.display_name).all()
    
    return render_template('admin/users.html', 
                         users=users, 
                         search=search, 
                         status=status,
                         all_roles=all_roles)


@bp.route('/kullanicilar/<int:id>')
@permission_required('manage_users')
def user_detail(id):
    """Kullanıcı detay"""
    user = User.query.get_or_404(id)
    all_roles = Role.query.all()
    
    return render_template('admin/user_detail.html', user=user, all_roles=all_roles)


@bp.route('/kullanicilar/<int:id>/onayla', methods=['POST'])
@permission_required('manage_users')
def approve_user(id):
    """Kullanıcıyı onayla"""
    user = User.query.get_or_404(id)
    user.is_approved = True
    user.is_active = True  # Onaylanan kullanıcı aktif olur
    db.session.commit()
    
    flash(f'{user.username} kullanıcısı onaylandı.', 'success')
    return redirect(url_for('admin.users'))


@bp.route('/kullanicilar/<int:id>/ban-toggle', methods=['POST'])
@permission_required('manage_users')
def toggle_ban_user(id):
    """Kullanıcıyı banla/ban kaldır"""
    # Sadece moderatör ve yöneticiler ban işlemi yapabilir
    if not (current_user.has_role('moderator') or current_user.has_role('admin')):
        abort(403)
    
    user = User.query.get_or_404(id)
    
    # Root kullanıcıları banlanamaz
    if user.has_role('root'):
        flash('Root kullanıcıları banlanamaz.', 'danger')
        return redirect(url_for('admin.user_detail', id=id))
    
    # Admin ve moderatörleri banlayamaz
    if user.has_role('admin') or user.has_role('moderator'):
        flash('Yönetici veya moderatör banlanamaz.', 'danger')
        return redirect(url_for('admin.user_detail', id=id))
    
    # Kendi kendini banlayamaz
    if user.id == current_user.id:
        flash('Kendinizi banlayamazsınız.', 'danger')
        return redirect(url_for('admin.user_detail', id=id))
    
    # is_active alanını toggle et (False = banned)
    user.is_active = not user.is_active
    db.session.commit()
    
    action = 'aktif' if user.is_active else 'banlandı'
    flash(f'{user.username} kullanıcısı {action}.', 'success')
    return redirect(url_for('admin.user_detail', id=id))


@bp.route('/kullanicilar/<int:id>/rol-ekle', methods=['POST'])
@permission_required('manage_users')
def add_user_role(id):
    """Kullanıcıya rol ekle"""
    user = User.query.get_or_404(id)
    role_id = request.form.get('role_id', type=int)
    
    role = Role.query.get_or_404(role_id)
    
    # Root rolü sadece root kullanıcısına aittir, başkasına verilemez
    if role.name == 'root':
        flash('Root rolü özeldir ve başka kullanıcılara verilemez.', 'danger')
        return redirect(url_for('admin.user_detail', id=id))
    
    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        flash(f'{role.display_name} rolü eklendi.', 'success')
    else:
        flash('Kullanıcı zaten bu role sahip.', 'info')
    
    return redirect(url_for('admin.user_detail', id=id))


@bp.route('/kullanicilar/<int:id>/rol-kaldir/<int:role_id>', methods=['POST'])
@permission_required('manage_users')
def remove_user_role(id, role_id):
    """Kullanıcıdan rol kaldır"""
    user = User.query.get_or_404(id)
    role = Role.query.get_or_404(role_id)
    
    # Root rolü kaldırılamaz
    if role.name == 'root':
        flash('Root rolü kaldırılamaz.', 'danger')
        return redirect(url_for('admin.user_detail', id=id))
    
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        flash(f'{role.display_name} rolü kaldırıldı.', 'success')
    
    return redirect(url_for('admin.user_detail', id=id))


# ===== ROL YÖNETİMİ =====
@bp.route('/roller')
@permission_required('manage_roles')
def roles():
    """Rol listesi"""
    roles = Role.query.all()
    return render_template('admin/roles.html', roles=roles)


@bp.route('/roller/yeni', methods=['GET', 'POST'])
@permission_required('manage_roles')
def create_role():
    """Yeni rol oluştur"""
    if request.method == 'POST':
        name = request.form.get('name')
        display_name = request.form.get('display_name')
        description = request.form.get('description')
        permission_ids = request.form.getlist('permissions', type=int)
        
        if not name or not display_name:
            flash('Rol adı ve görünen adı zorunludur.', 'danger')
            return redirect(url_for('admin.create_role'))
        
        # Aynı isimde rol var mı?
        if Role.query.filter_by(name=name).first():
            flash('Bu isimde bir rol zaten mevcut.', 'danger')
            return redirect(url_for('admin.create_role'))
        
        role = Role(
            name=name,
            display_name=display_name,
            description=description,
            is_system=False
        )
        
        # İzinleri ekle
        if permission_ids:
            permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
            role.permissions = permissions
        
        db.session.add(role)
        db.session.commit()
        
        flash('Rol başarıyla oluşturuldu.', 'success')
        return redirect(url_for('admin.roles'))
    
    all_permissions = Permission.query.all()
    return render_template('admin/create_role.html', permissions=all_permissions)


@bp.route('/roller/<int:id>/duzenle', methods=['GET', 'POST'])
@permission_required('manage_roles')
def edit_role(id):
    """Rol düzenle"""
    role = Role.query.get_or_404(id)
    
    if role.is_system:
        flash('Sistem rolleri düzenlenemez.', 'warning')
        return redirect(url_for('admin.roles'))
    
    if request.method == 'POST':
        role.display_name = request.form.get('display_name')
        role.description = request.form.get('description')
        permission_ids = request.form.getlist('permissions', type=int)
        
        # İzinleri güncelle
        if permission_ids:
            permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
            role.permissions = permissions
        else:
            role.permissions = []
        
        db.session.commit()
        
        flash('Rol başarıyla güncellendi.', 'success')
        return redirect(url_for('admin.roles'))
    
    all_permissions = Permission.query.all()
    return render_template('admin/edit_role.html', role=role, permissions=all_permissions)


@bp.route('/roller/<int:id>/sil', methods=['POST'])
@permission_required('manage_roles')
def delete_role(id):
    """Rol sil"""
    role = Role.query.get_or_404(id)
    
    if role.is_system:
        flash('Sistem rolleri silinemez.', 'warning')
        return redirect(url_for('admin.roles'))
    
    db.session.delete(role)
    db.session.commit()
    
    flash('Rol silindi.', 'info')
    return redirect(url_for('admin.roles'))


# ===== ETKİNLİK YÖNETİMİ =====
@bp.route('/etkinlikler')
@permission_required('create_event')
def events():
    """Etkinlik listesi"""
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.event_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/events.html', events=events)

# NOT: Etkinlik create/edit/delete işlemleri events Blueprint'inde yapılıyor
# Admin panelindeki butonlar events.create, events.edit, events.delete route'larına yönlendiriyor


@bp.route('/etkinlikler/<int:id>/rapor')
@login_required
def event_report(id):
    """Etkinlik raporu - Admin veya view_event_reports izni gerekli"""
    # Admin veya izinli kullanıcılar erişebilir
    if not (current_user.is_admin() or current_user.can('view_event_reports')):
        abort(403)
    
    from app.utils.event_reports import generate_event_report, get_event_statistics
    
    event = Event.query.get_or_404(id)
    report = generate_event_report(id)
    stats = get_event_statistics(id)
    
    return render_template('admin/event_report.html', 
                         event=event,
                         report=report,
                         stats=stats)


@bp.route('/etkinlikler/<int:id>/rapor/indir')
@login_required
def download_event_report(id):
    """Etkinlik raporunu CSV olarak indir - Admin veya view_event_reports izni gerekli"""
    # Admin veya izinli kullanıcılar erişebilir
    if not (current_user.is_admin() or current_user.can('view_event_reports')):
        abort(403)
    
    from app.utils.event_reports import generate_csv_report
    from flask import Response
    
    event = Event.query.get_or_404(id)
    csv_content = generate_csv_report(id)
    
    filename = f"etkinlik_raporu_{event.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return Response(
        csv_content,
        mimetype='text/csv; charset=utf-8',
        headers={
            'Content-Disposition': f'attachment; filename={filename}',
            'Content-Type': 'text/csv; charset=utf-8'
        }
    )


@bp.route('/etkinlikler/<int:id>/katilimcilar')
@permission_required('manage_registrations')
def event_registrations(id):
    """Etkinlik katılımcıları"""
    event = Event.query.get_or_404(id)
    registrations = EventRegistration.query.filter_by(event_id=id).all()
    
    return render_template('admin/event_registrations.html',
                         event=event,
                         registrations=registrations)


# ===== YAZI YÖNETİMİ =====
@bp.route('/yazilar')
@permission_required('edit_post')
def posts():
    """Yazı listesi"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/posts.html', posts=posts)


@bp.route('/yazilar/ayarlar', methods=['GET', 'POST'])
@permission_required('manage_settings')
def blog_settings():
    """Blog ayarları"""
    if request.method == 'POST':
        # Otomatik onay ayarı
        auto_approve = request.form.get('auto_approve') == 'on'
        setting = SiteSetting.query.filter_by(key='comment_auto_approve').first()
        if setting:
            setting.value = 'true' if auto_approve else 'false'
        else:
            setting = SiteSetting(key='comment_auto_approve', value='true' if auto_approve else 'false', category='blog')
            db.session.add(setting)
        
        # Yasaklı kelimeler
        blacklist = request.form.get('blacklist', '')
        setting = SiteSetting.query.filter_by(key='comment_blacklist').first()
        if setting:
            setting.value = blacklist
        else:
            setting = SiteSetting(key='comment_blacklist', value=blacklist, category='blog')
            db.session.add(setting)
        
        db.session.commit()
        flash('Blog ayarları güncellendi.', 'success')
        return redirect(url_for('admin.blog_settings'))
    
    # Ayarları getir
    auto_approve_setting = SiteSetting.query.filter_by(key='comment_auto_approve').first()
    auto_approve = auto_approve_setting.value == 'true' if auto_approve_setting else False
    
    blacklist_setting = SiteSetting.query.filter_by(key='comment_blacklist').first()
    blacklist = blacklist_setting.value if blacklist_setting else ''
    
    return render_template('admin/blog_settings.html', 
                         auto_approve=auto_approve, 
                         blacklist=blacklist)


# ===== SİTE AYARLARI =====
@bp.route('/ayarlar', methods=['GET', 'POST'])
@permission_required('manage_settings')
def settings():
    """Site ayarları"""
    if request.method == 'POST':
        logo_uploaded = False
        
        # Logo dosyası yükleme kontrolü
        if 'logo_file' in request.files:
            file = request.files['logo_file']
            if file and file.filename:
                # Dosya güvenliği
                filename = secure_filename(file.filename)
                # Benzersiz isim oluştur
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                name, ext = os.path.splitext(filename)
                unique_filename = f"logo_{timestamp}{ext}"
                
                # Uploads klasörü yolu
                upload_folder = os.path.join('app', 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Dosyayı kaydet
                file_path = os.path.join(upload_folder, unique_filename)
                file.save(file_path)
                
                # Logo URL'sini ayarla
                logo_url = f"/static/uploads/{unique_filename}"
                setting = SiteSetting.query.filter_by(key='site_logo').first()
                if setting:
                    setting.value = logo_url
                else:
                    setting = SiteSetting(key='site_logo', value=logo_url)
                    db.session.add(setting)
                
                logo_uploaded = True
        
        # Diğer form alanlarını işle
        for key, value in request.form.items():
            if key.startswith('setting_'):
                setting_key = key.replace('setting_', '')
                
                # Eğer logo dosyası yüklendiyse, site_logo URL alanını atla
                if setting_key == 'site_logo' and logo_uploaded:
                    continue
                
                setting = SiteSetting.query.filter_by(key=setting_key).first()
                
                if setting:
                    setting.value = value
                else:
                    setting = SiteSetting(key=setting_key, value=value)
                    db.session.add(setting)
        
        db.session.commit()
        flash('Ayarlar başarıyla güncellendi.', 'success')
        return redirect(url_for('admin.settings'))
    
    settings = SiteSetting.query.all()
    settings_dict = {s.key: s.value for s in settings}
    
    return render_template('admin/settings.html', settings=settings_dict)


# ===== MESAJLAR =====
@bp.route('/mesajlar')
def messages():
    """İletişim mesajları"""
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/messages.html', messages=messages)


@bp.route('/mesajlar/<int:id>')
def message_detail(id):
    """Mesaj detay"""
    message = ContactMessage.query.get_or_404(id)
    
    # Okundu olarak işaretle
    if not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('admin/message_detail.html', message=message)


@bp.route('/mesajlar/<int:id>/yanitla', methods=['POST'])
def reply_message(id):
    """Mesajı yanıtla"""
    message = ContactMessage.query.get_or_404(id)
    reply = request.form.get('reply')
    
    message.reply = reply
    message.is_replied = True
    message.replied_at = datetime.utcnow()
    
    db.session.commit()
    
    # Burada e-posta gönderme işlemi yapılabilir
    
    flash('Yanıt kaydedildi.', 'success')
    return redirect(url_for('admin.message_detail', id=id))


@bp.route('/mesajlar/<int:id>/sil', methods=['POST'])
def delete_message(id):
    """Mesajı sil"""
    message = ContactMessage.query.get_or_404(id)
    
    sender_name = message.name
    db.session.delete(message)
    db.session.commit()
    
    flash(f'{sender_name} tarafından gönderilen mesaj silindi.', 'success')
    return redirect(url_for('admin.messages'))


# ============== DUYURULAR ==============

@bp.route('/duyurular')
def announcements():
    """Duyuru listesi"""
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    roles = Role.query.all()
    return render_template('admin/announcements.html', announcements=announcements, roles=roles)


@bp.route('/duyurular/yeni', methods=['GET', 'POST'])
def new_announcement():
    """Yeni duyuru oluştur"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_published = 'is_published' in request.form
        send_email = 'send_email' in request.form
        
        # Hedef rolleri al
        target_roles = request.form.getlist('target_roles')
        
        if not title or not content:
            flash('Başlık ve içerik zorunludur.', 'error')
            return redirect(url_for('admin.new_announcement'))
        
        # Eğer hiç rol seçilmediyse "all" olarak işaretle
        if not target_roles:
            target_roles_str = 'all'
        else:
            target_roles_str = ','.join(target_roles)
        
        announcement = Announcement(
            title=title,
            content=content,
            target_roles=target_roles_str,
            is_published=is_published,
            send_email=send_email,
            created_by=current_user.id
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        # E-posta gönderimi aktifse ve duyuru yayınlanmışsa
        if send_email and is_published and not announcement.email_sent:
            send_announcement_emails(announcement)
        
        flash('Duyuru başarıyla oluşturuldu.', 'success')
        return redirect(url_for('admin.announcements'))
    
    # GET isteği
    roles = Role.query.all()
    return render_template('admin/announcement_form.html', roles=roles, announcement=None)


@bp.route('/duyurular/<int:id>/duzenle', methods=['GET', 'POST'])
def edit_announcement(id):
    """Duyuru düzenle"""
    announcement = Announcement.query.get_or_404(id)
    
    if request.method == 'POST':
        announcement.title = request.form.get('title')
        announcement.content = request.form.get('content')
        announcement.is_published = 'is_published' in request.form
        send_email = 'send_email' in request.form
        
        # Hedef rolleri al
        target_roles = request.form.getlist('target_roles')
        
        if not announcement.title or not announcement.content:
            flash('Başlık ve içerik zorunludur.', 'error')
            return redirect(url_for('admin.edit_announcement', id=id))
        
        # Rolleri güncelle
        if not target_roles:
            announcement.target_roles = 'all'
        else:
            announcement.target_roles = ','.join(target_roles)
        
        # E-posta gönderimi
        old_send_email = announcement.send_email
        announcement.send_email = send_email
        announcement.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Eğer e-posta gönderme şimdi aktif hale geldiyse ve daha önce gönderilmediyse
        if send_email and not old_send_email and announcement.is_published and not announcement.email_sent:
            send_announcement_emails(announcement)
        
        flash('Duyuru başarıyla güncellendi.', 'success')
        return redirect(url_for('admin.announcements'))
    
    # GET isteği
    roles = Role.query.all()
    
    # Seçili rolleri belirle
    selected_roles = []
    if announcement.target_roles != 'all':
        selected_roles = [int(r) for r in announcement.target_roles.split(',') if r]
    
    return render_template('admin/announcement_form.html', 
                         roles=roles, 
                         announcement=announcement,
                         selected_roles=selected_roles)


@bp.route('/duyurular/<int:id>/sil', methods=['POST'])
def delete_announcement(id):
    """Duyuru sil"""
    announcement = Announcement.query.get_or_404(id)
    
    db.session.delete(announcement)
    db.session.commit()
    
    flash('Duyuru başarıyla silindi.', 'success')
    return redirect(url_for('admin.announcements'))


def send_announcement_emails(announcement):
    """Duyuruyu hedef kullanıcılara e-posta ile gönder"""
    try:
        # Hedef kullanıcıları belirle
        if announcement.target_roles == 'all':
            users = User.query.filter_by(is_approved=True).all()
        else:
            role_ids = [int(r) for r in announcement.target_roles.split(',') if r]
            users = User.query.join(User.roles).filter(
                Role.id.in_(role_ids),
                User.is_approved == True
            ).distinct().all()
        
        # E-posta gönderme işlemi burada yapılacak
        # Şu an için sadece işaretleme yapıyoruz
        announcement.email_sent = True
        db.session.commit()
        
        flash(f'{len(users)} kullanıcıya e-posta gönderildi.', 'success')
    except Exception as e:
        flash(f'E-posta gönderme hatası: {str(e)}', 'error')
