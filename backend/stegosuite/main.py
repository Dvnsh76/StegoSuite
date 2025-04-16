from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
from PIL import Image
import cv2
import io
import json
import os
import tempfile
import shutil
from metrics import calculate_metrics_in_memory
import logging
import traceback

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

app = Flask(__name__,static_folder='frontend\dist',static_url_path='')
CORS(app, expose_headers=['X-Metrics'])

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/encode', methods=['POST'])
def handle_encode():
    img = None
    return_data = None
    metrics = None
    
    try:
        scheme = request.form.get('scheme')
        message = request.form.get('message')
        image_file = request.files.get('image')
        
        if not all([scheme, message, image_file]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        input_buffer = io.BytesIO(image_file.read())
        output_buffer = io.BytesIO()
        
        if scheme == 'dct':
            img_pil = Image.open(input_buffer)
            img_pil = img_pil.convert('YCbCr')
            img_arr = np.array(img_pil)
            img_pil.close()
            
            h = (img_arr.shape[0] // 8) * 8
            w = (img_arr.shape[1] // 8) * 8
            
            if h == 0 or w == 0:
                raise ValueError("Image too small for DCT encoding")
                
            img_arr = img_arr[:h, :w]
            processed_buffer = io.BytesIO()
            Image.fromarray(img_arr, 'YCbCr').convert('RGB').save(processed_buffer, format='PNG')
            processed_buffer.seek(0)
            
            from encoders.dct import dct_encode_in_memory
            dct_encode_in_memory(processed_buffer, message, output_buffer)
        elif scheme == 'pvd':
            from encoders.pvd import pvd_encode_in_memory
            pvd_encode_in_memory(input_buffer, message, output_buffer)
        elif scheme == 'erde':
            from encoders.erde import erde_encode_in_memory
            erde_encode_in_memory(input_buffer, message, output_buffer)
        elif scheme == 'lsbm':
            from encoders.lsbm import lsbm_encode_in_memory
            lsbm_encode_in_memory(input_buffer, message, output_buffer)
        else:
            return jsonify({'error': 'Invalid encoding scheme'}), 400
        
        input_buffer.seek(0)
        output_buffer.seek(0)
        
        try:
            metrics = calculate_metrics_in_memory(input_buffer, output_buffer)
        except Exception as metrics_err:
            logging.warning(f"Metrics calculation failed: {metrics_err}")
            metrics = None
        
        output_buffer.seek(0)
        
        headers = {}
        if metrics:
            try:
                headers['X-Metrics'] = json.dumps(metrics)
            except Exception as json_err:
                logging.warning(f"Failed to serialize metrics: {json_err}")
        
        return send_file(
            output_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name='stego.png'
        ), 200, headers
        
    except ValueError as ve:
        return jsonify({'error': f'Input Error: {ve}'}), 400
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error(f"Encoding error: {e}\n{error_details}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/decode', methods=['POST'])
def handle_decode():
    try:
        scheme = request.form.get('scheme')
        image_file = request.files.get('image')
        
        if not all([scheme, image_file]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        input_buffer = io.BytesIO(image_file.read())
        
        if scheme == 'auto':
            from decoders.auto_d import auto_decode_using_metadata_in_memory
            result = auto_decode_using_metadata_in_memory(input_buffer)
        elif scheme == 'dct':
            from decoders.dct import dct_decode_in_memory
            result = dct_decode_in_memory(input_buffer)
        elif scheme == 'pvd':
            from decoders.pvd import pvd_decode_in_memory
            result = pvd_decode_in_memory(input_buffer)
        elif scheme == 'erde':
            from decoders.erde import erde_decode_in_memory
            result = erde_decode_in_memory(input_buffer)
        elif scheme == 'lsbm':
            from decoders.lsbm import lsbm_decode_in_memory
            result = lsbm_decode_in_memory(input_buffer)
        else:
            return jsonify({'error': 'Invalid decoding scheme'}), 400
        
        if isinstance(result, str) and result.startswith("AutoDecode Error:"):
            result_message = result
        elif result is None or result == "":
            result_message = ""
        else:
            result_message = str(result)
        
        return jsonify({
            'message': result_message,
            'scheme': scheme
        })
        
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error(f"Decoding error: {e}\n{error_details}")
        return jsonify({'error': str(e)}), 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")


if __name__ == '__main__':
    logging.info("Starting StegoSuite Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
