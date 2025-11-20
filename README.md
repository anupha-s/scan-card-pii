# Thai ID Card Scanner with ThaiPersonalCardExtract

ระบบสแกนบัตรประชาชนไทยแบบเรียลไทม์ที่ใช้ ThaiPersonalCardExtract library เพื่อความแม่นยำสูง

## คุณสมบัติ

- ✅ สแกนบัตรประชาชนไทยจากกล้องแบบเรียลไทม์
- ✅ ใช้ ThaiPersonalCardExtract (Python) ที่ออกแบบมาเฉพาะบัตรประชาชนไทย
- ✅ ดึงข้อมูลอัตโนมัติ: เลขบัตร, ชื่อ, นามสกุล, วันเกิด, ศาสนา, ที่อยู่, วันออกบัตร, วันหมดอายุ
- ✅ UI ที่ใช้งานง่าย รองรับมือถือ
- ✅ สแกนอัตโนมัติทุก 5 วินาที

## ความต้องการของระบบ

### Backend (Python)
- Python 3.8+
- Tesseract OCR
- pip (Python package manager)

### Frontend
- เบราว์เซอร์ที่รองรับ WebRTC (Chrome, Firefox, Safari, Edge)
- HTTPS หรือ localhost (สำหรับการเข้าถึงกล้อง)

## การติดตั้ง

### 1. ติดตั้ง Tesseract OCR

#### Windows
```bash
# ดาวน์โหลดและติดตั้งจาก
https://github.com/UB-Mannheim/tesseract/wiki

# หรือใช้ Chocolatey
choco install tesseract
```

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

### 2. ติดตั้ง Python Dependencies

