from database.models import  Student
from database.query import is_user
from database.manipulate import commmit_student
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    ConversationHandler,
    MessageHandler,
)


# start handler
def start(update, bot):
    exist = is_user(update.effective_user.id) 
    if exist:
        reply_keyboard = [
            [InlineKeyboardButton(text="Customer Support", callback_data="customer_feedback")],
            [InlineKeyboardButton(text="Make Order", callback_data="make_order")],
             [InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")],
             [InlineKeyboardButton(text="Change Delivery Location", callback_data="edit_room")]
        ]
        markup = InlineKeyboardMarkup(reply_keyboard)
        bot.bot.send_message(
            chat_id=update.effective_chat.id,
            text="""
                Welcome to Byte & Crunch! \n How may we be of assistance to you?
                """,
            reply_markup=markup
        )
        
    else:
        reply_keyboard = [
            [InlineKeyboardButton(text="Let's Go!", callback_data="is_customer")],
        ]
        markup = InlineKeyboardMarkup(reply_keyboard)
        bot.bot.send_message(
            chat_id=update.message.chat_id,
            text="Welcome to Byte & Crunch Telegram Bot!",
            reply_markup=markup,
        )

        return 0


#is customer
def setup_customer(update, bot):
    query = update.callback_query
    message = query.edit_message_text(
            text="""
                Thank you for chooosing Byte & Crunch!
                \nWe need some information before you can continue to ordering your food!
                \nLet's start with  your name!
                """
            )
    bot.user_data["start_id"] = message.message_id
   
    return "mat_no"

def enter_mat_no(update, bot):
    name = update.message
    bot.user_data["user_type"] = Student(name=name.text)
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id=name.message_id)
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id= bot.user_data["start_id"])
    message = bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Next is your matric.no! \n please send your matric.no!"
    )
    bot.user_data["start_id"] = message.message_id
    return "email_"

def enter_email(update, bot):
    matno = update.message
    bot.user_data["user_type"].matno = matno.text
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id=matno.message_id)
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id= bot.user_data["start_id"])
    message = bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What's your email address?"
    )
    bot.user_data["start_id"] = message.message_id
    return "room_address"

def enter_room_address(update, bot):
    email = update.message
    bot.user_data["user_type"].email = email.text
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id=email.message_id)
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id= bot.user_data["start_id"])
    message = bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Where's your hall and room👀👀👀? \n This is delivery location(can be changed later in settings)"
    )
    bot.user_data["start_id"] = message.message_id
    return "confirm_details"



def confirm_details(update, bot):
    room = update.message
    user = bot.user_data["user_type"]
    bot.user_data["user_type"].room = room.text

    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id=room.message_id)
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id= bot.user_data["start_id"])
    name , matno, email = user.name, user.matno, user.email

    reply_keyboard = [
        [InlineKeyboardButton(text="Yes, Submit!", callback_data="save")],
        [InlineKeyboardButton(text="No, Re-enter Details", callback_data="return")],
    ]
    mark_up = InlineKeyboardMarkup(reply_keyboard)
    message = bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
            Here's what you entered: \n
            Name =>{name}
            Matric No => {matno}
            Email => {email}
            Room details => {room.text}

            Is this all correct?

            """,
        reply_markup=mark_up,
    )
    bot.user_data["start_id"] = message.message_id
    return "submit"



# save user to database
def submit(update, bot):
    bot.user_data["cart"] = {}
    bot.user_data["cart_total"] = 0
    user_type = bot.user_data['user_type']
    user_type.userid = update.effective_user.id
    if update.callback_query.data == "save":
        query = update.callback_query
        commmit_student(user_type)      
        reply_keyboard = [
         [
            InlineKeyboardButton(text="Back to home!", callback_data="start")
        ]
    ]
        markup = InlineKeyboardMarkup(reply_keyboard)  
        query.edit_message_text(
            text="Account Created Successfully!",
            reply_markup=markup 
        )
        del bot.user_data['user_type']
        del bot.user_data["start_id"]
        return ConversationHandler.END
    elif update.callback_query.data == "return":
        message = bot.bot.send_message(
            chat_id=update.effective_chat.id,
               text="""
                    Please enter your full name!
                    """,
                )
        bot.user_data["start_id"] = message.message_id
        return "mat_no"

    return ConversationHandler.END

def home(update, bot):
    query = update.callback_query
    reply_keyboard = [
            [InlineKeyboardButton(text="Customer Support", callback_data="customer_feedback")],
            [InlineKeyboardButton(text="Make Order", callback_data="make_order")],
            [InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")],
            [InlineKeyboardButton(text="Change Delivery Location", callback_data="edit_room")]
        ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text="""
            Welcome to Byte & Crunch! \n How may we be of assistance to you?
            """,
        reply_markup=markup
    )

def cancel(update,bot):
	update.message.reply_text('Operation canceled')
	return ConversationHandler.END


start_handler = CommandHandler("start", start, run_async=True)
setup_user_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(pattern="is_customer", callback=setup_customer, run_async=True)
        ],
    states= {
        "mat_no": [MessageHandler(Filters.all, enter_mat_no, run_async=True)],
        "email_":[MessageHandler(Filters.all, enter_email, run_async=True)],
        "room_address": [MessageHandler(Filters.all, enter_room_address, run_async=True)],
        "confirm_details" : [MessageHandler(Filters.all, confirm_details, run_async=True)],
        "submit": [CallbackQueryHandler(submit, run_async=True)]

    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
back_to_home = CallbackQueryHandler(callback=home, pattern="start")
