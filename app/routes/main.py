from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import Event, Post, SiteSetting, ContactMessage, User, Announcement
from app.forms import ContactForm
from app import db
from datetime import datetime
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Ana sayfa"""
    now = datetime.now()
    
    # Yaklaşan etkinlikler
    upcoming_events = Event.query.filter(
        Event.is_published == True,
        Event.event_date > now
    ).order_by(Event.event_date.asc()).limit(3).all()
    
    # Öne çıkan yazılar
    featured_posts = Post.query.filter_by(
        is_published=True,
        is_featured=True
    ).order_by(Post.published_at.desc()).limit(3).all()
    
    # Son yazılar
    recent_posts = Post.query.filter_by(
        is_published=True
    ).order_by(Post.created_at.desc()).limit(6).all()
    
    # Duyurular (kullanıcıya göre filtrele)
    announcements = []
    if current_user.is_authenticated:
        all_announcements = Announcement.query.filter_by(is_published=True).order_by(Announcement.created_at.desc()).all()
        announcements = [a for a in all_announcements if a.is_visible_to_user(current_user)]
    
    # İstatistikler
    stats = {
        'total_members': User.query.filter_by(is_approved=True).count(),
        'total_events': Event.query.filter_by(is_published=True).count(),
        'total_posts': Post.query.filter_by(is_published=True).count()
    }
    
    return render_template('main/index.html',
                         upcoming_events=upcoming_events,
                         recent_posts=recent_posts,
                         announcements=announcements,
                         stats=stats,
                         now=now)


@bp.route('/hakkimizda')
def about():
    """Hakkımızda sayfası"""
    return render_template('main/about.html')


@bp.route('/iletisim', methods=['GET', 'POST'])
def contact():
    """İletişim sayfası"""
    form = ContactForm()
    
    if form.validate_on_submit():
        contact_message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        
        db.session.add(contact_message)
        db.session.commit()
        
        flash('Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('main/contact.html', form=form)


# Context processor __init__.py'ye taşındı - site ayarları otomatik yükleniyor

