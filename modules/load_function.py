import logging
import boto3
import os
from datetime import date

logger = logging.getLogger(__name__)

def s3_load(data_dir:str, date:date, AWS_ACCESS_KEY:str, AWS_SECRET_ACCESS_KEY:str, AWS_BUCKET_NAME:str):
    """The function is uploading the data for the chosen date from the given folder to the s3 bucket using given credentials. Only files that are not in the s3 bucket yet will be uploaded. Uploaded files will be removed from local folder.

    Args:
        data_dir (str): root data folder
        date (date): chosen date to upload the data
        AWS_ACCESS_KEY (str): AWS access key
        AWS_SECRET_ACCESS_KEY (str): AWS secret key
        AWS_BUCKET_NAME (str): s3 bucket name
    """

    # transform the date to the format of the file structure
    chosen_date = str(date).replace("-", "")
    start_time = f'{chosen_date}T00'
    end_time = f'{chosen_date}T23'

    files_path = f'{data_dir}/{start_time}-{end_time}/extracted_jsons'

    # # connect to AWS user
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # list all files in the yesterday folder
    files_extracted = os.listdir(files_path)

    # # list the files in the s3 bucket
    # objects = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
    # files_s3 = []
    # for my_bucket_object in objects['Contents']:
    #     files_s3.append(my_bucket_object['Key'])

    # only upload the files that are not in s3 bucket
    # files_to_upload = []
    # for file in files_extracted:
    #     if file not in files_s3:
    #         files_to_upload.append(file)

    # check if there are files to upload
    files_count = len(files_extracted)

    if files_count > 0:
        print(f'Files to upload: {files_count}')
        logger.info(f'Files to upload: {files_count}')
        
        # uploading the files to s3 bucket
        for file in files_extracted:
            filename_s3 = file
            file_to_upload = f'{files_path}/{file}'
            try:
                s3_client.upload_file(file_to_upload, AWS_BUCKET_NAME, filename_s3)
                print(f'File uploaded successfully: {file}')
                logger.info(f'File uploaded successfully: {file}')
                os.remove(file_to_upload)
                logger.info(f'File removed locally: {file}')
            except Exception as e:
                print(f'An error occurred: {e}')
                logger.error(f'An error occurred: {e}')
    else:
        print('No new files to upload')
        logger.warning('No new files to upload')
