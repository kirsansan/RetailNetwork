import os
# install as python-dotenv
from dotenv import load_dotenv

load_dotenv()

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ENV_TYPE = os.getenv('ENV_TYPE')

if ENV_TYPE == 'local':
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PORT = int(os.getenv('POSTGRES_PORT'))
    DB_BASE_NAME = os.getenv('POSTGRES_BASE')
    DB_HOST = 'localhost'
elif ENV_TYPE == 'external-with-servers-postgres':
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_USER = 'postgres'
    DB_PORT = '5432'
    DB_BASE_NAME = os.getenv('POSTGRES_BASE')
    DB_HOST = 'localhost'
else:
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PORT = int(os.getenv('POSTGRES_PORT'))
    DB_BASE_NAME = os.getenv('POSTGRES_BASE')
    DB_HOST = os.getenv('POSTGRES_HOST')

LOG_FILE_NAME = "retailnetwork_log.log"

MAX_NODE_PER_PAGE = 10
