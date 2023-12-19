'''
Byte&Crunch Commission Rates
	Less than 200 - 250
	Between 200 and 800 - 300
	Between 800 and 1500 - 400
	Between 1500 and 3000 - 500
	Above 3000 - 700   


'''
import os
from dotenv.main import load_dotenv
import requests
import uuid
from database.models import FlutterPayment, Student
from database.query import get_student

load_dotenv()

def compute_rates(price):
    rate = 0
    if price < 200:
        rate = 250
    elif price in range(200-1,800):
        rate = 300
    elif price in range(800-1,1500):
        rate = 400
    elif price in range(1500-1,3000):
        rate = 500
    elif price >= 3000:
        rate = 700

    return rate

def cart_to_lol(cart):
    temp_cart = list(cart.items())
    new_cart = []
    for item in temp_cart:
        new_cart.append(list(item))

    return new_cart


def flutterlink(subtotal, user_id, my_order, reference):
    payment = FlutterPayment(amount=subtotal, reference=reference, order_item=my_order)
    payment.save()
    student = get_student(user_id)
    print(student)
    user_email = student[4]
    print(user_email)
    print("start")
    flutterwave_url = 'https://api.flutterwave.com/v3/payments'
        
    secret_key = os.environ["FLUTTERWAVE_SECRET_KEY"]
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json',
    }
    # amount = amount * 100
    data = {
        'tx_ref': reference,
        'amount': subtotal,
        'redirect_url': 'https://webhook.site/358549f4-e83f-4aaa-8e62-394b7d7fe898',
        'customer': {
            'email': user_email,
        },
        'customizations': {
            'title': "BytenCrunch"
        }
    }
    

    response = requests.post(flutterwave_url, headers=headers, json=data)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    flutterwave_response = response.json()

    if flutterwave_response.get('status', False):
        payment_url = flutterwave_response['data']['link']
        print(payment_url)
        print("Got payment url")
        return payment_url
    else:
        print("Failed to get payment url")
        return {"status": "failed", "error": "Payment initialization failed"}

def status_check(status):
    if (status == "successful"  or status == "SUCCESSFUL"):
        return True
    else:
        return False
