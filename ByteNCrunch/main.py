import logging
from handlers import all_handlers
from config import TOKEN
from telegram.ext import Updater 
from threading import Thread
from webhook_server import app

def run_flask_server():
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    flask_thread = Thread(target=run_flask_server)
    flask_thread.start()
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    for handler in all_handlers:
        dispatcher.add_handler(handler)


    updater.start_polling()