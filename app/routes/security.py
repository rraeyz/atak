"""Güvenlik görevlileri için QR kod okutma route'ları"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Event, QRCode, CheckIn, EventRegistration, User
from app.utils.decorators import permission_required
from app.utils.qr_generator import decode_qr_code_data
from datetime import datetime

bp = Blueprint('security', __name__, url_prefix='/guvenlik')


@bp.route('/')
@login_required
@permission_required('scan_qr_codes')
def index():
    """Güvenlik ana sayfa - Aktif etkinlikler"""
    # Bugünkü ve gelecekteki etkinlikler
    events = Event.query.filter(
        Event.event_date >= datetime.now().date()
    ).order_by(Event.event_date.asc()).all()
    
    return render_template('security/index.html', events=events)


@bp.route('/etkinlik/<int:event_id>')
@login_required
@permission_required('scan_qr_codes')
def event_scanner(event_id):
    """QR kod okutma sayfası"""
    event = Event.query.get_or_404(event_id)
    
    # Etkinlik istatistikleri
    total_registered = EventRegistration.query.filter_by(
        event_id=event_id,
        status='approved'
    ).count()
    
    total_checked_in = CheckIn.query.filter_by(
        event_id=event_id
    ).count()
    
    stats = {
        'total_registered': total_registered,
        'checked_in': total_checked_in,
        'remaining': total_registered - total_checked_in
    }
    
    # Son check-in'ler
    recent_checkins = CheckIn.query.filter_by(
        event_id=event_id
    ).order_by(CheckIn.checked_in_at.desc()).limit(10).all()
    
    return render_template('security/scanner.html', 
                         event=event,
                         stats=stats,
                         recent_checkins=recent_checkins)


@bp.route('/qr-okut', methods=['POST'])
@login_required
@permission_required('scan_qr_codes')
def scan_qr():
    """QR kod okut ve giriş kaydet"""
    qr_data = request.json.get('qr_data')
    event_id = request.json.get('event_id')
    
    if not qr_data or not event_id:
        return jsonify({
            'success': False,
            'message': 'Geçersiz istek.'
        }), 400
    
    # QR kodu çöz
    decoded = decode_qr_code_data(qr_data)
    
    if not decoded:
        return jsonify({
            'success': False,
            'message': 'Geçersiz QR kod formatı.',
            'status': 'invalid_format'
        }), 400
    
    # QR kodu veritabanında bul
    qr_code = QRCode.query.filter_by(code=decoded['code']).first()
    
    if not qr_code:
        return jsonify({
            'success': False,
            'message': 'QR kod bulunamadı.',
            'status': 'not_found'
        }), 404
    
    # QR kod aktif mi?
    if not qr_code.is_active:
        return jsonify({
            'success': False,
            'message': 'Bu QR kod devre dışı bırakılmış.',
            'status': 'inactive'
        }), 400
    
    # Etkinlik kontrolü
    if qr_code.event_id != int(event_id):
        return jsonify({
            'success': False,
            'message': 'Bu QR kod başka bir etkinlik için geçerli.',
            'status': 'wrong_event',
            'event_title': qr_code.event.title
        }), 400
    
    # Daha önce giriş yapılmış mı?
    existing_checkin = CheckIn.query.filter_by(
        event_id=event_id,
        user_id=qr_code.user_id
    ).first()
    
    if existing_checkin:
        user_name = f'{qr_code.user.first_name} {qr_code.user.last_name}'.strip() if qr_code.user.first_name or qr_code.user.last_name else qr_code.user.username
        return jsonify({
            'success': False,
            'message': f'{user_name} zaten giriş yapmış.',
            'status': 'already_checked_in',
            'user': {
                'first_name': qr_code.user.first_name,
                'last_name': qr_code.user.last_name,
                'username': qr_code.user.username,
                'email': qr_code.user.email,
                'checked_in_at': existing_checkin.checked_in_at.strftime('%d.%m.%Y %H:%M')
            }
        }), 400
    
    # Kayıt var mı kontrol et
    registration = EventRegistration.query.filter_by(
        event_id=event_id,
        user_id=qr_code.user_id
    ).first()
    
    if not registration or registration.status != 'approved':
        # Kayıt yok - yine de giriş yap ama işaretle
        check_in = CheckIn(
            event_id=event_id,
            user_id=qr_code.user_id,
            qr_code_id=qr_code.id,
            status='not_registered',
            checked_in_by=current_user.id,
            notes='Etkinliğe kaydı yok, QR kod ile giriş yapıldı.'
        )
        db.session.add(check_in)
        db.session.commit()
        
        user_name = f'{qr_code.user.first_name} {qr_code.user.last_name}'.strip() if qr_code.user.first_name or qr_code.user.last_name else qr_code.user.username
        return jsonify({
            'success': True,
            'warning': True,
            'message': f'⚠️ {user_name} etkinliğe kayıtlı değil, ancak giriş yapıldı.',
            'status': 'not_registered',
            'user': {
                'first_name': qr_code.user.first_name,
                'last_name': qr_code.user.last_name,
                'username': qr_code.user.username,
                'email': qr_code.user.email
            }
        })
    
    # Normal giriş
    check_in = CheckIn(
        event_id=event_id,
        user_id=qr_code.user_id,
        qr_code_id=qr_code.id,
        status='checked_in',
        checked_in_by=current_user.id
    )
    
    # QR kodu kullanıldı olarak işaretle
    qr_code.used = True
    qr_code.used_at = datetime.utcnow()
    
    # Katılım kaydını güncelle
    registration.attendance = True
    
    db.session.add(check_in)
    db.session.commit()
    
    user_name = f'{qr_code.user.first_name} {qr_code.user.last_name}'.strip() if qr_code.user.first_name or qr_code.user.last_name else qr_code.user.username
    return jsonify({
        'success': True,
        'message': f'✓ {user_name} başarıyla giriş yaptı!',
        'status': 'success',
        'user': {
            'first_name': qr_code.user.first_name,
            'last_name': qr_code.user.last_name,
            'username': qr_code.user.username,
            'email': qr_code.user.email
        }
    })


@bp.route('/manuel-giris/<int:event_id>', methods=['POST'])
@login_required
@permission_required('scan_qr_codes')
def manual_checkin(event_id):
    """Manuel giriş (QR kodsuz)"""
    # Hem 'search' hem 'user_identifier' parametrelerini kontrol et
    username_or_email = request.args.get('search') or request.form.get('search') or request.form.get('user_identifier')
    
    if not username_or_email:
        return jsonify({
            'success': False,
            'message': 'Kullanıcı adı veya e-posta giriniz.'
        }), 400
    
    # Kullanıcıyı bul
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'Kullanıcı bulunamadı.'
        }), 404
    
    # Daha önce giriş yapmış mı?
    existing_checkin = CheckIn.query.filter_by(
        event_id=event_id,
        user_id=user.id
    ).first()
    
    if existing_checkin:
        user_name = f'{user.first_name} {user.last_name}'.strip() if user.first_name or user.last_name else user.username
        return jsonify({
            'success': False,
            'message': f'{user_name} zaten giriş yapmış.'
        }), 400
    
    # Kayıt kontrolü
    registration = EventRegistration.query.filter_by(
        event_id=event_id,
        user_id=user.id,
        status='approved'
    ).first()
    
    status = 'checked_in' if registration else 'not_registered'
    notes = 'Manuel giriş' if registration else 'Kayıtsız - Manuel giriş'
    
    # Giriş kaydet
    check_in = CheckIn(
        event_id=event_id,
        user_id=user.id,
        status=status,
        checked_in_by=current_user.id,
        notes=notes
    )
    
    db.session.add(check_in)
    
    if registration:
        registration.attendance = True
    
    db.session.commit()
    
    user_name = f'{user.first_name} {user.last_name}'.strip() if user.first_name or user.last_name else user.username
    
    # JSON response dön
    return jsonify({
        'success': True,
        'message': f'✓ {user_name} başarıyla giriş yaptı!' if registration else f'⚠️ {user_name} kayıtsız olarak giriş yaptı.',
        'user': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email
        },
        'status': status
    })
