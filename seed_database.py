#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Veritabanını sıfırla ve seed verilerle doldur"""

from run import app, db, seed_db

if __name__ == '__main__':
    with app.app_context():
        print('🔄 Veritabanı sıfırlanıyor...')
        db.drop_all()
        db.create_all()
        print('✅ Veritabanı tabloları oluşturuldu.')
        
        print('🔄 Seed veriler ekleniyor...')
        seed_db()
        print('✅ Veritabanı başarıyla seed edildi!')
        print('\n📋 Giriş Bilgileri:')
        print('   Kullanıcı adı: root')
        print('   Şifre: Senveben12*')
        print('   E-posta: root@atakkulubu.com')
