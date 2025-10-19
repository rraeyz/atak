from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message='Kullanıcı adı gereklidir')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre gereklidir')
    ])
    remember = BooleanField('Beni Hatırla')


class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message='Kullanıcı adı gereklidir'),
        Length(min=3, max=80, message='Kullanıcı adı 3-80 karakter arasında olmalıdır')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta gereklidir'),
        Email(message='Geçerli bir e-posta adresi giriniz')
    ])
    first_name = StringField('Ad', validators=[
        DataRequired(message='Ad gereklidir'),
        Length(max=100, message='Ad en fazla 100 karakter olabilir')
    ])
    last_name = StringField('Soyad', validators=[
        DataRequired(message='Soyad gereklidir'),
        Length(max=100, message='Soyad en fazla 100 karakter olabilir')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre gereklidir'),
        Length(min=8, message='Şifre en az 8 karakter olmalıdır')
    ])
    confirm_password = PasswordField('Şifre Tekrarı', validators=[
        DataRequired(message='Şifre tekrarı gereklidir'),
        EqualTo('password', message='Şifreler eşleşmiyor')
    ])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu e-posta adresi zaten kayıtlı. Lütfen farklı bir e-posta adresi kullanın.')


class EditProfileForm(FlaskForm):
    first_name = StringField('Ad', validators=[
        DataRequired(message='Ad gereklidir'),
        Length(max=100, message='Ad en fazla 100 karakter olabilir')
    ])
    last_name = StringField('Soyad', validators=[
        DataRequired(message='Soyad gereklidir'),
        Length(max=100, message='Soyad en fazla 100 karakter olabilir')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta gereklidir'),
        Email(message='Geçerli bir e-posta adresi giriniz')
    ])
    bio = TextAreaField('Hakkında', validators=[
        Length(max=500, message='Hakkında en fazla 500 karakter olabilir')
    ])
    avatar = FileField('Profil Resmi', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Sadece resim dosyaları yüklenebilir (jpg, png, gif)')
    ])

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Bu e-posta adresi zaten kullanılıyor.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Mevcut Şifre', validators=[
        DataRequired(message='Mevcut şifre gereklidir')
    ])
    new_password = PasswordField('Yeni Şifre', validators=[
        DataRequired(message='Yeni şifre gereklidir'),
        Length(min=8, message='Şifre en az 8 karakter olmalıdır')
    ])
    confirm_password = PasswordField('Yeni Şifre Tekrarı', validators=[
        DataRequired(message='Şifre tekrarı gereklidir'),
        EqualTo('new_password', message='Şifreler eşleşmiyor')
    ])


class ContactForm(FlaskForm):
    name = StringField('Ad Soyad', validators=[
        DataRequired(message='Ad soyad gereklidir'),
        Length(max=100, message='Ad soyad en fazla 100 karakter olabilir')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta gereklidir'),
        Email(message='Geçerli bir e-posta adresi giriniz')
    ])
    subject = StringField('Konu', validators=[
        DataRequired(message='Konu gereklidir'),
        Length(max=200, message='Konu en fazla 200 karakter olabilir')
    ])
    message = TextAreaField('Mesaj', validators=[
        DataRequired(message='Mesaj gereklidir'),
        Length(min=10, message='Mesaj en az 10 karakter olmalıdır')
    ])
