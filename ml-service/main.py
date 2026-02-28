from flask import Flask, request, jsonify
from flask_cors import CORS
import predict

app = Flask(__name__)
CORS(app) # Enable CORS for all routes (important for React integration)

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Handle crop disease analysis requests.
    Expects a Multipart/FormData request with an 'image' file.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    
    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        img_bytes = image_file.read()
        result = predict.predict_disease(img_bytes)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to analyze image"}), 500
            
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "serving"})

if __name__ == '__main__':
    # Running on port 5001 as configured in the frontend
    app.run(host='0.0.0.0', port=5001, debug=True)
