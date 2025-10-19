from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Event, EventRegistration, QRCode
from app.utils.decorators import approved_user_required
from datetime import datetime
from app.utils.qr_generator import generate_event_qr_code

bp = Blueprint('events', __name__, url_prefix='/etkinlikler')

@bp.route('/')
def index():
    """Etkinlikler listesi"""
    now = datetime.now()
    
    # Yaklaşan etkinlikler
    upcoming_events = Event.query.filter(
        Event.is_published == True,
        Event.event_date > now
    ).order_by(Event.event_date.asc()).all()
    
    # Geçmiş etkinlikler
    past_events = Event.query.filter(
        Event.is_published == True,
        Event.event_date <= now
    ).order_by(Event.event_date.desc()).all()
    
    return render_template('events/index.html',
                         upcoming_events=upcoming_events,
                         past_events=past_events,
                         now=now)


@bp.route('/<int:id>')
def detail(id):
    """Etkinlik detay sayfası"""
    event = Event.query.get_or_404(id)
    now = datetime.now()
    
    # Kullanıcının kayıt durumu (iptal edilmemiş kayıt)
    user_registration = None
    if current_user.is_authenticated:
        user_registration = EventRegistration.query.filter_by(
            event_id=id,
            user_id=current_user.id
        ).filter(EventRegistration.status != 'cancelled').first()
    
    return render_template('events/detail.html',
                         event=event,
                         user_registration=user_registration,
                         now=now)


