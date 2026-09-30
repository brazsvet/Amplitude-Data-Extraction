# import libraries and packages
from datetime import date
from datetime import timedelta
from datetime import datetime
from dotenv import load_dotenv
import os

# import functions
from modules.log_initialise import log_setup
from modules.extract_function import amplitude_extract
from modules.load_function import s3_load

### logger

# logging set up
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'log'

# logger initilisation
logger = log_setup(log_dir, timestamp)
logger.info('Logger successfully initialised')

### Amplitude data extract

# API URL
url = 'https://analytics.eu.amplitude.com/api/2/export'

# enviromental variables from .env file
load_dotenv()

# getting API credentials
api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")

# retrieving data from yesterday
yesterday = date.today() - timedelta(days = 1)

data_dir = 'data'

# extracting data
amplitude_extract(data_dir, url, yesterday, api_key, secret_key)

### load data to s3 bucket

# getting AWS credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# loading data
s3_load(data_dir, yesterday, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)