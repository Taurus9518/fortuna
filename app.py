from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

TELEGRAM_BOT_TOKEN = '7494838365:AAGgZH33vCnpEOtc8t3WR_kVyxsXWV0dS5o'

logging.basicConfig(level=logging.DEBUG)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        if not data or 'message' not in data or 'chat_id' not in data:
            logging.error("No message or chat_id provided")
            return jsonify({'error': 'No message or chat_id provided'}), 400

        message = data['message']
        chat_id = data['chat_id']
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {'chat_id': chat_id, 'text': message}
        
        logging.debug(f"Sending payload: {payload}")
        response = requests.post(url, json=payload)
        
        logging.debug(f"Response status: {response.status_code}")
        logging.debug(f"Response content: {response.content}")

        if response.status_code == 200:
            return jsonify({'status': 'success'}), 200
        else:
            logging.error(f"Failed to send message: {response.json()}")
            return jsonify({'status': 'failure', 'response': response.json()}), 500
    except Exception as e:
        logging.exception("An error occurred")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
