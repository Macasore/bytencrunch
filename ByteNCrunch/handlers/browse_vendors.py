from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_all_vendors


# *add funtion to fetch product data before sending to browse product handler
# *integrate with ibiang's api

def browse_shops_init(update, bot):
    query = update.callback_query
    vendors = get_all_vendors()
    try :
        cart = bot.user_data["cart"]
    except:
        bot.user_data["cart"] = {}
        bot.user_data["cart_total"] = 0

    print(vendors)
    bot.user_data["vendors"] = vendors
    browse_state = 5
    bot.user_data["browse_state"] = browse_state
    my_vendors = vendors[0:browse_state]
    buttons = []
    for vendor in my_vendors:
        buttons.append(
            [InlineKeyboardButton(text=vendor[1], callback_data=f"browse_shop_{vendor[0]}")]
        )
    reply_keyboard = buttons + [
        
            [
                InlineKeyboardButton(text="Next", callback_data="browse_vendors_next")
            ],
            [
                InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
           ,
            InlineKeyboardButton(text="Back to Home!", callback_data="start")
        ]
        
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text="What do you feel like getting today? \n Hurry up though, we stop taking orders by 4pm",
        reply_markup=markup,
    )

# def browse_shops_init(update, bot):
#     query = update.callback_query
#     buttons = [[

#             InlineKeyboardButton(text="Back to Home!", callback_data="start")
#         ]]
#     reply_keyboard = buttons
#     markup = InlineKeyboardMarkup(reply_keyboard)
#     query.edit_message_text(
#         text="Sorry we're currently down for maintenance! \n Sorry for the inconvenience, we'll be back in a bit!",
#         reply_markup=markup,
#     )

def browse_vendors(update,bot):
    query = update.callback_query
    match update.callback_query.data:
        case "browse_vendors_next":
            if bot.user_data["browse_state"] >= len(bot.user_data["vendors"]):
                state = bot.user_data["browse_state"]
                my_vendors = bot.user_data["vendors"][state-5:state]
                buttons = []
                for vendor in my_vendors:
                    buttons.append(
                        [InlineKeyboardButton(text=vendor[1], callback_data=f"browse_shop_{vendor[0]}")]
                    )
                reply_keyboard =buttons+ [    
                        [
                        InlineKeyboardButton(text="Previous", callback_data="browse_vendors_previous"),
                        ],
                        [
                            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                   ,
            InlineKeyboardButton(text="Back to Home!", callback_data="start")
        ]
                    ]
            else: 
                state = bot.user_data["browse_state"]
                my_vendors = bot.user_data["vendors"][state:state+5]
                bot.user_data["browse_state"] = state + 5
                buttons = []
                for vendor in my_vendors:
                    buttons.append(
                        [InlineKeyboardButton(text=vendor[1], callback_data=f"browse_shop_{vendor[0]}")]
                    )
                reply_keyboard =buttons+ [    
                        [
                        InlineKeyboardButton(text="Previous", callback_data="browse_vendors_previous"),
                        InlineKeyboardButton(text="Next", callback_data="browse_vendors_next")
                        ],
                        [
                            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                      ,
            InlineKeyboardButton(text="Back to Home!", callback_data="start")
        ]
                    ]
            
            
        case "browse_vendors_previous":
            state = bot.user_data["browse_state"]
            if state > 5:
                state = bot.user_data["browse_state"]
                my_vendors = bot.user_data["vendors"][state-10:state-5]
                bot.user_data["browse_state"] = state - 5
                buttons = []
                for vendor in my_vendors:
                    buttons.append(
                        [InlineKeyboardButton(text=vendor[1], callback_data=f"browse_shop_{vendor[0]}")]
                    )
                reply_keyboard = buttons+ [

                    [
                    InlineKeyboardButton(text="Previous", callback_data="browse_vendors_previous"),
                    InlineKeyboardButton(text="Next", callback_data="browse_vendors_next")
                    ],
                    [
                        InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                  ,
            InlineKeyboardButton(text="Back to Home!", callback_data="start")
        ]
                ]
            elif state == 5:
                state = bot.user_data["browse_state"]
                my_vendors = bot.user_data["vendors"][0:state]
                buttons = []
                for vendor in my_vendors:
                    buttons.append(
                        [InlineKeyboardButton(text=vendor[1], callback_data=f"browse_shop_{vendor[0]}")]
                    )
                reply_keyboard = buttons+[
                    
                    [
                    InlineKeyboardButton(text="Next", callback_data="browse_vendors_next")
                    ,
                        InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                    ],
        [
            InlineKeyboardButton(text="Back to Home!", callback_data="start")
        ]
                ]

    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text="What do you feel like getting today?",
        reply_markup=markup,
    )



browse_vendor_handler = CallbackQueryHandler(callback=browse_shops_init, pattern="make_order", run_async=True)
browse_vendor_ext_handler = CallbackQueryHandler(callback=browse_vendors, pattern="browse_vendors_", run_async=True)
