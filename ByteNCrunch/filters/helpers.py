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
from database.query import get_student, get_product

load_dotenv()

def compute_rates(price):
    # rate = 0
    # if price <= 1000:
    #     rate = 250
    # elif price in range(1050-1, 2500):
    #     rate = 350
    # elif price in range(2550-1, 4000):
    #     rate = 450
    # elif price in range(4050-1, 5500):
    #     rate = 550
    # elif price > 5550:
    #     rate = 600

    # return rate
    return 90

def cart_to_lol(cart):
    temp_cart = list(cart.items())
    new_cart = []
    for item in temp_cart:
        new_cart.append(list(item))

    return new_cart

def recompute_total(cart):
    total = 0
    for key,value in cart.items():
        prod = get_product(key)
        total += (value * prod[3])
    return total

def redo_table(schema):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )
    command = "CREATE TABLE IF NOT EXISTS {} ({})".format(schema[0], schema[1])

    # userid = user.userid
    # role = user.role
    crsr = mycon.cursor()
    
    crsr.execute(
        command
    )
    mycon.commit()

    mycon.close()
    print(f"created {schema[0]}")

def delete_table(name):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )
    command = " DROP TABLE IF EXISTS `{}`".format(name)

    crsr = mycon.cursor()
    crsr.execute(
        command
    )
    mycon.commit()

    mycon.close()
    print(f"deleted {name}")


def flutterlink(subtotal, user_id, my_order, reference):
    payment = FlutterPayment(amount=subtotal, reference=reference, order_item=my_order, user_id=user_id)
    payment.save()
    student = get_student(user_id)
    user_email = student[4]
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
        'redirect_url': 'https://bytencrunch-ed2943193a2c.herokuapp.com/redirect',
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
        return payment_url
    else:
        print("Failed to get payment url")
        return {"status": "failed", "error": "Payment initialization failed"}

def status_check(status):
    if status.lower() == "successful":
        return True
    else:
        return False
