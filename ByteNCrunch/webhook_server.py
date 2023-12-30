from flask import Flask, render_template, request, make_response, jsonify
import os, telegram
import json
from database.query import update_status, get_order
import requests
from dotenv.main import load_dotenv
from threading import Thread
load_dotenv()

app = Flask(__name__)

@app.route('/flutterwave_webhook', methods=['POST'])
def flutterwave_webhook():
    data = request.get_json()
    secret_hash = os.getenv("FLW_SECRET_HASH")
    signature = request.headers.get("verif-hash")

    if signature is None or (signature != secret_hash):
        return make_response("Unauthorized", 401)

    payload = request.get_data(as_text=True)
    response = make_response("OK", 200)

    data = json.loads(payload)
    status = data["status"]
    reference = data["txRef"]
    
    if status == 'successful' or status == 'SUCCESSFUL':

        try:
            new_status = update_status(reference, status)
            print("testing")
            telegram_token = os.getenv("TOKEN")
            group_id = os.getenv("order_group_id")
            order = get_order(reference)
            order += f"\n #flutterwavePayment"
            bot = telegram.Bot(token=os.getenv("TOKEN"))
            bot.send_message(chat_id=os.getenv("order_group_id"), text=order)
            return (response)
            
        except:
           print("error")
        
    else:
        new_status = update_status(reference, status)
        return response
    
@app.route('/redirect', methods=['GET'])
def redirect():
    return render_template('redirect.html')

def run_flask_server():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))


if __name__ == '__main__':
    flask_thread = Thread(target=run_flask_server)
    flask_thread.start()
    port = os.getenv('PORT')
    print(port)
    app.run(host='0.0.0.0',port=port)
