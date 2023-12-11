from flask import Flask, render_template, request, make_response, jsonify
import os
import json
from database.query import update_status
import requests

app = Flask(__name__)

@app.route('/flutterwave_webhook', methods=['POST'])
def flutterwave_webhook():
    data = request.get_json()
    secret_hash = os.getenv("FLW_SECRET_HASH")
    signature = request.headers.get("verifi-hash")

    if signature is None or (signature != secret_hash):
        return make_response("Unauthorized", 401)

    payload = request.get_data(as_text=True)
    response = make_response("OK", 200)

    data = json.loads(payload)
    email = data["customer"]["email"]
    status = data["status"]
    reference = data["txRef"]
    
    if status == 'successful' or status == 'SUCCESSFUL':

        try:
            new_status = update_status(reference, status)
            print("testing")
            telegram_token = os.getenv("TOKEN")
            group_id = os.getenv("order_group_id")
            message = f"Payment successful for reference: {reference} with email: {email}"
            requests.get(f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={group_id}&text={message}")
            return (response)
            
        except:
           print("error")
        
    else:
        new_status = update_status(reference, status)
        return response
    
@app.route('/redirect', methods=['GET'])
def redirect():
    return render_template('redirect.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
