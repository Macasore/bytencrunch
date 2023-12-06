import mysql.connector as connector
from dotenv.main import load_dotenv
from .models import User, Student
import os
from .query import get_last_order

load_dotenv()



def commit_user(user:User):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

    userid = user.userid
    role = user.role
    crsr = mycon.cursor()
    print(userid)
    crsr.execute(
        "INSERT INTO user (userid, role) VALUES (%s, %s)",
        (userid, role)
    )
    mycon.commit()

    mycon.close()
    
def commmit_student(student:Student):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

    role = student.role
    userid = student.userid
    name = student.name
    matno = student.matno
    email = student.email
    room = student.room
    mycursor = mycon.cursor()
    mycursor.execute(
        "INSERT INTO student (role, userid, name, email, matno ,  room) VALUES (%s, %s, %s,%s, %s, %s)",
        (role, userid,name,email, matno,room)
         )
    mycon.commit()
    mycon.close()


def commit_order(cust_id, cust_name, ammount):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )
    mycursor = mycon.cursor()
    mycursor.execute(
        "INSERT INTO orders (customer_id, customer_name, ammount_paid) VALUES (%s, %s, %s)",
        (cust_id, cust_name ,ammount)
         )
    mycon.commit()
    mycon.close()

def commit_order_item(product_id, quantity, order_id,):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )
    mycursor = mycon.cursor()
    mycursor.execute(
        "INSERT INTO order_item (product_id , order_id, item_count) VALUES (%s, %s, %s)",
        (product_id, order_id,quantity)
         )
    mycon.commit()
    mycon.close()

def push_order(cart_dict, cust_id, cust_name, total):
    #id, quant
    cart = list(cart_dict.items())
    commit_order(cust_id=cust_id, cust_name=cust_name, ammount=total)
    order_id = get_last_order((cust_id,cust_name,total))
    for i in cart:

        commit_order_item(i[0], i[1], order_id)

def update_room(user_id, room):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )

    crsr = mycon.cursor()
    crsr.execute(
        "UPDATE student SET room = %s WHERE userid =%s",
        (room, user_id)
    )
    mycon.commit()

    mycon.close()
