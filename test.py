from ByteNCrunch.database.query import get_order
import telegram
import os

order = get_order("6a3cacaa-87da-4f96-85c8-7df2240378f0")
order += f"\n #flutterwavePayment"
print(order)
bot = telegram.Bot(token=os.getenv("TOKEN"))
bot.send_message(chat_id=os.getenv("order_group_id"), text=order)
