from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import requests, base64, io

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    data = request.get_json() or {}
    message_id = data.get('messageId')
    attachment_id = data.get('attachmentId')
    user_email = data.get('userEmail', 'me')
    mime_type = data.get('mimeType', 'application/pdf')

    auth_header = request.headers.get('Authorization', '')
    access_token = auth_header.replace('Bearer ', '')

    if not all([message_id, attachment_id, access_token]):
        return jsonify({'error': 'Missing params', 'text': ''}), 200

    url = f'https://gmail.googleapis.com/gmail/v1/users/{user_email}/messages/{message_id}/attachments/{attachment_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        return jsonify({'error': f'Gmail {resp.status_code}', 'text': ''}), 200

    att = resp.json().get('data', '').replace('-', '+').replace('_', '/')
    att += '=' * (-len(att) % 4)
    file_bytes = base64.b64decode(att)

    try:
        # Si c'est une image (PNG, JPG, etc.) → traitement direct
        if mime_type.startswith('image/'):
            img = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(img, lang='fra+eng')
        else:
            # PDF → convert_from_bytes
            images = convert_from_bytes(file_bytes)
            text = ''.join(pytesseract.image_to_string(img, lang='fra+eng') for img in images)

        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e), 'text': ''}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)