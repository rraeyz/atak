"""Etkinlik raporu oluşturma modülü"""
import csv
from io import StringIO
from datetime import datetime
from app.models import Event, EventRegistration, CheckIn, QRCode


def generate_event_report(event_id):
    """
    Etkinlik için detaylı rapor oluştur
    
    Args:
        event_id: Etkinlik ID
    
    Returns:
        dict: Rapor verileri
    """
    event = Event.query.get_or_404(event_id)
    
    # Tüm kayıtları al
    registrations = EventRegistration.query.filter_by(
        event_id=event_id,
        status='approved'
    ).all()
    
    # Check-in verilerini al
    check_ins = CheckIn.query.filter_by(event_id=event_id).all()
    check_in_user_ids = [ci.user_id for ci in check_ins]
    
    # Rapor verileri
    report_data = {
        'event': event,
        'total_registered': len(registrations),
        'total_attended': len(check_ins),
        'total_not_attended': len(registrations) - len(check_ins),
        'attendance_rate': (len(check_ins) / len(registrations) * 100) if registrations else 0,
        'registrations': [],
        'check_ins': check_ins,
        'generated_at': datetime.now()
    }
    
    # Kayıt detayları
    for reg in registrations:
        attended = reg.user_id in check_in_user_ids
        check_in = next((ci for ci in check_ins if ci.user_id == reg.user_id), None)
        
        # Template'in beklediği formatta: doğrudan registration objesi + ek alanlar
        # Registration objesine dinamik olarak ek alanlar ekliyoruz
        # attendance zaten model'de var ama güncel olmayabilir, o yüzden override ediyoruz
        reg.attendance = attended
        # Template check_ins[0] şeklinde erişiyor, o yüzden liste olarak veriyoruz
        reg.check_ins = [check_in] if check_in else []
        
        report_data['registrations'].append(reg)
    
    return report_data


def generate_csv_report(event_id):
    """
    Etkinlik için CSV raporu oluştur
    
    Args:
        event_id: Etkinlik ID
    
    Returns:
        str: CSV içeriği (UTF-8 BOM ile)
    """
    report = generate_event_report(event_id)
    
    output = StringIO()
    # UTF-8 BOM ekle (Excel için Türkçe karakter desteği)
    output.write('\ufeff')
    writer = csv.writer(output)
    
    # Başlıklar
    writer.writerow([
        'Kullanıcı Adı',
        'Ad Soyad',
        'E-posta',
        'Kayıt Tarihi',
        'Katıldı mı?',
        'Giriş Tarihi',
        'Giriş Yapan Görevli'
    ])
    
    # Veriler
    for reg in report['registrations']:
        # Artık reg doğrudan EventRegistration objesi
        user = reg.user
        check_in = reg.check_ins[0] if reg.check_ins else None
        
        writer.writerow([
            user.username,
            f"{user.first_name} {user.last_name}",
            user.email,
            reg.registered_at.strftime('%d.%m.%Y %H:%M'),
            'Evet' if reg.attendance else 'Hayır',
            check_in.checked_in_at.strftime('%d.%m.%Y %H:%M') if check_in else '-',
            check_in.security_staff.username if check_in and check_in.security_staff else '-'
        ])
    
    # Özet bilgiler
    writer.writerow([])
    writer.writerow(['ÖZET'])
    writer.writerow(['Toplam Kayıt', report['total_registered']])
    writer.writerow(['Katılan', report['total_attended']])
    writer.writerow(['Katılmayan', report['total_not_attended']])
    writer.writerow(['Katılım Oranı', f"%{report['attendance_rate']:.2f}"])
    writer.writerow(['Rapor Tarihi', report['generated_at'].strftime('%d.%m.%Y %H:%M')])
    
    return output.getvalue()


def get_event_statistics(event_id):
    """
    Etkinlik istatistiklerini al
    
    Args:
        event_id: Etkinlik ID
    
    Returns:
        dict: İstatistik verileri
    """
    event = Event.query.get_or_404(event_id)
    
    total_registered = EventRegistration.query.filter_by(
        event_id=event_id,
        status='approved'
    ).count()
    
    total_checked_in = CheckIn.query.filter_by(
        event_id=event_id,
        status='checked_in'
    ).count()
    
    not_registered_entries = CheckIn.query.filter_by(
        event_id=event_id,
        status='not_registered'
    ).count()
    
    return {
        'event_id': event_id,
        'event_title': event.title,
        'total_registered': total_registered,
        'total_checked_in': total_checked_in,
        'total_attended': total_checked_in,  # Alias for template compatibility
        'total_not_attended': total_registered - total_checked_in,
        'not_registered_entries': not_registered_entries,
        'attendance_rate': (total_checked_in / total_registered * 100) if total_registered else 0
    }
