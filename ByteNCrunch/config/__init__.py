from dotenv import load_dotenv
import os

load_dotenv()


# config = dotenv_values(".env")
TOKEN = os.environ["TOKEN"]
DB_HOST =os.environ["DB_HOST"]
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ["DB_PASSWORD"]
DATABASE = os.environ["DATABASE"]