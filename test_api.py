"""
สคริปต์ทดสอบ API สำหรับสแกนบัตรประชาชน
ใช้สำหรับทดสอบว่า backend ทำงานได้ถูกต้อง
"""

import requests
import base64
import json
import sys

def test_health():
    """ทดสอบ health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/health')
        print("✅ Health Check:", response.json())
        return True
    except Exception as e:
        print("❌ Health Check Failed:", str(e))
        return False

def test_scan_card(image_path):
    """ทดสอบการสแกนบัตรจากไฟล์ภาพ"""
    try:
        # อ่านไฟล์ภาพและแปลงเป็น base64
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # สร้าง data URL
        image_url = f"data:image/jpeg;base64,{image_data}"
        
        # ส่ง request ไปยัง API
        response = requests.post(
            'http://localhost:5000/api/scan-card',
            json={'image': image_url},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Scan Card Success!")
            print("\n📋 ข้อมูลที่สแกนได้:")
            print(json.dumps(result['data'], indent=2, ensure_ascii=False))
            print("\n🔍 Raw OCR Result:")
            print(json.dumps(result['raw'], indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Scan Card Failed: {response.status_code}")
            print(response.text)
            return False
            
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์: {image_path}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    print("🧪 Testing Thai ID Card Scanner API\n")
    print("=" * 50)
    
    # ทดสอบ health check
    print("\n1. Testing Health Check...")
    if not test_health():
        print("\n⚠️ Backend server ไม่ทำงาน กรุณาเริ่ม server ด้วย: python app.py")
        sys.exit(1)
    
    # ทดสอบการสแกนบัตร (ถ้ามีไฟล์ภาพ)
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"\n2. Testing Card Scan with image: {image_path}")
        test_scan_card(image_path)
    else:
        print("\n💡 Tip: ทดสอบการสแกนบัตรด้วยคำสั่ง:")
        print("   python test_api.py path/to/id_card_image.jpg")
    
    print("\n" + "=" * 50)
    print("✅ Testing Complete!")
