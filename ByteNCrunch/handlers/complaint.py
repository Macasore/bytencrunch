import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler
import os
from dotenv.main import load_dotenv
from filters.helpers import get_student

load_dotenv()

logger = logging.getLogger(__name__)
NAME, MATRIC_NO, EMAIL, HALL, DESCRIPTION, SUMMARY, CHECK, NAME_MESSAGE= range(8)
complaint = {
    'username': 'null',
    'full_name': '',
    'matric_no': '',
    'hall_roomno': '',
    'description': '',
    'email': '',
    'category': ','
}
def add_complaint(update, bot):
    query = update.callback_query
    reply_keyboard = [
        [InlineKeyboardButton(text="Payment Complaint", callback_data="PAYMENT COMPLAINT")],
        [InlineKeyboardButton(text="Delivery Complaint", callback_data="DELIVERY COMPLAINT")],
        [InlineKeyboardButton(text="Others", callback_data="OTHER COMPLAINT")],
        [InlineKeyboardButton(text="Back to Home!", callback_data="start")]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text="Please select your complaint category: ", 
        reply_markup=markup
    )
    user = update.effective_user
    username = user.username
    if username:
        complaint['username'] = user.username
        return NAME
    return NAME
    
def name(update, context):
    query = update.callback_query
    logger.info("THis user chose %s", query.data)
    complaint['category'] = query.data
    query.answer()
    reply_keyboard = [
        [InlineKeyboardButton(text="Cancel", callback_data="cancel")],
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(text="Please input your full-name: " ,reply_markup=markup)

    return MATRIC_NO
 
def name_message(update, context):
    user_message = update.message.text
    logger.info("This user chose %s'", user_message)
    update.message.reply_text("Please input your full-name: ")
    return MATRIC_NO

def matric_no(update, context):
     query = update.callback_query
     logger.info("THis user's fullname is %s'", update.message.text)
     complaint["full_name"] = update.message.text
     update.message.reply_text("Please input Matric number: ")
     
     return EMAIL
 
def email(update, context):
     query = update.callback_query
     logger.info("THis user's matric number is %s'", update.message.text)
     complaint["matric_no"] = update.message.text
     update.message.reply_text("Please input your email address: ")
     
     return HALL
 
def hall(update, context):
     query = update.callback_query
     logger.info("THis user's email address is %s'", update.message.text)
     complaint["email"] = update.message.text
     update.message.reply_text("Please enter you hall and room number eg: Daniel E403: ")
     
     return DESCRIPTION
 
 
def desc(update, context):
     query = update.callback_query
     logger.info("This user's email is %s'", update.message.text)
     complaint["hall_roomno"] = update.message.text
     update.message.reply_text("Please input your complaint description: ")
     
     return SUMMARY
 
def summary(update, context):
     query = update.callback_query
     logger.info("THis user's complaint is %s'", update.message.text)
     complaint["description"] = update.message.text
     user_id = update.effective_user.id
     student = get_student(user_id)
     print(student)
    #  user_email = student[4]
    #  complaint["email"] = user_email
     reply_keyboard = [
        [InlineKeyboardButton(text="YES", callback_data="YES")],
        [InlineKeyboardButton(text="NO", callback_data="NO")]
     ]
     print(complaint['description'])
     markup = InlineKeyboardMarkup(reply_keyboard)
     update.message.reply_text(text="""Here are your details:\n "Category":{} \n Name: {} \n Matric number: {} \n Email: {} \n Room_number: {} \n Complaint: {} \n\n are these details correct?
                               
                               """.format(complaint['category'], complaint["full_name"],
                                          complaint["matric_no"], complaint["email"], complaint["hall_roomno"],
                                          complaint["description"]),reply_markup=markup)
     return CHECK
 
def check(update, context):
    query = update.callback_query
    logger.info("This user's check is %s'", query.data)
    check = query.data

    if check == 'YES':
        query.answer()
        reply_keyboard = [
        [InlineKeyboardButton(text="Back to Home!", callback_data="start")],
    ]
        markup = InlineKeyboardMarkup(reply_keyboard)
        query.edit_message_text("Thank you for your feedback, Our customer service team would reach out to you via your email shortly\n",
                                reply_markup = markup)
        group_chat_id = os.getenv('complaint_group_id')
        summary_text = f"Category: {complaint['category']}\nName: {complaint['full_name']}\nMatric number: {complaint['matric_no']}\n Email: {complaint['email']} \nRoom_number: {complaint['hall_roomno']}\nComplaint: {complaint['description']}"
        context.bot.send_message(chat_id=group_chat_id, text=summary_text)
        return ConversationHandler.END
    elif check == 'NO':
        query.answer()
        query.edit_message_text("please input 'continue'\n")
        return NAME_MESSAGE
    
        
def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END   

complaint_handler = ConversationHandler(
    entry_points = [CallbackQueryHandler(pattern="customer_feedback",callback=add_complaint, run_async=True)],
    states={
        NAME: [CallbackQueryHandler(name)],
        NAME_MESSAGE: [MessageHandler(Filters.text & ~Filters.command, name_message, run_async=True)],
        MATRIC_NO: [MessageHandler(Filters.text & ~Filters.command, matric_no, run_async=True)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, email, run_async=True)],
        HALL: [MessageHandler(Filters.text & ~Filters.command, hall, run_async=True)],
        DESCRIPTION: [MessageHandler(Filters.text & ~Filters.command, desc, run_async=True)],
        SUMMARY: [MessageHandler(Filters.text & ~Filters.command, summary,  run_async=True)],
        CHECK: [CallbackQueryHandler(check)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    )