```bash
# สร้าง virtual environment (แนะนำ)
python -m venv venv

# เปิดใช้งาน virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

### 3. ตั้งค่า Tesseract Path (ถ้าจำเป็น)

ถ้า Tesseract ไม่อยู่ใน PATH ให้แก้ไขไฟล์ `app.py`:

```python
# Windows
reader = PersonalCard(lang="mix", tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe")

# macOS/Linux
reader = PersonalCard(lang="mix", tesseract_cmd="/usr/local/bin/tesseract")
```

## การใช้งาน

### 1. เริ่มต้น Backend Server

```bash
python app.py
```

Server จะรันที่ `http://localhost:5000`

### 2. เปิด Frontend

เปิดไฟล์ `index.html` ในเบราว์เซอร์:

```bash
# ใช้ Python HTTP Server
python -m http.server 8000

# จากนั้นเปิด
http://localhost:8000
```

หรือใช้ Live Server extension ใน VS Code

### 3. ใช้งานระบบ

1. คลิก "เปิดกล้อง & เริ่มสแกน"
2. อนุญาตการเข้าถึงกล้อง
3. จ่อบัตรประชาชนให้อยู่ในเฟรมและชัดเจน
4. ระบบจะสแกนอัตโนมัติทุก 5 วินาที
5. ข้อมูลจะถูกเติมลงในฟอร์มอัตโนมัติ
6. ตรวจสอบและแก้ไขข้อมูลก่อนบันทึก

## API Endpoints

### POST /api/scan-card

สแกนบัตรประชาชนจากภาพ

**Request Body:**
```json
{
  "image": "data:image/png;base64,..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "citizenId": "1234567890123",
    "firstName": "สมชาย",
    "lastName": "ใจดี",
    "dob": "01 Jan 1990",
    "address": "123 ถนนสุขุมวิท...",
    "religion": "พุทธ",
    "issueDate": "01 Jan 2020",
    "expireDate": "01 Jan 2030"
  },
  "raw": { ... }
}
```

### GET /api/health

ตรวจสอบสถานะ server

**Response:**
```json
{
  "status": "ok"
}
```

## การแก้ปัญหา

### ปัญหา: Tesseract not found
- ตรวจสอบว่าติดตั้ง Tesseract แล้ว
- ตั้งค่า `tesseract_cmd` ใน `app.py` ให้ถูกต้อง

### ปัญหา: CORS Error
- ตรวจสอบว่า backend รันอยู่
- ตรวจสอบ API URL ใน frontend

### ปัญหา: กล้องไม่เปิด
- ใช้ HTTPS หรือ localhost
- ตรวจสอบสิทธิ์การเข้าถึงกล้องในเบราว์เซอร์

### ปัญหา: OCR ไม่แม่นยำ
- ให้แสงสว่างเพียงพอ
- ถือบัตรให้ตรงและชัดเจน
- หลีกเลี่ยงเงาและแสงสะท้อน
- ใช้กล้องที่มีความละเอียดสูง

## ข้อควรระวัง

⚠️ **PDPA & Security:**
- ระบบนี้เป็นเดโม่เท่านั้น
- ไม่ควรใช้กับข้อมูลจริงโดยไม่มีมาตรการรักษาความปลอดภัย
- ควรเพิ่ม: encryption, authentication, access control, audit log
- ปฏิบัติตาม พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล (PDPA)

## เทคโนโลยีที่ใช้

- **Backend:** Python, Flask, ThaiPersonalCardExtract, OpenCV
- **Frontend:** HTML5, JavaScript, WebRTC
- **OCR:** Tesseract OCR

## การ Deploy บน Vercel

### ⚠️ ข้อจำกัดสำคัญ

**Vercel ไม่รองรับ Tesseract OCR และ OpenCV ในแบบ Serverless Functions โดยตรง** เนื่องจาก:
- Tesseract ต้องการ binary files ที่ใหญ่เกินไป
- OpenCV ต้องการ system libraries ที่ Vercel ไม่มี
- ThaiPersonalCardExtract ต้องการทั้งสองอย่าง

### แนวทางแก้ไข (3 ทางเลือก)

#### ทางเลือกที่ 1: Deploy Frontend บน Vercel + Backend แยก
1. Deploy เฉพาะ `index.html` บน Vercel (Static Site)
2. Deploy Backend (Python) บน:
   - **Railway** (แนะนำ - รองรับ Python + Tesseract)
   - **Render** (Free tier มี)
   - **Heroku** (มี buildpack สำหรับ Tesseract)
   - **DigitalOcean App Platform**
   - **Google Cloud Run**

```bash
# Deploy frontend บน Vercel
vercel --prod

# แก้ไข API URL ใน index.html ให้ชี้ไปที่ backend
# เช่น: https://your-backend.railway.app/api/scan-card
```

#### ทางเลือกที่ 2: Deploy ทั้งหมดบน Railway
Railway รองรับ Python และ Tesseract ได้เต็มรูปแบบ

```bash
# 1. สร้าง railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE"
  }
}

# 2. Deploy
railway up
```

#### ทางเลือกที่ 3: ใช้ External OCR API
แทนที่ ThaiPersonalCardExtract ด้วย:
- **Google Cloud Vision API** (มี Thai OCR)
- **Azure Computer Vision** (รองรับภาษาไทย)
- **AWS Textract**

### Quick Deploy บน Railway (แนะนำ)

1. สร้างบัญชี [Railway.app](https://railway.app)
2. เชื่อมต่อ GitHub repository
3. เพิ่ม Nixpacks buildpack สำหรับ Tesseract:

```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python app.py"
restartPolicyType = "ON_FAILURE"
healthcheckPath = "/api/health"
healthcheckTimeout = 100
```

4. เพิ่ม environment variables:
```
FLASK_ENV=production
PORT=5000
```

5. Deploy!

### Deploy Frontend บน Vercel (Static)

```bash
# 1. ติดตั้ง Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel --prod

# 4. อัปเดต API URL ใน index.html
# แก้จาก /api/scan-card เป็น https://your-backend.railway.app/api/scan-card
```

## License

MIT License

## เครดิต

- [ThaiPersonalCardExtract](https://github.com/ggafiled/ThaiPersonalCardExtract) by ggafiled
