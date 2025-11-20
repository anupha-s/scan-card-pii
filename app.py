from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ThaiPersonalCardExtract import PersonalCard
import base64
import io
from PIL import Image
import numpy as np
import cv2
import os

app = Flask(__name__)
CORS(app)

reader = PersonalCard(lang="mix", tesseract_cmd=r"tesseract")

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

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
        
        # Convert to OpenCV format
        img_array = np.array(image)
        if len(img_array.shape) == 2:
            img_cv = img_array
        else:
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Extract card information
        result = reader.extractInfo(img_cv)
        
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
            'raw': result
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
