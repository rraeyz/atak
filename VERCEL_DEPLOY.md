# Vercel Deployment Rehberi

## 1. Vercel CLI Kurun
```powershell
npm install -g vercel
```

## 2. Login
```powershell
vercel login
```

## 3. Deploy
```powershell
cd C:\Users\rraey\OneDrive\Desktop\Projeler\atak
vercel
```

İlk deployment'ta soruları yanıtlayın:
- Set up and deploy? **Y**
- Which scope? (Hesabınızı seçin)
- Link to existing project? **N**
- Project name? **atak-kulubu**
- Directory? **./app**
- Override settings? **N**

## 4. Production Deploy
```powershell
vercel --prod
```

Siteniz hazır: `https://atak-kulubu.vercel.app`

## NOT: Vercel SQLite desteklemiyor
PostgreSQL veya başka bir veritabanı kullanmanız gerekecek.
