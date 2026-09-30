# import libraries and packages
from datetime import date
from datetime import timedelta
from datetime import datetime
from dotenv import load_dotenv
import os

# import functions
from modules.log_initialise import log_setup
from modules.extract_function import extract_json

# logging set up
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'log'

# logger initilisation
logger = log_setup(log_dir, timestamp)
logger.info('Logger successfully initialised')

# API URL
url = 'https://analytics.eu.amplitude.com/api/2/export'

# enviromental variables from .env file
load_dotenv()

# saving API credentials
api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")

# retrieving data from yesterday
yesterday = date.today() - timedelta(days = 1)

data_dir = 'data'

# extracting data
extract_json(data_dir, url, yesterday, api_key, secret_key)

