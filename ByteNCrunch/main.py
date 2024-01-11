from flask import Flask, render_template, request, make_response, jsonify
from database.query import update_status
import requests
from dotenv.main import load_dotenv
from threading import Thread
from telegram.ext import Updater
from handlers import all_handlers, admin_handlers
from filters.helpers import redo_table, delete_table
from database.query import fetch_todays_fluter_orders, fetch_todays_orders
import os
import json
import logging
load_dotenv()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    order_schema = (
        "orders" ,
        "id INT AUTO_INCREMENT PRIMARY KEY , customer_id BIGINT, customer_name VARCHAR(120), ammount_paid INT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  FOREIGN KEY (customer_id) REFERENCES student(userid) "
                    )
    order_item_schema = (
        "order_item",
        "id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, order_id INT, item_count INT, FOREIGN KEY (product_id) REFERENCES product(id), FOREIGN KEY (order_id) REFERENCES orders(id)"
                    )
    # delete_table(order_item_schema[0])
    # delete_table(order_schema[0])
    redo_table(order_schema)
    redo_table(order_item_schema)
    updater = Updater(os.getenv("TOKEN"))
    updater_two  = Updater("6911099761:AAFzK5qM-JowUTHD1-SG_P9QJPfKjflS5_4")
    dispatcher_two = updater_two.dispatcher
    for handler in admin_handlers:
        dispatcher_two.add_handler(handler)

    dispatcher = updater.dispatcher
    updaters = [updater, updater_two]
    for handler in all_handlers:
        dispatcher.add_handler(handler)

    for my_updater in updaters:
        my_updater.start_polling()
