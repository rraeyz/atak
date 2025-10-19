"""QR Kod üretme ve yönetme modülü"""
import qrcode
import os
import secrets
from io import BytesIO
from datetime import datetime


def generate_unique_code():
    """Benzersiz QR kod string üret"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = secrets.token_hex(16)
    return f"ATAK-{timestamp}-{random_part}"


def generate_qr_code(data, filename=None):
    """
    QR kod resmi oluştur
    
    Args:
        data: QR kodda saklanacak veri
        filename: Kayıt edilecek dosya adı (opsiyonel)
    
    Returns:
        QR kod resmi yolu veya BytesIO nesnesi
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    if filename:
        # Dosya olarak kaydet
        upload_folder = os.path.join('app', 'static', 'uploads', 'qr_codes')
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        img.save(filepath)
        # Sadece uploads klasöründen sonraki yolu döndür (url_for ile kullanmak için)
        return f"uploads/qr_codes/{filename}"
    else:
        # BytesIO olarak döndür
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer


def generate_event_qr_code(user_id, event_id, registration_id):
    """
    Etkinlik için QR kod oluştur
    
    Args:
        user_id: Kullanıcı ID
        event_id: Etkinlik ID
        registration_id: Kayıt ID
    
    Returns:
        (qr_code_string, qr_image_path)
    """
    # Benzersiz kod oluştur
    code = generate_unique_code()
    
    # QR kod verisi: kod|kullanıcı_id|etkinlik_id|kayıt_id
    qr_data = f"{code}|{user_id}|{event_id}|{registration_id}"
    
    # Dosya adı
    filename = f"event_{event_id}_user_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    
    # QR kod oluştur
    qr_image_path = generate_qr_code(qr_data, filename)
    
    return code, qr_image_path


def decode_qr_code_data(qr_data):
    """
    QR kod verisini çöz
    
    Args:
        qr_data: QR koddan okunan veri string
    
    Returns:
        dict: {'code': str, 'user_id': int, 'event_id': int, 'registration_id': int}
        veya None (geçersiz format)
    """
    try:
        parts = qr_data.split('|')
        if len(parts) != 4:
            return None
        
        return {
            'code': parts[0],
            'user_id': int(parts[1]),
            'event_id': int(parts[2]),
            'registration_id': int(parts[3])
        }
    except (ValueError, IndexError):
        return None
