from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post, Comment
from app.utils.decorators import approved_user_required, permission_required
from datetime import datetime

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/')
def index():
    """Blog yazıları listesi"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    
    query = Post.query.filter_by(is_published=True)
    
    if category:
        query = query.filter_by(category=category)
    
    posts = query.order_by(Post.published_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Kategoriler
    categories = db.session.query(Post.category).filter(
        Post.is_published == True,
        Post.category != None
    ).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('blog/index.html',
                         posts=posts,
                         categories=categories,
                         current_category=category)


@bp.route('/<slug>')
def detail(slug):
    """Blog yazısı detay sayfası"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # Yayınlanmamış yazıyı sadece yazar veya yetkili görebilir
    if not post.is_published:
        if not current_user.is_authenticated or (post.author_id != current_user.id and not current_user.has_permission('edit_post')):
            abort(404)
    
    # Görüntülenme sayısını artır
    post.views += 1
    db.session.commit()
    
    # Yorumları getir - moderatörler tüm yorumları görebilir
    query = Comment.query.filter_by(
        post_id=post.id,
        is_deleted=False,
        parent_id=None
    )
    
    # Moderatör değilse sadece onaylı yorumları göster
    if not current_user.is_authenticated or not current_user.has_permission('moderate_comments'):
        query = query.filter_by(is_approved=True)
    
    comments = query.order_by(Comment.created_at.desc()).all()
    
    return render_template('blog/detail.html',
                         post=post,
                         comments=comments)


