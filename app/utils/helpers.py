from datetime import datetime
import os
import secrets
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

def format_datetime(value, format='%d.%m.%Y %H:%M'):
    """Tarih formatla"""
    if value is None:
        return ""
    return value.strftime(format)


def allowed_file(filename):
    """Dosya uzantısı kontrol et"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_picture(form_picture, folder='general', size=(800, 800)):
    """Resim kaydet ve yolu döndür"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, picture_fn)
    
    # Klasör yoksa oluştur
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    # Resmi yeniden boyutlandır
    output_size = size
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return os.path.join(folder, picture_fn)


def delete_picture(picture_path):
    """Resmi sil"""
    if picture_path and picture_path != 'default-avatar.png':
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_path)
        if os.path.exists(full_path):
            os.remove(full_path)


def generate_slug(title):
    """Başlıktan slug oluştur"""
    import re
    from unidecode import unidecode
    
    # Türkçe karakterleri dönüştür
    title = unidecode(title)
    # Küçük harfe çevir
    title = title.lower()
    # Özel karakterleri kaldır
    title = re.sub(r'[^\w\s-]', '', title)
    # Boşlukları tire ile değiştir
    title = re.sub(r'[\s_]+', '-', title)
    # Birden fazla tireyi tek tireye düşür
    title = re.sub(r'-+', '-', title)
    # Baş ve sondaki tireleri kaldır
    title = title.strip('-')
    
    return title or 'untitled'