@bp.route('/<int:id>/kayit-ol', methods=['POST'])
@login_required
@approved_user_required
def register(id):
    """Etkinliğe kayıt ol"""
    event = Event.query.get_or_404(id)
    
    # Kayıt kontrolü
    if not event.is_registration_open:
        flash('Bu etkinlik için kayıt kabul edilmiyor.', 'warning')
        return redirect(url_for('events.detail', id=id))
    
    if event.is_full:
        flash('Bu etkinlik dolu.', 'warning')
        return redirect(url_for('events.detail', id=id))
    
    if event.registration_deadline and event.registration_deadline < datetime.utcnow():
        flash('Kayıt süresi dolmuş.', 'warning')
        return redirect(url_for('events.detail', id=id))
    
    # Daha önce kayıt olmuş mu? (İptal edilmemiş kayıt var mı?)
    existing_registration = EventRegistration.query.filter_by(
        event_id=id,
        user_id=current_user.id
    ).filter(EventRegistration.status != 'cancelled').first()
    
    if existing_registration:
        # Eğer zaten kayıtlıysa fakat QR kodu yoksa, eksikse oluştur
        from app.models import QRCode as _QRCodeModel
        qr_code_existing = _QRCodeModel.query.filter_by(registration_id=existing_registration.id).first()
        if not qr_code_existing:
            try:
                code, qr_image_path = generate_event_qr_code(
                    current_user.id,
                    event.id,
                    existing_registration.id
                )
                print(f"🔧 (existing) QR Kod Debug:")
                print(f"  Code: {code}")
                print(f"  Image Path: {qr_image_path}")

                qr_code_new = _QRCodeModel(
                    user_id=current_user.id,
                    event_id=event.id,
                    registration_id=existing_registration.id,
                    code=code,
                    qr_image_path=qr_image_path
                )
                db.session.add(qr_code_new)
                db.session.commit()
                print(f"✅ (existing) QR kod veritabanına kaydedildi: {qr_code_new.qr_image_path}")
                flash('Bu etkinliğe zaten kayıtlısınız. Eksik QR kodunuz oluşturuldu!', 'success')
            except Exception as e:
                print(f"❌ (existing) QR kod oluşturma hatası: {e}")
                import traceback
                traceback.print_exc()
                flash('Bu etkinliğe zaten kayıtlısınız ancak QR kod oluşturulamadı. Lütfen yöneticiye bildirin.', 'warning')
        else:
            flash('Bu etkinliğe zaten kayıtlısınız.', 'info')
        
        return redirect(url_for('events.detail', id=id))
    
    # İptal edilmiş bir kayıt var mı? Varsa yeniden aktif hale getir
    cancelled_registration = EventRegistration.query.filter_by(
        event_id=id,
        user_id=current_user.id,
        status='cancelled'
    ).first()
    
    if cancelled_registration:
        # Mevcut iptal edilmiş kaydı yeniden aktif hale getir
        cancelled_registration.status = 'approved'
        cancelled_registration.registered_at = datetime.utcnow()
        db.session.commit()
        
        # Aktifleştirildikten sonra QR kodu oluştur (eğer yoksa)
        qr_reactivated = False
        try:
            from app.models import QRCode as _QRCodeModel
            qr_code_existing = _QRCodeModel.query.filter_by(registration_id=cancelled_registration.id).first()
            if not qr_code_existing:
                code, qr_image_path = generate_event_qr_code(
                    current_user.id,
                    event.id,
                    cancelled_registration.id
                )
                print(f"🔧 (reactivated) QR Kod Debug:")
                print(f"  Code: {code}")
                print(f"  Image Path: {qr_image_path}")

                qr_code_new = _QRCodeModel(
                    user_id=current_user.id,
                    event_id=event.id,
                    registration_id=cancelled_registration.id,
                    code=code,
                    qr_image_path=qr_image_path
                )
                db.session.add(qr_code_new)
                db.session.commit()
                print(f"✅ (reactivated) QR kod veritabanına kaydedildi: {qr_code_new.qr_image_path}")
                qr_reactivated = True
            else:
                qr_reactivated = True  # QR zaten var
        except Exception as e:
            print(f"❌ (reactivated) QR kod oluşturma hatası: {e}")
            import traceback
            traceback.print_exc()
            flash('Etkinliğe yeniden kayıt oldunuz ancak QR kod oluşturulamadı. Lütfen yöneticiye bildirin.', 'warning')
            return redirect(url_for('events.detail', id=id))

        if qr_reactivated:
            flash('Etkinliğe yeniden kayıt oldunuz! QR kodunuzu profil sayfanızdan görebilirsiniz.', 'success')
        
        return redirect(url_for('events.detail', id=id))
    
    # Yeni kayıt
    notes = request.form.get('notes')
    registration = EventRegistration(
        event_id=id,
        user_id=current_user.id,
        status='approved',  # Otomatik onay
        notes=notes
    )
    
    db.session.add(registration)
    db.session.commit()
    
    # QR kod oluştur
    qr_created = False
    try:
        code, qr_image_path = generate_event_qr_code(
            current_user.id,
            event.id,
            registration.id
        )
        
        # Debug log
        print(f"🔧 QR Kod Debug:")
        print(f"  Code: {code}")
        print(f"  Image Path: {qr_image_path}")
        
        qr_code = QRCode(
            user_id=current_user.id,
            event_id=event.id,
            registration_id=registration.id,
            code=code,
            qr_image_path=qr_image_path
        )
        db.session.add(qr_code)
        db.session.commit()
        
        print(f"✅ QR kod veritabanına kaydedildi: {qr_code.qr_image_path}")
        qr_created = True
    except Exception as e:
        print(f"❌ QR kod oluşturma hatası: {e}")
        import traceback
        traceback.print_exc()
        # Hata durumunda kullanıcıyı bilgilendir
        flash('Etkinliğe kayıt oldunuz ancak QR kod oluşturulamadı. Lütfen yöneticiye bildirin.', 'warning')
        return redirect(url_for('events.detail', id=id))
    
    if qr_created:
        flash('Etkinliğe başarıyla kayıt oldunuz! QR kodunuzu profil sayfanızdan görebilirsiniz.', 'success')
    
    return redirect(url_for('events.detail', id=id))


@bp.route('/<int:id>/kayit-iptal', methods=['POST'])
@login_required
def cancel_registration(id):
    """Etkinlik kaydını iptal et"""
    registration = EventRegistration.query.filter_by(
        event_id=id,
        user_id=current_user.id
    ).first_or_404()
    
    registration.status = 'cancelled'
    db.session.commit()
    
    flash('Etkinlik kaydınız iptal edildi.', 'info')
    return redirect(url_for('events.detail', id=id))


@bp.route('/kayitlarim')
@login_required
def my_registrations():
    """Kullanıcının kayıtlı olduğu etkinlikler"""
    registrations = EventRegistration.query.filter_by(
        user_id=current_user.id
    ).order_by(EventRegistration.registered_at.desc()).all()
    
    return render_template('events/my_registrations.html',
                         registrations=registrations,
                         now=datetime.now())


