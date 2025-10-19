from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def permission_required(permission_name):
    """İzin kontrolü decorator'ı"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not current_user.is_approved:
                flash('Hesabınız henüz onaylanmamış. Lütfen yönetici onayını bekleyin.', 'warning')
                return redirect(url_for('main.index'))
            
            if not current_user.has_permission(permission_name):
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def role_required(role_name):
    """Rol kontrolü decorator'ı"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not current_user.has_role(role_name):
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Admin kontrolü decorator'ı"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.has_role('admin'):
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def approved_user_required(f):
    """Onaylı kullanıcı kontrolü decorator'ı"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_approved:
            flash('Hesabınız henüz onaylanmamış. Lütfen yönetici onayını bekleyin.', 'warning')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function
