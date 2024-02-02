from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_product
from filters.helpers import compute_rates
from dotenv.main import load_dotenv
from datetime import datetime
import os
from database.manipulate import push_order
from database.query import get_user_name, get_user_room

load_dotenv()




def checkout(update, bot):
    time_limit_upper = 6
    time_limit_lower = 17
    current_time = datetime.now().strftime("%Y-%m-%d, %H:%M").split(",")[1].split(":")[0].strip()
    ct_int = int(current_time)
    query = update.callback_query
    if ct_int >= time_limit_lower :
         text_to_send = f"Hi there! \n We're currently resting for the day, pleease come back between 8am and 5:30pm "
         reply_keyboard = [
         [
            InlineKeyboardButton(text="Back to home!", callback_data="start")
        ]
    ]
         markup = InlineKeyboardMarkup(reply_keyboard)
         query.edit_message_text(
            text=text_to_send,
            reply_markup=markup,
        )
    elif  ct_int <= time_limit_upper:
         text_to_send = f"Hi there! \n We're currently resting for the day, pleease come back between 8am and 5:30pm "
         reply_keyboard = [
         [
            InlineKeyboardButton(text="Back to home!", callback_data="start")
        ]
    ]
         markup = InlineKeyboardMarkup(reply_keyboard)
         query.edit_message_text(
            text=text_to_send,
            reply_markup=markup,
        )
    else:

        # data = update.callback_query.data
        total = int(bot.user_data["cart_total"])
        rate = compute_rates(total)
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Bank tranfer to Byte n Crunch", callback_data="pay_with_direct_transfer")
            ] ,
            [
                InlineKeyboardButton(text="Pay with Flutterwave", callback_data="pay_with_flutter_wave")
            ],
             [
                InlineKeyboardButton(text="Back to home!", callback_data="start")
            ]
        ]
        markup = InlineKeyboardMarkup(reply_keyboard)
        query.edit_message_text(
            text=f"You total comes down to # {total+rate} \n Subtotal: #{total} \n Shipping : #{rate} \n Please ensure that you have a good internet condition before proceeding",
            reply_markup=markup,
        )

def direct_transfer(update, bot):
    query = update.callback_query
    
    time_limit_upper = 6
    time_limit_lower = 17
    current_time = datetime.now().strftime("%Y-%m-%d, %H:%M").split(",")[1].split(":")[0].strip()
    ct_int = int(current_time)
    if ct_int >= time_limit_lower :
         text_to_send = f"Hi there! \n We're currently resting for the day, pleease come back between 8am and 5:30pm "
         reply_keyboard = [
         [
            InlineKeyboardButton(text="Back to home!", callback_data="start")
        ]
    ]
         markup = InlineKeyboardMarkup(reply_keyboard)
         query.edit_message_text(
            text=text_to_send,
            reply_markup=markup,
        )
    elif  ct_int <= time_limit_upper:
         text_to_send = f"Hi there! \n We're currently resting for the day, pleease come back between 8am and 5:30pm "
         reply_keyboard = [
         [
            InlineKeyboardButton(text="Back to home!", callback_data="start")
        ]
    ]
         markup = InlineKeyboardMarkup(reply_keyboard)
         query.edit_message_text(
            text=text_to_send,
            reply_markup=markup,
        )
    else:
        
         total = int(bot.user_data["cart_total"])
         rate = compute_rates(total)
         total += rate
         acc_name = os.environ["ACCOUNT_NAME"]
         acc_no =  os.environ["ACCOUNT_NUMBER"]
         bank =  os.environ["BANK"]
         text_to_send = f"Make a tranfer of #{total} to the account given below: \n Account Name = {acc_name} \n Account Number = {acc_no} \n Bank = {bank} \n {ct_int}"
         reply_keyboard = [
             [
                InlineKeyboardButton(text="I've made the Transfer!", callback_data="direct_payment_confirm")
            ],
             [
                InlineKeyboardButton(text="Back to home!", callback_data="start")
            ]
        ]
         markup = InlineKeyboardMarkup(reply_keyboard)
         query.edit_message_text(
            text=text_to_send,
            reply_markup=markup,
        )
    


def confirm_direct_transfer(update, bot):
    query = update.callback_query
    # user_name = os.environ["byte_user_name"]
    total = int(bot.user_data["cart_total"])
    rate = compute_rates(int(bot.user_data["cart_total"]))
    new_total = total+rate
    bot.user_data["cart_total"] = new_total
    name = get_user_name(update.effective_user.id)
    room = get_user_room(update.effective_user.id)
    order_group_id = os.getenv("order_group_id")
    print(name)
    text_to_send = f"Thanks you for choosing us! \n Please send a copy of your transfer receipt to @mikeyruled to begin processing your order; your order will not be processed until you do.\nand do well to join our official channel if you haven't: https://t.me/+TJOB63n3Jc81MWU0 "
    push_order(bot.user_data["cart"],update.effective_user.id,name,int(bot.user_data["cart_total"]))
    my_text = f"Order for {name}, "
    for i in list(bot.user_data["cart"].items()):
        product = get_product(i[0])
        my_text += f"\n >> {i[1]} order(s) of {product[1]} at # {int(product[3]) * i[1]} \n To be delivered to {room} \n ***Payment not Confirmed*** \n #DirectBankTransfer"

    my_text += f"\n Total(plus shipping) = {new_total}"
    reply_keyboard = [
         [
            InlineKeyboardButton(text="Back to home!", callback_data="start")
        ]
    ]
    bot.bot.send_message(chat_id= order_group_id, text=my_text)
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=text_to_send,
        reply_markup=markup,
    )
    bot.user_data["cart"] = {}
    bot.user_data["cart_total"] = 0



check_out_handler = CallbackQueryHandler(callback=checkout, pattern="checkout")
direct_transfer_handler = CallbackQueryHandler(callback=direct_transfer, pattern="pay_with_direct_transfer")
confirm_direct_transfer_handler =  CallbackQueryHandler(callback=confirm_direct_transfer, pattern="direct_payment_confirm")