# ===== ADMIN: ETKİNLİK YÖNETİMİ =====

@bp.route('/yeni', methods=['GET', 'POST'])
@login_required
def create():
    """Yeni etkinlik oluştur"""
    from app.utils.decorators import permission_required
    
    if not current_user.has_permission('create_event'):
        abort(403)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')
        location = request.form.get('location')
        organizer = request.form.get('organizer')
        event_date = request.form.get('event_date')
        end_date = request.form.get('end_date')
        registration_deadline = request.form.get('registration_deadline')
        max_participants = request.form.get('max_participants', type=int)
        is_published = request.form.get('is_published') == 'on'
        is_featured = request.form.get('is_featured') == 'on'
        is_registration_open = request.form.get('is_registration_open') == 'on'
        event_type = request.form.get('event_type')
        
        if not title or not event_date:
            flash('Başlık ve etkinlik tarihi zorunludur.', 'danger')
            return redirect(url_for('events.create'))
        
        # Tarihleri datetime'a çevir
        try:
            event_date = datetime.fromisoformat(event_date)
            end_date = datetime.fromisoformat(end_date) if end_date else None
            registration_deadline = datetime.fromisoformat(registration_deadline) if registration_deadline else None
        except ValueError:
            flash('Geçersiz tarih formatı.', 'danger')
            return redirect(url_for('events.create'))
        
        event = Event(
            title=title,
            description=description,
            content=content,
            location=location,
            organizer=organizer or current_user.get_full_name(),
            event_date=event_date,
            end_date=end_date,
            registration_deadline=registration_deadline,
            max_participants=max_participants,
            is_published=is_published,
            is_featured=is_featured,
            is_registration_open=is_registration_open,
            event_type=event_type,
            created_by=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Etkinlik başarıyla oluşturuldu!', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('events/create.html')


@bp.route('/<int:id>/duzenle', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Etkinlik düzenle"""
    if not current_user.has_permission('edit_event'):
        abort(403)
    
    event = Event.query.get_or_404(id)
    
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event.content = request.form.get('content')
        event.location = request.form.get('location')
        event.organizer = request.form.get('organizer')
        event.is_published = request.form.get('is_published') == 'on'
        event.is_featured = request.form.get('is_featured') == 'on'
        event.is_registration_open = request.form.get('is_registration_open') == 'on'
        event.event_type = request.form.get('event_type')
        event.max_participants = request.form.get('max_participants', type=int)
        
        # Tarihleri güncelle
        event_date = request.form.get('event_date')
        end_date = request.form.get('end_date')
        registration_deadline = request.form.get('registration_deadline')
        
        try:
            if event_date:
                event.event_date = datetime.fromisoformat(event_date)
            if end_date:
                event.end_date = datetime.fromisoformat(end_date)
            if registration_deadline:
                event.registration_deadline = datetime.fromisoformat(registration_deadline)
        except ValueError:
            flash('Geçersiz tarih formatı.', 'danger')
            return redirect(url_for('events.edit', id=id))
        
        db.session.commit()
        
        flash('Etkinlik başarıyla güncellendi!', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('events/edit.html', event=event)


@bp.route('/<int:id>/sil', methods=['POST'])
@login_required
def delete(id):
    """Etkinlik sil"""
    if not current_user.has_permission('delete_event'):
        abort(403)
    
    event = Event.query.get_or_404(id)
    
    db.session.delete(event)
    db.session.commit()
    
    flash('Etkinlik başarıyla silindi.', 'success')
    return redirect(url_for('admin.events'))


@bp.route('/qr-kodum/<int:registration_id>')
@login_required
@approved_user_required
def my_qr_code(registration_id):
    """Kullanıcının QR kodunu göster"""
    registration = EventRegistration.query.get_or_404(registration_id)
    
    # Sadece kendi QR kodunu görebilir
    if registration.user_id != current_user.id:
        abort(403)
    
    # QR kodu var mı?
    qr_code = QRCode.query.filter_by(registration_id=registration_id).first()
    
    if not qr_code:
        flash('QR kod bulunamadı.', 'warning')
        return redirect(url_for('events.my_registrations'))
    
    return render_template('events/qr_code.html', 
                         qr_code=qr_code, 
                         registration=registration,
                         event=registration.event)
