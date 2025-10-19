from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Role
from app.forms import LoginForm, RegisterForm, EditProfileForm, ChangePasswordForm
from app.utils.helpers import save_picture, delete_picture
from werkzeug.security import generate_password_hash
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Giriş sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Hesabınız aktif değil. Lütfen yönetici ile iletişime geçin.', 'warning')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        
        # Kullanıcının son görülme zamanını güncelle
        user.last_seen = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        
        flash(f'Hoş geldiniz, {user.username}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Kayıt sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Yeni kullanıcı oluştur
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            is_active=True,
            is_approved=False  # Admin onayı bekliyor
        )
        user.set_password(form.password.data)
        
        # Varsayılan rol ata (member)
        member_role = Role.query.filter_by(name='member').first()
        if member_role:
            user.roles.append(member_role)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Kayıt işleminiz başarılı! Hesabınız yönetici onayından sonra aktif olacaktır.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Çıkış"""
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('main.index'))


@bp.route('/profile')
@bp.route('/profile/<int:user_id>')
@login_required
def profile(user_id=None):
    """Kullanıcı profili"""
    if user_id:
        user = User.query.get_or_404(user_id)
    else:
        user = current_user
    
    from app.models import Post, Event, EventRegistration
    return render_template('auth/profile.html', user=user, Post=Post, Event=Event, EventRegistration=EventRegistration, now=datetime.utcnow())


@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Profil düzenleme"""
    form = EditProfileForm()
    
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        
        # Avatar yükleme
        if form.avatar.data:
            # Eski avatarı sil
            if current_user.avatar:
                delete_picture(current_user.avatar)
            
            # Yeni avatarı kaydet
            avatar_path = save_picture(form.avatar.data, folder='avatars', size=(300, 300))
            current_user.avatar = avatar_path
        
        db.session.commit()
        flash('Profiliniz başarıyla güncellendi.', 'success')
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    
    return render_template('auth/edit_profile.html', form=form)


@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Şifre değiştirme"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Şifreyi değiştir
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash('Şifreniz başarıyla değiştirildi.', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html', form=form)
