from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pytesseract
import base64
import io
from PIL import Image
import numpy as np
import cv2
import os
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

def extract_thai_id_info(text):
    """Extract information from Thai ID card OCR text"""
    result = {
        'Identification_Number': '',
        'Name': '',
        'Lastname': '',
        'Date_of_Birth': '',
        'Address': '',
        'Religion': '',
        'Date_of_Issue': '',
        'Date_of_Expiry': '',
    }
    
    # Extract ID number (13 digits)
    id_match = re.search(r'\b(\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d[\s\-]*\d)\b', text)
    if id_match:
        result['Identification_Number'] = re.sub(r'[\s\-]', '', id_match.group(1))
    
    # Extract dates (various formats)
    date_patterns = [
        r'(\d{1,2}[\s\-\.\/]\w{3,}[\s\-\.\/]\d{2,4})',
        r'(\d{1,2}[\s\-\.\/]\d{1,2}[\s\-\.\/]\d{2,4})'
    ]
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text))
    
    if len(dates) >= 1:
        result['Date_of_Birth'] = dates[0]
    if len(dates) >= 2:
        result['Date_of_Issue'] = dates[1]
    if len(dates) >= 3:
        result['Date_of_Expiry'] = dates[2]
    
    # Extract name (look for Thai or English name patterns)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        # Look for name indicators
        if any(keyword in line.lower() for keyword in ['name', 'ชื่อ', 'นาย', 'นาง', 'นางสาว', 'mr', 'mrs', 'miss']):
            # Try to extract name from this line or next
            name_line = line
            if i + 1 < len(lines):
                name_line += ' ' + lines[i + 1]
            
            # Remove common prefixes
            name_line = re.sub(r'(Name|ชื่อ|นามสกุล|Surname|Last\s*Name|นาย|นาง|นางสาว|Mr\.?|Mrs\.?|Miss)', '', name_line, flags=re.IGNORECASE)
            name_parts = name_line.strip().split()
            
            if len(name_parts) >= 2:
                result['Name'] = name_parts[0]
                result['Lastname'] = ' '.join(name_parts[1:])
            elif len(name_parts) == 1:
                result['Name'] = name_parts[0]
            break
    
    # Extract religion
    religion_match = re.search(r'(พุทธ|คริสต์|อิสลาม|ฮินดู|ซิกข์|Buddhist|Christian|Islam|Hindu|Sikh)', text, re.IGNORECASE)
    if religion_match:
        result['Religion'] = religion_match.group(1)
    
    # Extract address (usually the longest text block)
    address_keywords = ['address', 'ที่อยู่', 'บ้านเลขที่']
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in address_keywords):
            # Collect following lines as address
            address_lines = lines[i:min(i+5, len(lines))]
            result['Address'] = ' '.join([l.strip() for l in address_lines if l.strip()])
            break
    
    return result

@app.route('/api/scan-card', methods=['POST'])
def scan_card():
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Preprocess image for better OCR
        img_array = np.array(image)
        
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # OCR with Thai and English
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(thresh, lang='tha+eng', config=custom_config)
        
        # Extract information
        result = extract_thai_id_info(text)
        
        # Format response
        response = {
            'success': True,
            'data': {
                'citizenId': result.get('Identification_Number', ''),
                'firstName': result.get('Name', ''),
                'lastName': result.get('Lastname', ''),
                'dob': result.get('Date_of_Birth', ''),
                'address': result.get('Address', ''),
                'religion': result.get('Religion', ''),
                'issueDate': result.get('Date_of_Issue', ''),
                'expireDate': result.get('Date_of_Expiry', ''),
            },
            'raw': result,
            'ocr_text': text
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
