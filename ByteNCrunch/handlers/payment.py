from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler
from filters.helpers import compute_rates, flutterlink, status_check
from database.models import FlutterPayment, Student
import uuid
import requests
import os
from dotenv.main import load_dotenv
from database.query import get_product, get_status
from flask import make_response
import logging

load_dotenv()

logger = logging.getLogger(__name__)

CONFIRMATION, RESTART = range(2)
payment_list = {
    'payment_url': '',
    'reference': '',
}

def flutterwave_handler(update, bot):
    my_order = ""
    cart = list(bot.user_data["cart"].items())
    query = update.callback_query
    user_id = update.effective_user.id
    print("it reached here")
    total = int(bot.user_data["cart_total"])
    reference = str(uuid.uuid4())
    payment_list["reference"] = reference
    data = update.callback_query.data
    rate = compute_rates(total)
    subtotal = total + rate
    for i in cart:
        product = get_product(i[0])
        my_order += "{} orders of {} at {} paid {}".format(i[1], product[1], (int(product[3]) * i[1]), subtotal)
    print(my_order)
    link = flutterlink(subtotal, user_id, my_order, reference)
    payment_list["payment_url"] = link
    reply_keyboard = [[InlineKeyboardButton(text="YES", callback_data="yes")], [InlineKeyboardButton(text="NO", callback_data="no")]]
    markup = InlineKeyboardMarkup(reply_keyboard)
    bot.bot.send_message(chat_id=update.effective_chat.id, text=f"please make payments using this link: \n\n{link} \n Have you made payments?", reply_markup=markup)
    return CONFIRMATION

def handle_payment_confirmation(update, bot):
    print("got here")
    query = update.callback_query
    data = query.data

    if data == "yes":
        payment_ref = payment_list["reference"]
        status = get_status(payment_ref)
        print(status)
        print("testing")
        status_value = status_check(status)
        if (status_value == True):
            print("it was true")
            bot.bot.send_message(chat_id=update.effective_chat.id, text="Your order is being processed")
            return ConversationHandler.END
        else:
            print("it was false")
            link = payment_list["payment_url"]
            reply_keyboard = [[InlineKeyboardButton(text="YES", callback_data="yes")], [InlineKeyboardButton(text="NO", callback_data="no")]]
            markup = InlineKeyboardMarkup(reply_keyboard)
            bot.bot.send_message(chat_id=update.effective_chat.id, text=f"Your payment hasn't been confirmed. \nPlease make your payment using the link provided. \n\n{link} \n have you made payments?", reply_markup=markup)
            return CONFIRMATION
    else:
        # The user has not made payments
        link = payment_list["payment_url"]
        reply_keyboard = [[InlineKeyboardButton(text="YES", callback_data="yes")], [InlineKeyboardButton(text="NO", callback_data="no")]]
        markup = InlineKeyboardMarkup(reply_keyboard)
        bot.bot.send_message(chat_id=update.effective_chat.id, text=f"Please make your payment using the link provided. \n\n{link} \n have you made payments?", reply_markup=markup)
        return CONFIRMATION

def restart_conversation(update, context):
    query = update.callback_query
    query.answer()
    return ConversationHandler.START

def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

flutterwave_payment_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=flutterwave_handler, pattern="pay_with_flutter_wave")],
    states={
        CONFIRMATION: [CallbackQueryHandler(handle_payment_confirmation)],
        RESTART: [CallbackQueryHandler(restart_conversation)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
