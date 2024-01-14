from enum import Enum
from datetime import datetime
import mysql.connector as connector
from dotenv.main import load_dotenv
import os
import json

load_dotenv()



class User:
    
    def __init__(self,userid=None, role=None):
        self.userid=userid
        self.role=role
        

        
class Student:

    def __init__(self, role=None, userid=None, name=None, matno=None,email=None, room= None, account_number=None, bank=None):
        self.role = role
        self.userid = userid
        self.name =name
        self.matno=matno
        self.email = email
        self.room = room
        self.account_number= account_number
        self.bank = bank

    def __str__(self):
        return self.role


class Order:
	def __init__(self, id=None,customer_id=None,status=None):
		self.id = id
		self.customer_id= customer_id
		self.status = status
		
		
class OrderItem:
	def __init__(self, id=None,product_id=None,order=None,item_count=0):
		self.id=id
		self.product_id = product_id
		self.order=order
		self.item_count=item_count
		
		
class Status(Enum):
	Delivered = "delivered"
	Cancelled = "cancelled"
	Pending = "pending"
	Rejected_By_Vendor = "rejected_by_vendor"
            
class FlutterPayment:
    def __init__(self, id=None, amount=None, reference=None, status='pending', created_at=None, user_id=None, order_item=None):
            self.id = id
            self.amount = amount
            self.reference = reference
            self.status = status
            self.user_id = user_id
            self.order_item = order_item
            self.created_at = created_at if created_at is not None else datetime.now()
            
    def save(self):
        mycon = connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DATABASE"],
            port=os.environ["DB_PORT"],
            ssl_disabled=True
        )

        mycursor = mycon.cursor()

        order_item_json = json.dumps(self.order_item)

        sql = "INSERT INTO flutter_payment (amount, reference, status, created_at, user_id, order_item) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (self.amount, self.reference, self.status, self.created_at, self.user_id, order_item_json)

        mycursor.execute(sql, val)

        mycon.commit()
        self.id = mycursor.lastrowid  
        mycursor.close()
        mycon.close()

    def __str__(self):
        return f"FlutterPayment(id={self.id}, amount={self.amount}, reference={self.reference}, status={self.status}, created_at={self.created_at}, user_id={self.user_id}, order_item={self.order_item})"

    def to_dict(self):
        return {
            "id": self.id,
            "amount": str(self.amount),
            "reference": self.reference,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
            "order_item": self.order_item,
        }
            

