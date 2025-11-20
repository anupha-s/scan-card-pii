# คู่มือการ Deploy Thai ID Card Scanner

## 🎯 สรุปแนวทางที่แนะนำ

เนื่องจาก Vercel ไม่รองรับ Tesseract OCR และ OpenCV ในแบบ Serverless Functions แนวทางที่ดีที่สุดคือ:

**Frontend (Static) → Vercel**  
**Backend (Python + Tesseract) → Railway/Render**

---

## 📦 ทางเลือกที่ 1: Deploy ทั้งหมดบน Railway (แนะนำ)

### ขั้นตอน

1. **สร้าง Project บน Railway**
   - เชื่อมต่อ GitHub repo
   - Railway จะ detect Python และติดตั้งทุกอย่างอัตโนมัติ

2. **ตั้งค่า Static Files**
   แก้ไข `app.py` เพิ่ม route สำหรับ index.html:
   ```python
   from flask import send_from_directory
   
   @app.route('/')
   def index():
       return send_from_directory('.', 'index.html')
   ```

3. **Deploy**
   - Push code ไปยัง GitHub
   - Railway จะ deploy อัตโนมัติ

4. **เข้าใช้งาน**
   - `https://your-app.railway.app`

---

## 📦 ทางเลือกที่ 2: Render (Free Tier)

### ขั้นตอน

1. **สร้างบัญชี Render**
   - ไปที่ https://render.com
   - Sign up ด้วย GitHub

2. **สร้าง Web Service ใหม่**
   - คลิก "New +" → "Web Service"
   - เชื่อมต่อ repository

3. **ตั้งค่า Build & Deploy**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

4. **เพิ่ม Environment Variables**
   ```
   PYTHON_VERSION=3.10
   ```

5. **ติดตั้ง Tesseract**
   สร้างไฟล์ `render.yaml`:
   ```yaml
   services:
     - type: web
       name: thai-id-scanner
       env: python
       buildCommand: |
         apt-get update
         apt-get install -y tesseract-ocr tesseract-ocr-tha
         pip install -r requirements.txt
       startCommand: python app.py
   ```

---

## 📦 ทางเลือกที่ 3: Heroku

### ขั้นตอน

1. **ติดตั้ง Heroku CLI**
   ```bash
   npm install -g heroku
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **สร้าง App**
   ```bash
   heroku create your-app-name
   ```

4. **เพิ่ม Buildpacks**
   ```bash
   heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
   heroku buildpacks:add --index 2 heroku/python
   ```

5. **สร้างไฟล์ Aptfile**
   ```
   tesseract-ocr
   tesseract-ocr-tha
   tesseract-ocr-eng
   ```

6. **สร้างไฟล์ Procfile**
   ```
   web: python app.py
   ```

7. **Deploy**
   ```bash
   git push heroku main
   ```

---

## 🧪 ทดสอบหลัง Deploy

### ทดสอบ Backend

```bash
# Health Check
curl https://your-backend-url/api/health

# ทดสอบด้วย Python script
python test_api.py path/to/test-card.jpg
```

### ทดสอบ Frontend

1. เปิด browser ไปที่ URL ที่ได้
2. คลิก "เปิดกล้อง & เริ่มสแกน"
3. จ่อบัตรประชาชน
4. ตรวจสอบว่าข้อมูลถูกดึงมาถูกต้อง

---

## 🔧 การแก้ปัญหา

### ปัญหา: CORS Error
**แก้ไข:** ตรวจสอบว่า backend มี CORS headers ครบ (มีอยู่แล้วใน app.py)

### ปัญหา: Tesseract not found
**แก้ไข:** 
- Railway: ใช้ nixpacks.toml (มีอยู่แล้ว)
- Render: ใช้ render.yaml
- Heroku: ใช้ Aptfile + buildpack

### ปัญหา: API timeout
**แก้ไข:** 
- เพิ่ม timeout ใน frontend
- ใช้ภาพที่มีขนาดเล็กลง (resize ก่อนส่ง)

### ปัญหา: OCR ไม่แม่นยำ
**แก้ไข:**
- ตรวจสอบว่า Tesseract Thai language pack ติดตั้งแล้ว
- ปรับคุณภาพภาพให้ดีขึ้น
- เพิ่มแสงสว่าง

---

## 💰 ค่าใช้จ่าย

| Platform | Free Tier | ข้อจำกัด |
|----------|-----------|----------|
| **Railway** | $5 credit/month | 500 hours/month |
| **Render** | Free | 750 hours/month, sleep after 15 min |
| **Heroku** | Free (ถูกยกเลิก) | - |
| **Vercel** | Free | Static sites unlimited |

**แนะนำ:** Railway (ทั้งหมดใน 1 ที่)

---

## 📝 Checklist ก่อน Deploy

- [ ] ทดสอบ local ให้ทำงานได้ก่อน
- [ ] ตรวจสอบ requirements.txt ครบถ้วน
- [ ] เพิ่ม CORS headers ใน backend
- [ ] ตั้งค่า environment variables
- [ ] อัปเดต API URL ใน frontend
- [ ] ทดสอบ health check endpoint
- [ ] ทดสอบการสแกนบัตรจริง
- [ ] เพิ่ม error handling
- [ ] เพิ่ม rate limiting (ถ้าจำเป็น)
- [ ] ตรวจสอบ PDPA compliance

---

## 🔐 Security Checklist

- [ ] ใช้ HTTPS เท่านั้น
- [ ] เพิ่ม rate limiting
- [ ] ไม่เก็บภาพบัตรบน server
- [ ] เพิ่ม authentication (ถ้าใช้งานจริง)
- [ ] Log access สำหรับ audit
- [ ] Encrypt data in transit
- [ ] ปฏิบัติตาม PDPA

---

## 📚 Resources

- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [ThaiPersonalCardExtract](https://github.com/ggafiled/ThaiPersonalCardExtract)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
