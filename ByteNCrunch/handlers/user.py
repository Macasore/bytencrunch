from database.manipulate import  update_room
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    Filters,
    ConversationHandler,
    MessageHandler,
)


def edit_room(update, bot):
    query = update.callback_query
    reply_keyboard = [
             [
                InlineKeyboardButton(text="Cancel", callback_data="start")
            ]
        ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    message = query.edit_message_text(
        text="""
            Where would you want you orders sent to?
            """,
        reply_markup=markup
    )
    bot.user_data["start_id"] = message.message_id
    return "room"

def confirm_room(update,bot):
    room = update.message
    userid = update.effective_user.id
    update_room(user_id=userid,room=room.text)
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id=room.message_id)
    bot.bot.delete_message(chat_id=update.effective_chat.id,message_id= bot.user_data["start_id"])
    reply_keyboard = [
             [
                InlineKeyboardButton(text="Back to Home!", callback_data="start")
            ]
        ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    message = bot.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Delivery location set to => {room.text}",
        reply_markup = markup
    )
    bot.user_data["start_id"] = message.message_id
    return ConversationHandler.END

edit_room_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=edit_room, pattern="edit_room")],
    states= {
        "room" : [MessageHandler(Filters.all, confirm_room, run_async=True)]
    },
    fallbacks=[]
)
