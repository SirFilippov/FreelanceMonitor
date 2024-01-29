import logging
import os
from os import getenv
from dotenv import load_dotenv

env_file = os.path.abspath('.env')
load_dotenv(env_file)

TELEGA_TOKEN = getenv('TELEGA_TOKEN')
TELEGA_ADMIN_ID = getenv('TELEGA_ADMIN_ID')

MONGO_PORT = 27017
MONGO_HOST = 'localhost'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s]: %(message)s",
    encoding='utf-8',
)
