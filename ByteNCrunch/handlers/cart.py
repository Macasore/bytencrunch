from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler
from database.query import get_product
from filters.helpers import cart_to_lol


def add_to_cart(update, bot):
    query = update.callback_query
    data = update.callback_query.data
    button = []
    match data[:13]:
        #anything to dodge regex, lol
        case "cart_quan_add":
            product_id = update.callback_query.data[18:]
            print(product_id)
            product = get_product(product_id)
            product_count = bot.user_data["product_count"] 
            product_count +=1
            bot.user_data["product_count"] = product_count
            button =  [
                       [ InlineKeyboardButton(text="-1", callback_data=f"cart_quan_minus_one_{product_id}"),
                        InlineKeyboardButton(text="+1", callback_data=f"cart_quan_add_one_{product_id}")]
                    ]
        case "cart_quan_min":
            if bot.user_data["product_count"] > 1:
                product_id = update.callback_query.data[20:]
                product = get_product(product_id)
                product_count = bot.user_data["product_count"]
                product_count -=1
                bot.user_data["product_count"] = product_count
                button =  [
                            [InlineKeyboardButton(text="-1", callback_data=f"cart_quan_minus_one_{product_id}"),
                            InlineKeyboardButton(text="+1", callback_data=f"cart_quan_add_one_{product_id}")]
                        ]
            else:
                product_id = update.callback_query.data[20:]
                product = get_product(product_id)
                product_count = 1
                bot.user_data["product_count"] = product_count
                button =  [[InlineKeyboardButton(text="+1", callback_data=f"cart_quan_add_one_{product_id}")]]

        case _:
            product_id = update.callback_query.data[12:]
            product = get_product(product_id)
            product_count = 1
            bot.user_data["product_count"] = product_count
            button =  [
                       [InlineKeyboardButton(text="+1", callback_data=f"cart_quan_add_one_{product_id}")]
                    ]
    
    reply_keyboard = button + [
       
        [
            InlineKeyboardButton(text="Add to cart", callback_data=f"add_to_cart_{product_id}_{product_count}")
        ],
        [
            InlineKeyboardButton(text="Cancel", callback_data="start")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=f"Add {product[1]} to cart?  \nQuantity : {product_count} \nPrice : # {int(product[3] * product_count)}",
        reply_markup=markup,
    )

def add_to_cart_confirm(update, bot):
    query = update.callback_query
    data = update.callback_query.data
    product_id = int(data[12:].split("_")[0])
    product_count = int(data[12:].split("_")[1])
    if product_id in bot.user_data["cart"].keys():
        bot.user_data["cart"][product_id] += product_count    
    else:
        bot.user_data["cart"][product_id] = product_count
    bot.user_data["cart_total"] += product_count * get_product(product_id)[3]
    print(get_product(product_id)[3])
    reply_keyboard = [
        
        [
            InlineKeyboardButton(text="Proceed to Checkout", callback_data="checkout")
        ] ,
         [
            InlineKeyboardButton(text="Manage Cart", callback_data="manage_cart")
        ] ,
        [InlineKeyboardButton(text="Continue shopping!", callback_data="make_order")],
        [
            InlineKeyboardButton(text="Back to Home!", callback_data="start")
        ]
    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=f"{product_count} order(s) of {get_product(product_id)[1] }added to cart!",
        reply_markup=markup,
    )


def manage_cart(update, bot):
    cart = cart_to_lol(bot.user_data["cart"])
    query = update.callback_query
    if len(cart) == 0:
        my_text = "Nothing to see here!👀"
        reply_keyboard = [
            [
                InlineKeyboardButton(text="Back to Home!", callback_data="start")
            ]

        ]
    else:
        my_text = "Here's what you have in your cart right now!"
        for i in cart:
            product = get_product(i[0])
            my_text += f"\n >> {i[1]} orders of {product[1]} at # {int(product[3]) * i[1]}"

        
        reply_keyboard = [
            
            [
                InlineKeyboardButton(text="Edit Cart Items", callback_data="edit_cart"),
                InlineKeyboardButton(text="Proceed to Checkout", callback_data="checkout")
            ] ,
            [
                InlineKeyboardButton(text="Back to Home!", callback_data="start")
            ]

        ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=my_text,
        reply_markup=markup,
    )

def edit_cart(update, bot):
    query = update.callback_query
    data= query.data
    cart = cart_to_lol(bot.user_data["cart"])
    my_text = ""
    if len(bot.user_data["cart"]) == 0:
        my_text = "Hello there! \n There's nothing here👀"
        reply_keyboard  = [
            [
                InlineKeyboardButton(text="Back to Home!", callback_data="start")
            ]
        ]

    else:
        buttons = [
            [
                InlineKeyboardButton(text="-1", callback_data="edit_cart_less_one"),
                InlineKeyboardButton(text="+1", callback_data="edit_cart_plus_one"),
            ],
            [
                InlineKeyboardButton(text="Previous", callback_data="edit_cart_prev"),
                InlineKeyboardButton(text="Next", callback_data="edit_cart_next")
            ],
        ]
        match data:
            case "edit_cart":
                browse_state = 0
                bot.user_data["browse_state"] = browse_state
                cart_item = cart[browse_state]
                product_id = cart_item[0]
                count = cart_item[1]
                product = get_product(product_id)
                my_text = f"{count} order(s) of {product[1]} at {product[3]} each. \n Subtotal=> {product[3]*count}"
            case "edit_cart_less_one" | "edit_cart_plus_one":
                browse_state = bot.user_data["browse_state"] 
                print(browse_state)
                match data:
                    case "edit_cart_less_one":
                        if cart[browse_state][1] >1:
                            bot.user_data["cart"][cart[browse_state][0]] -= 1
                            if len(bot.user_data["cart"]) == 0:
                                my_text = "Nothing here! \n /start to go back home"
                            else:
                                cart = cart_to_lol(bot.user_data["cart"])
                                cart_item = cart[browse_state]
                                product_id = cart_item[0]
                                count = cart_item[1]
                                product = get_product(product_id)
                                my_text = f"{count} order(s) of {product[1]} at {product[3]} each. \n Subtotal=> {product[3]*count}"
                                
                        else:
                            cart_item = cart[browse_state]
                            product_id = cart_item[0]
                            del(bot.user_data["cart"][product_id])
                            if len(bot.user_data["cart"]) == 0:
                                my_text = "Nothing here! \n /start to go back home"
                            else:
                                browse_state = 0
                                cart = list(bot.user_data["cart"].items())
                                cart_item = cart[browse_state]
                                product_id = cart_item[0]
                                count = cart_item[1]
                                product = get_product(product_id)
                                bot.user_data["browse_state"] = browse_state
                                my_text = f"{count} order(s) of {product[1]} at {product[3]} each. \n Subtotal=> {product[3]*count}"
                    case "edit_cart_plus_one": 
                        bot.user_data["cart"][cart[browse_state][0]] += 1
                
                        cart = cart_to_lol(bot.user_data["cart"])
                        cart_item = cart[browse_state]
                        product_id = cart_item[0]
                        count = cart_item[1]
                        product = get_product(product_id)
                        my_text = f"{count} order(s) of {product[1]} at {product[3]} each. \n Subtotal=> {product[3]*count}"
            case "edit_cart_kill_one":
                browse_state = bot.user_data["browse_state"] 
                cart_item = cart[browse_state]
                product_id = cart_item[0]
                del(bot.user_data["cart"][product_id])
                if len(bot.user_data["cart"]) == 0:
                    my_text = "Nothing here! \n /start to go back home"
                else:
                    browse_state = 0
                    cart = list(bot.user_data["cart"].items())
                    cart_item = cart[browse_state]
                    product_id = cart_item[0]
                    count = cart_item[1]
                    product = get_product(product_id)
                    bot.user_data["browse_state"] = browse_state
                    my_text = f"{count} order(s) of {product[1]} at {product[3]} each. \n Subtotal=> {product[3]*count}"

            case "edit_cart_next" | "edit_cart_prev":
                match data:
                    case "edit_cart_next":
                        browse_state = bot.user_data["browse_state"]
                        if browse_state + 1 == len(cart):
                            del(buttons[1][1])
                        else:
                            browse_state = bot.user_data["browse_state"] + 1
                    case "edit_cart_prev":
                        browse_state = bot.user_data["browse_state"]
                        if browse_state == 0:
                            del(buttons[1][0])
                        else:
                            browse_state = bot.user_data["browse_state"] - 1
                bot.user_data["browse_state"] = browse_state
                cart_item = cart[browse_state]
                product_id = cart_item[0]
                count = cart_item[1]
                product = get_product(product_id)
                my_text = f"{count} order(s) of {product[1]} at {product[3]} each. \n Subtotal=> {product[3]*count}"

        reply_keyboard  = buttons + [
            [
                InlineKeyboardButton(text="Delete Item", callback_data="edit_cart_kill_one")
            ],
            [
                InlineKeyboardButton(text="Done", callback_data="manage_cart"),
                InlineKeyboardButton(text="Back to Home!", callback_data="start")
            ]
        ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    query.edit_message_text(
        text=my_text,
        reply_markup=markup,
    )

    
add_to_cart_handler = CallbackQueryHandler(callback=add_to_cart, pattern="add_product_", run_async=True )
cart_quantity_handler = CallbackQueryHandler(callback=add_to_cart, pattern="cart_quan_", run_async=True)
confirm_cart = CallbackQueryHandler(callback=add_to_cart_confirm, pattern="add_to_cart_")
manage_cart_handler = CallbackQueryHandler(callback=manage_cart, pattern="manage_cart")
edit_cart_handler= CallbackQueryHandler(callback=edit_cart, pattern="edit_cart", run_async=True)
