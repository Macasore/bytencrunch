import mysql.connector as connector
from dotenv.main import load_dotenv
import os, csv

load_dotenv()

def create_database():
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=os.environ["DB_PORT"],
        ssl_disabled=True
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(os.environ["DATABASE"]))
    mydb.commit()
     

def create_table( name, fields):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"],
        port=os.environ["DB_PORT"],
        ssl_disabled=True
    )

    operation = "CREATE TABLE IF NOT EXISTS {} ({})".format(name, fields)
    crsr = mydb.cursor()
    crsr.execute(operation)
    mydb.commit()

tables = {
    "student" : "role CHAR(120), userid BIGINT PRIMARY KEY, name VARCHAR(120), matno CHAR(15) UNIQUE,email VARCHAR(70), room VARCHAR(255), account_number CHAR(10), bank CHAR(180)",
    "vendor" : "userid BIGINT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120), UNIQUE (name)",
    "product" : "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120), vendorID BIGINT, price INT,options TEXT, FOREIGN KEY (vendorID) REFERENCES vendor(userid)",
    "orders" : "id INT AUTO_INCREMENT PRIMARY KEY , customer_id BIGINT, customer_name VARCHAR(120), ammount_paid INT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  FOREIGN KEY (customer_id) REFERENCES student(userid)",
    "order_item" : "id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, order_id INT, item_count INT, FOREIGN KEY (product_id) REFERENCES product(id), FOREIGN KEY (order_id) REFERENCES orders(id)",
    # "user" : " userid BIGINT PRIMARY KEY, role CHAR(120) "

}

tables["flutter_payment"] = """
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    order_item VARCHAR(300),
    amount DECIMAL(15, 2),
    reference VARCHAR(100),
    status CHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
"""

def add_vendor(vendor):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    mycursor = mycon.cursor()
    mycursor.execute(
        "INSERT INTO vendor (name) VALUES (%s)",
        (vendor,)
         )
    mycon.commit()
    mycon.close()
def find_vendorid(vendor):
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
        "SELECT * FROM vendor WHERE name=%s",
        (vendor,)
        )                  
    result = crsr.fetchall()[0]  
    mycon.close()
    return result[0]


def add_product(item,price,vendor,options):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    port=os.environ["DB_PORT"],
    ssl_disabled=True
    )
    crsr = mycon.cursor()
    vendorID = find_vendorid(vendor)
    print(vendorID)
    crsr.execute(
        "INSERT INTO product (name, vendorID,options, price) VALUES (%s,%s,%s,%s)",
        ( item.strip(), vendorID,options, price)
    )
    mycon.commit()
    mycon.close()

def populate_vendor_and_product(f_name,):
    with open(f_name, "r") as f:
        vendors = []
        items = []
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)
            if row["Vendor"].title() not in vendors:
                vendors.append(row["Vendor"].title())
                add_vendor(row["Vendor"].title())
            add_product(row["Item"], row["Price"], row["Vendor"], row["Additional Options"])

    print(vendors)


create_database()
for key, val in tables.items():
    create_table(key, val)

populate_vendor_and_product("menu.csv")
