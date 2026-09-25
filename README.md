# Amplitude Data Extraction
This script is extracting the Amplitude web-site data with the Amplitude API. API returns .zip files, consisting of .json.gz files. 

The amplitude_extract script is calling the API, saving .zip files locally under the /data folder, then extracts .gz files and stores them under the /{start_time}-{end_time} folder and unpacks .json files under the /extracted_jsons

<img width="206" height="450" alt="image" src="https://github.com/user-attachments/assets/ba74c645-76d6-4989-9cc6-13b2a16f3b8e" />

To use program, open the amplitude_extract script and run it.

Here you can find the API information: https://amplitude.com/docs/apis/analytics/export
