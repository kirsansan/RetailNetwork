import os
# install as python-dotenv
from dotenv import load_dotenv


load_dotenv()




# for future in case of notices via e-mail
# MY_EMAIL = os.getenv('MY_EMAIL')
# MY_EMAIL_PASSWORD = os.getenv('MY_EMAIL_PASSWORD')
# MY_EMAIL_HOST = os.getenv('MY_EMAIL_HOST')
# MY_EMAIL_PORT = int(os.getenv('MY_EMAIL_PORT'))
# if os.getenv('EMAIL_SENDING_SIMULATION_MODE') == 'False':
#     EMAIL_SENDING_SIMULATION_MODE = False
# else:
#     EMAIL_SENDING_SIMULATION_MODE = True


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

HIERARCHY_MODE = True
# in this mode only Factory-type node might be available as Supplier for RetailNetwork node
# and only RetailNetwork-type node might be available as Supplier for IndividualEntrepreneur
