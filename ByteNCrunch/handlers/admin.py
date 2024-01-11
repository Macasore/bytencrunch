from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler, CommandHandler
import csv, os

from database.query import fetch_todays_fluter_orders, fetch_todays_orders


def fetch_from_direct_transfer(update, bot):
    my_orders = fetch_todays_orders()
    user_id = update.effective_user.id
    headers = ["id",  "customer_id", "customer_name", 'ammount_paid' , "Date order was Made", "Order Details"]
    my_orders.insert(0,headers)
    with open(f'{user_id}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(my_orders)

    bot.bot.send_document(update.effective_chat.id,  open(f'{user_id}.csv', 'rb'))
    os.remove(f'{user_id}.csv')

def fetch_from_flutter(update, bot):
    my_orders = fetch_todays_fluter_orders()
    user_id = update.effective_user.id
    headers = ["id","user_id","order_item","amount","reference","status","created_at"]
    my_orders.insert(0,headers)
    with open(f'{user_id}_flutter.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(my_orders)

    bot.bot.send_document(update.effective_chat.id,  open(f'{user_id}_flutter.csv', 'rb'))
    os.remove(f'{user_id}_flutter.csv')


fetch_from_direct_transfer_handler = CommandHandler(
    "direct_transfer",
    fetch_from_direct_transfer
)

fetch_from_flutter_handler = CommandHandler(
    "flutter",
    fetch_from_flutter
)
    
