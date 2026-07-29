from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import os
import uuid
import base64
import traceback

app = Flask(__name__)
CORS(app)

TEMP_DIR = 'temp_faces'
os.makedirs(TEMP_DIR, exist_ok=True)

def save_base64_img(b64_str):
    if ',' in b64_str:
        b64_str = b64_str.split(',')[1]
    img_data = base64.b64decode(b64_str)
    filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.jpg")
    with open(filename, 'wb') as f:
        f.write(img_data)
    return filename

@app.route('/verify-face', methods=['POST'])
def verify_face():
    data = request.json
    if not data or 'img1_base64' not in data or 'img2_base64' not in data:
        return jsonify({'error': 'img1_base64 and img2_base64 are required'}), 400
    
    img1_path = None
    img2_path = None
    
    try:
        img1_path = save_base64_img(data['img1_base64'])
        img2_path = save_base64_img(data['img2_base64'])
        
        # Using ArcFace model, metric=Euclidean l2 (most common for arcface)
        # We also enforce_detection=True so it throws error if no face is found
        result = DeepFace.verify(
            img1_path=img1_path,
            img2_path=img2_path,
            model_name="ArcFace",
            detector_backend="opencv",
            enforce_detection=True
        )
        
        return jsonify({
            'verified': bool(result['verified']),
            'distance': float(result['distance']),
            'threshold': float(result['threshold'])
        })
    except ValueError as e:
        # Usually triggered when no face is found in one of the images
        return jsonify({'error': 'Face not detected in image. Please provide a clear picture.', 'details': str(e)}), 400
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': 'Server error classifying face', 'details': str(e)}), 500
    finally:
        # Cleanup temporary files immediately to save disk read/write
        if img1_path and os.path.exists(img1_path):
            os.remove(img1_path)
        if img2_path and os.path.exists(img2_path):
            os.remove(img2_path)

if __name__ == '__main__':
    # Initial load of ArcFace weights on startup to prevent slow first-request
    print("Loading ArcFace model weights into memory...")
    try:
        DeepFace.build_model("ArcFace")
        print("Model loaded successfully.")
    except Exception as e:
        print("Model pre-load failed:", e)

    app.run(port=5001, debug=False)
