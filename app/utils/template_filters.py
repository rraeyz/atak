from datetime import datetime


def format_datetime(value, format='%d.%m.%Y %H:%M'):
    """Tarih formatla - Jinja2 filtresi için"""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except:
            return value
    return value.strftime(format)
