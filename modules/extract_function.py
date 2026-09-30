import logging
import requests
import os
import zipfile
import gzip
import json
from datetime import date

logger = logging.getLogger(__name__)

def amplitude_extract(data_dir:str, url:str, date:date, api_key:str, secret_key:str):
    """The function is calling Amplitude API using given credentials and stores extracted json files to the data_dir folder. 
    The API call returnes the web-site event based data for the chosen date. 

    Args:
        data_dir (str): name of the directory where data files are stored
        url (str): API URL
        date (date): chosen date to retrieve the data
        AMP_API_KEY (str): Amplitude access key
        AMP_SECRET_KEY (str): Amplitude secret key
    """
    # transform the date to the Amplitude API accessable format
    chosen_date = str(date).replace("-", "")
    start_time = f'{chosen_date}T00'
    end_time = f'{chosen_date}T23'

    # time parameters for the API call
    params = {
        'start': start_time,
        'end': end_time
    }

    # API call
    response = requests.get(url, params=params, auth=(api_key, secret_key))

    # getting API request status
    status = response.status_code
    print(f'API response status code: {status}')
    logger.info(f'API response status code: {status}')

    # if connection was successfull
    if 200 <= status < 300:

        print("Response successfully recieved")
        logger.info("Response successfully recieved")

        # create the data directory
        os.makedirs(data_dir, exist_ok=True)

        # save the raw zip file
        zip_path = f'{data_dir}/{start_time}-{end_time}.zip'
        with open(zip_path, "wb") as f:
            f.write(response.content)
        print(f'File saved successfully. Destination: {zip_path}')
        logger.info(f'File saved successfully. Destination: {zip_path}')

        # extract the content from the .zip to .json.gz files
        gz_dir = f'{data_dir}/{start_time}-{end_time}'
        os.makedirs(gz_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(gz_dir)
        print(f"Archieve successfully unpacked. Destination: {gz_dir}")
        logger.info(f"Archieve successfully unpacked. Destination: {gz_dir}")

        # create folder for extracted jsons
        gz_path = f'{gz_dir}/{os.listdir(gz_dir)[0]}'
        folder_path = f'{gz_dir}/extracted_jsons'
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created: {folder_path}")
        logger.info(f"Folder created: {folder_path}")

        # extract all the .gz files from gz_dir to .json format
        files = 0
        for filename in os.listdir(gz_path):
            if filename.endswith(".json.gz"):
                files += 1
                json_path = os.path.join(folder_path, filename[:-3])  # removes .gz extension

                try:
                    with gzip.open(f'{gz_path}/{filename}', "rt", encoding="utf-8") as f:
                        data = f.read()
                        with open(json_path, "w") as file:
                            json.dump(data, file)
                    # delete unpacked .gz file
                    os.remove(f'{gz_path}/{filename}')
                except Exception as e:
                    print(f'An error has occured: {e}')
                    logger.error(f'An error has occured: {e}')

        if files >= 24:
            print(f'Files from {chosen_date} are complete. Files downloaded: {files}')
            logger.info(f'Files from {chosen_date} are complete. Files downloaded: {files}')
        elif files > 0:
            print(f'Files from {chosen_date} are incomplete. Files downloaded: {files}')
            logger.warning(f'Files from {chosen_date} are incomplete. Files downloaded: {files}')
        else:
            print(f'No files from {chosen_date}. Files downloaded: {files}')
            logger.error(f'No files from {chosen_date}. Files downloaded: {files}')

    elif status == 400:
        print("The file size of the exported data is too large. Shorten the time ranges and try again. The limit size is 4GB.")
        logger.error("The file size of the exported data is too large. Shorten the time ranges and try again. The limit size is 4GB.")
    elif status == 404:
        print("No data available for the time range requested.")
        logger.error("No data available for the time range requested.")
    elif status == 504:
        print("	The amount of data is large causing a timeout. For large amounts of data, use the Amazon S3 destination.")
        logger.error("	The amount of data is large causing a timeout. For large amounts of data, use the Amazon S3 destination.")
    else:
        print("Something went wrong. No data retrieved.")
        logger.critical("Something went wrong. No data retrieved.")