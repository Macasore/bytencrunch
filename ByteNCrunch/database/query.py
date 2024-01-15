import mysql.connector as connector
from dotenv.main import load_dotenv
from datetime import datetime
# from .models import User, Student
import os
import config

load_dotenv()



def is_user(userid = None) -> bool:
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE,
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )

    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM student WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()
    mycon.close()
    if result == []:
        return False
    else:
        return True



def get_all_vendors():
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE,
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM vendor"
    )
    result = crsr.fetchall()
    mycon.close()
    return result

def get_product(product_id):
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE,
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    # "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120), image LONGBLOB, description VARCHAR(800), vendorID BIGINT, available BOOL, price INT, FOREIGN KEY (vendorID) REFERENCES vendor(userid)"
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE id=%s",
        (product_id,)
    )

    result = crsr.fetchall()[0]
    mycon.close()

    return result

def get_all_products() -> list:
    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE,
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product"
    )

    result = crsr.fetchall()

    mycon.close()

    return result
   

def get_products_from(myid):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE vendorID=%s",(myid,)
    )

    result = crsr.fetchall()
    mycon.close()
    return result


def get_student(userid):

    mycon = connector.connect(
    host= config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DATABASE,
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )

    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM student WHERE userid=%s",
        (userid,)
        )            
    result = crsr.fetchall()[0]  
    mycon.close()
    return result

def get_status(reference):
    mycon = connector.connect(
        host= config.DB_HOST,
        user= config.DB_USER,
        password= config.DB_PASSWORD,
        database= config.DATABASE,
        port=os.environ["DB_PORT"],
    sssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM flutter_payment WHERE reference=%s",
        (reference,)
    )
    result = crsr.fetchall()[0][5]
    mycon.close()
    return result

def update_status(reference, status_value):
    mycon = connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DATABASE,
        port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "UPDATE flutter_payment SET status=%s WHERE reference=%s",
        (status_value, reference)
    )
    mycon.commit()
    mycon.close()

def get_last_order(dets):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM orders WHERE customer_id=%s AND customer_name= %s AND ammount_paid=%s",(dets[0],dets[1], dets[2])
    )

    result = crsr.fetchall()[-1][0]
    mycon.close()
    return result

def get_user_name(userid):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM student WHERE userid=%s",
        (userid,)
    )

    result = crsr.fetchall()[0][2]
    mycon.close()
    return result

def get_user_room(userid):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM student WHERE userid=%s",
        (userid,)
    )

    result = crsr.fetchall()[0][5]
    mycon.close()
    return result

def get_order(reference):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM flutter_payment WHERE reference=%s",
        (reference,)
    )

    result = crsr.fetchall()[0][2]
    mycon.close()
    return result

def get_all_orders():
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM orders"
    )

    result = crsr.fetchall()
    mycon.close()
    return result

def get_all_flutter_orders():
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM flutter_payment"
    )

    result = crsr.fetchall()
    mycon.close()
    return result

def get_all_order_items():
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM order_item"
    )

    result = crsr.fetchall()
    mycon.close()
    return result

def get_todays_orders():
    today = datetime.date(datetime.today()).isoformat()
    all_orders = get_all_orders()
    today_orders = []
    for my_order in all_orders:
        if datetime.date(my_order[-1]).isoformat() == today:
            today_orders.append(my_order)

    return today_orders

def fetch_todays_orders():
    all_orders = get_todays_orders()
    all_orders = [[k for k in i] for i in all_orders]
    print(all_orders)
    all_order_items = get_all_order_items()
    all_order_items = [[k for k in i]  for i in all_order_items]
    for i in all_orders:
        my_id = i[0]
        cusctomer = get_student(i[1])
        room = cusctomer[4]
        name = cusctomer[2]
        the_order = i
        my_items = []
        for j in all_order_items:
            if j[2] == my_id:
                my_items.append((j[1], j[3]))
                print(j)

        my_order = f"Order for {name}:  "
        print(my_items)
        for k in my_items:
            product = get_product(i[0])
            my_order += f" {k[1]} order(s) of {product[1]} at # {int(product[3]) * k[1]} To be delivered to {room} "
            my_order += f"  Total(plus shipping) = {i[3]}"
        all_orders[all_orders.index(i)].append(my_order)

    return all_orders

def fetch_todays_fluter_orders():
    today = datetime.date(datetime.today()).isoformat()
    all_orders = get_all_flutter_orders()
    today_orders = []
    for my_order in all_orders:
        if datetime.date(my_order[-1]).isoformat() == today:
            today_orders.append(my_order)

    return today_orders
