from flask import Flask, render_template, request, make_response, jsonify
from database.query import update_status
import requests
from dotenv.main import load_dotenv
from threading import Thread
from telegram.ext import Updater
from handlers import all_handlers
import os
import json
import logging
load_dotenv()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(os.getenv("TOKEN"))
    dispatcher = updater.dispatcher
    for handler in all_handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()
