# โครงสร้างโปรเจค Thai ID Card Scanner

```
thai-id-card-scanner/
│
├── 📄 index.html              # Frontend หลัก (UI สำหรับสแกนบัตร)
├── 🐍 app.py                  # Backend API (Flask + ThaiPersonalCardExtract)
├── 📋 requirements.txt        # Python dependencies
│
├── 📚 เอกสาร
│   ├── README.md              # คู่มือหลัก
│   ├── QUICKSTART.md          # คู่มือเริ่มต้นใช้งานด่วน
│   ├── DEPLOYMENT.md          # คู่มือ deploy แบบละเอียด
│   └── PROJECT_STRUCTURE.md   # ไฟล์นี้
│
├── 🧪 ทดสอบ
│   └── test_api.py            # Script ทดสอบ API
│
├── 🚀 Deployment Files
│   ├── railway.toml           # Config สำหรับ Railway (แนะนำ)
│   ├── nixpacks.toml          # Nixpacks config (Railway)
│   ├── render.yaml            # Config สำหรับ Render
│   ├── Procfile               # Config สำหรับ Heroku
│   └── Aptfile                # System packages สำหรับ Heroku
│
└── ⚙️ Config
    └── .gitignore             # Git ignore rules
```

## 📁 คำอธิบายไฟล์สำคัญ

### Frontend
- **index.html** - หน้าเว็บหลักที่มี:
  - UI สำหรับเปิดกล้อง
  - ระบบสแกนอัตโนมัติทุก 5 วินาที
  - ฟอร์มแสดงผลข้อมูลที่สแกนได้
  - รองรับทั้ง desktop และ mobile

### Backend
- **app.py** - Flask API server ที่มี:
  - `/` - Serve index.html
  - `/api/health` - Health check
  - `/api/scan-card` - OCR endpoint (รับภาพ → ส่งคืนข้อมูล)
  - ใช้ ThaiPersonalCardExtract สำหรับ OCR

### Dependencies
- **requirements.txt** - Python packages:
  - flask - Web framework
  - flask-cors - CORS support
  - ThaiPersonalCardExtract - Thai ID card OCR
  - opencv-python - Image processing
  - Pillow - Image handling

### Testing
- **test_api.py** - Script ทดสอบ API:
  - ทดสอบ health check
  - ทดสอบการสแกนบัตรจากไฟล์ภาพ
  - แสดงผลลัพธ์แบบละเอียด

## 🎯 แนวทางการ Deploy

### ✅ แนะนำ: Railway (Backend + Frontend)
```
โครงสร้าง: ทุกอย่างใน 1 ที่
ไฟล์ที่ใช้: railway.toml, nixpacks.toml
ข้อดี: ติดตั้งง่าย, รองรับ Tesseract, Free tier ดี
```



### ✅ ทางเลือกอื่น: Render
```
โครงสร้าร: Backend + Frontend
ไฟล์ที่ใช้: render.yaml
ข้อดี: Free tier, รองรับ Tesseract
```

## 🔄 Workflow การพัฒนา

### Local Development
```bash
1. ติดตั้ง Tesseract OCR
2. pip install -r requirements.txt
3. python app.py
4. เปิด http://localhost:5000
```

### Deploy to Railway
```bash
1. Push code ไปยัง GitHub
2. เชื่อมต่อ Railway กับ GitHub repo
3. Railway deploy อัตโนมัติ
4. รับ URL และทดสอบ
```



## 📊 ขนาดไฟล์โดยประมาณ

```
index.html          ~16 KB
app.py              ~3 KB
requirements.txt    ~200 bytes
test_api.py         ~2 KB
README.md           ~10 KB
DEPLOYMENT.md       ~15 KB
QUICKSTART.md       ~6 KB

รวมโค้ดหลัก:       ~21 KB
รวมเอกสาร:         ~31 KB
รวมทั้งหมด:        ~52 KB (ไม่รวม dependencies)
```

## 🔐 Security Notes

ไฟล์ที่ควร ignore:
- `.env` - Environment variables
- `venv/` - Python virtual environment
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files

ไฟล์ที่ต้องระวัง:
- `index.html` - อย่าฝัง API keys
- `app.py` - อย่าเก็บ sensitive data
- ภาพบัตรประชาชน - อย่าเก็บบน server

## 📝 License

MIT License - ใช้งานได้อย่างอิสระ แต่ต้องระวังเรื่อง PDPA

## 🙏 Credits

- ThaiPersonalCardExtract by ggafiled
- Tesseract OCR by Google
- Flask by Pallets
