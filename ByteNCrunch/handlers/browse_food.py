from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_products_from


# *add funtion to fetch product data before sending to browse product handler
# *integrate with ibiang's api

def browse_product(update, bot):
    query = update.callback_query
    vend = ((update.callback_query.data)[12:])
    products = get_products_from(vend)
    print(products)
    bot.user_data["products"] = products
    browse_state = 5
    bot.user_data["browse_state"] = browse_state
    my_products = products[0:browse_state]
    buttons = []
    for food in my_products:
        buttons.append(
            [InlineKeyboardButton(text=f"{food[1]}: #{food[3]}", callback_data=f"add_product_{food[0]}")]
        )
    reply_keyboard = buttons + [
            [
                # InlineKeyboardButton(text="Previous", callback_data="browse_products_previous"),
                InlineKeyboardButton(text="Next", callback_data="browse_products_next")
            ],
            [
                InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
            ]
        
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text="What do you feel like getting today?",
        reply_markup=markup,
    )

def add_product_extended(update,bot):
    query = update.callback_query
    match update.callback_query.data:
        case "browse_products_next":
            if bot.user_data["browse_state"] >= len(bot.user_data["products"]):
                state = bot.user_data["browse_state"]
                my_products = bot.user_data["products"][state-5:state]
                # bot.user_data["browse_state"] = state + 5
                buttons = []
                for food in my_products:
                    buttons.append(
                        [InlineKeyboardButton(text=f"{food[1]}: #{food[3]}", callback_data=f"add_product_{food[0]}")]
                    )
                reply_keyboard =buttons + [
                    
                        [
                            InlineKeyboardButton(text="Previous", callback_data="browse_products_previous"),
                            # InlineKeyboardButton(text="Next", callback_data="browse_products_next")
                        ],
                        [
                            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                        ]
                    
                ]
            else:
                state = bot.user_data["browse_state"]
                my_products = bot.user_data["products"][state:state+5]
                bot.user_data["browse_state"] = state + 5
                buttons = []
                for food in my_products:
                    buttons.append(
                        [InlineKeyboardButton(text=f"{food[1]}: #{food[3]}", callback_data=f"add_product_{food[0]}")]
                    )
                reply_keyboard =buttons + [
                    
                        [
                            InlineKeyboardButton(text="Previous", callback_data="browse_products_previous"),
                            InlineKeyboardButton(text="Next", callback_data="browse_products_next")
                        ],
                        [
                            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                        ]
                ]
                    

                
            
        case "browse_products_previous":
            state = bot.user_data["browse_state"]
            if state > 5:
                state = bot.user_data["browse_state"]
                my_products = bot.user_data["products"][state-10:state-5]
                bot.user_data["browse_state"] = state - 5
                buttons = []
                for food in my_products:
                    buttons.append(
                        [InlineKeyboardButton(text=f"{food[1]}: #{food[3]}", callback_data=f"add_product_{food[0]}")]
                    )
                reply_keyboard = buttons + [
                        [
                            InlineKeyboardButton(text="Previous", callback_data="browse_products_previous"),
                            InlineKeyboardButton(text="Next", callback_data="browse_products_next")
                        ],
                        [
                            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                        ]                    
                ]
            elif state == 5:
                state = bot.user_data["browse_state"]
                my_products = bot.user_data["products"][0:state]
                buttons = []
                for food in my_products:
                    buttons.append(
                        [InlineKeyboardButton(text=f"{food[1]}: #{food[3]}", callback_data=f"add_product_{food[0]}")]
                    )
                reply_keyboard = buttons + [
                        [
                            InlineKeyboardButton(text="Next", callback_data="browse_products_next")
                        ],
                        [
                            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
                        ]                    
                ]

    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text="What do you feel like getting today?",
        reply_markup=markup,
    )



browse_product_handler = CallbackQueryHandler(
    pattern="browse_shop_",
    callback= browse_product,
    run_async=True
    )
browse_product_ext_handler = CallbackQueryHandler(
    callback=add_product_extended,
    pattern="browse_products_",
    run_async=True
    )