@bp.route('/<slug>/yorum-yap', methods=['POST'])
@login_required
@approved_user_required
def add_comment(slug):
    """Yorum ekle"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    content = request.form.get('content')
    parent_id = request.form.get('parent_id', type=int)
    
    if not content:
        flash('Yorum içeriği boş olamaz.', 'danger')
        return redirect(url_for('blog.detail', slug=slug))
    
    # Kara liste kontrolü
    from app.models import SiteSetting
    blacklist_setting = SiteSetting.query.filter_by(key='comment_blacklist').first()
    if blacklist_setting and blacklist_setting.value:
        blacklist = [word.strip().lower() for word in blacklist_setting.value.split(',')]
        content_lower = content.lower()
        
        # Yasaklı kelime kontrolü
        for word in blacklist:
            if word and word in content_lower:
                flash(f'Yorumunuz uygunsuz kelime içeriyor ve engellenmiştir.', 'danger')
                return redirect(url_for('blog.detail', slug=slug))
    
    # Otomatik onay ayarını kontrol et
    auto_approve_setting = SiteSetting.query.filter_by(key='comment_auto_approve').first()
    auto_approve = auto_approve_setting.value == 'true' if auto_approve_setting else False
    
    comment = Comment(
        content=content,
        post_id=post.id,
        author_id=current_user.id,
        parent_id=parent_id,
        is_approved=auto_approve
    )
    
    db.session.add(comment)
    db.session.commit()
    
    if auto_approve:
        flash('Yorumunuz başarıyla eklendi.', 'success')
    else:
        flash('Yorumunuz gönderildi. Onaylandıktan sonra görünür olacaktır.', 'success')
    
    return redirect(url_for('blog.detail', slug=slug) + f'#comment-{comment.id}')



@bp.route('/yorum/<int:id>/sil', methods=['POST'])
@login_required
def delete_comment(id):
    """Yorum sil"""
    comment = Comment.query.get_or_404(id)
    
    # Sadece yorum sahibi veya yetkili kişi silebilir
    if comment.author_id != current_user.id and not current_user.has_permission('moderate_comments'):
        abort(403)
    
    comment.is_deleted = True
    db.session.commit()
    
    flash('Yorum silindi.', 'info')
    return redirect(url_for('blog.detail', slug=comment.post.slug))


@bp.route('/yorum/<int:id>/onayla', methods=['POST'])
@login_required
@permission_required('moderate_comments')
def approve_comment(id):
    """Yorumu onayla"""
    comment = Comment.query.get_or_404(id)
    comment.is_approved = True
    db.session.commit()
    
    flash('Yorum onaylandı.', 'success')
    return redirect(url_for('blog.detail', slug=comment.post.slug))


@bp.route('/yorum/<int:id>/reddet', methods=['POST'])
@login_required
@permission_required('moderate_comments')
def reject_comment(id):
    """Yorumu reddet"""
    comment = Comment.query.get_or_404(id)
    comment.is_approved = False
    db.session.commit()
    
    flash('Yorum reddedildi.', 'info')
    return redirect(url_for('blog.detail', slug=comment.post.slug))


@bp.route('/yeni-yazi', methods=['GET', 'POST'])
@login_required
@permission_required('create_post')
def create_post():
    """Yeni yazı oluştur"""
    if request.method == 'POST':
        title = request.form.get('title')
        summary = request.form.get('summary')
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.get('tags')
        is_published = request.form.get('is_published') == 'on'
        is_featured = request.form.get('is_featured') == 'on'
        
        if not title or not content:
            flash('Başlık ve içerik zorunludur.', 'danger')
            return redirect(url_for('blog.create_post'))
        
        # Slug oluştur
        from app.utils.helpers import generate_slug
        slug = generate_slug(title)
        
        # Slug benzersiz mi kontrol et
        existing_post = Post.query.filter_by(slug=slug).first()
        if existing_post:
            slug = f"{slug}-{int(datetime.utcnow().timestamp())}"
        
        # Görsel yükleme
        featured_image = None
        if 'featured_image' in request.files:
            image = request.files['featured_image']
            if image and image.filename:
                from app.utils.helpers import save_picture, allowed_file
                if allowed_file(image.filename):
                    featured_image = save_picture(image, folder='posts', size=(1200, 630))
        
        post = Post(
            title=title,
            slug=slug,
            summary=summary,
            content=content,
            category=category,
            tags=tags,
            is_published=is_published,
            is_featured=is_featured,
            author_id=current_user.id,
            featured_image=featured_image,
            published_at=datetime.utcnow() if is_published else None
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Yazı başarıyla oluşturuldu.', 'success')
        return redirect(url_for('blog.detail', slug=post.slug))
    
    return render_template('blog/create.html')


@bp.route('/<slug>/duzenle', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    """Yazı düzenle"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # Sadece yazar veya yetkili kişi düzenleyebilir
    if post.author_id != current_user.id and not current_user.has_permission('edit_post'):
        abort(403)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.summary = request.form.get('summary')
        post.content = request.form.get('content')
        post.category = request.form.get('category')
        post.tags = request.form.get('tags')
        post.is_published = request.form.get('is_published') == 'on'
        post.is_featured = request.form.get('is_featured') == 'on'
        
        # Görsel güncelleme
        if 'featured_image' in request.files:
            image = request.files['featured_image']
            if image and image.filename:
                from app.utils.helpers import save_picture, delete_picture, allowed_file
                if allowed_file(image.filename):
                    # Eski görseli sil
                    if post.featured_image:
                        delete_picture(post.featured_image)
                    
                    post.featured_image = save_picture(image, folder='posts', size=(1200, 630))
        
        db.session.commit()
        
        flash('Yazı başarıyla güncellendi.', 'success')
        return redirect(url_for('blog.detail', slug=post.slug))
    
    return render_template('blog/edit.html', post=post)


@bp.route('/<slug>/sil', methods=['POST'])
@login_required
def delete_post(slug):
    """Yazı sil"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    # Sadece yazar veya yetkili kişi silebilir
    if post.author_id != current_user.id and not current_user.has_permission('delete_post'):
        abort(403)
    
    # Görseli sil
    if post.featured_image:
        from app.utils.helpers import delete_picture
        delete_picture(post.featured_image)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Yazı silindi.', 'info')
    return redirect(url_for('blog.index'))
