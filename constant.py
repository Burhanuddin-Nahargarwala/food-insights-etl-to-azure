from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.environ.get("USERNAME")
db_password = os.environ.get("PASSWORD")
db_host = os.environ.get("HOST")
db_port = '5432'
db_name = os.environ.get("DB_NAME")