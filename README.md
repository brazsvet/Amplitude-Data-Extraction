# Amplitude Data Extraction

The script is extracting the Amplitude web-site hourly data from yesterday with the Amplitude API. API returns .zip files, consisting of .json.gz files.

The amplitude_extract.py script is calling the API, saving .zip files locally under the /data folder, then extracts .gz files and stores them under the /{start_time}-{end_time} folder and unpacks .json files under the /extracted_jsons

<img width="206" height="450" alt="image" src="https://github.com/user-attachments/assets/ba74c645-76d6-4989-9cc6-13b2a16f3b8e" />

To use program, open the amplitude_extract script and run it.

Here you can find the API information: https://amplitude.com/docs/apis/analytics/export

# Data Load to S3 Bucket

The load.py script is uploading the Amplitude data to the S3 bucket. Only files not existing in the bucket are being uploaded.
