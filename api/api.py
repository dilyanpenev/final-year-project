import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/colourise', methods=['POST'])
def get_current_time():
    input_image = request.files['image']
    data = input_image.stream.read()
    data = base64.b64encode(data).decode()
    return jsonify({'msg': 'success', 'img': data})
