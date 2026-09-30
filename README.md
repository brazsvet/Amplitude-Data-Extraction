# Amplitude to S3 Extract & Load Pipeline

An automated data extraction and loading pipeline that fetches hourly analytics data from Amplitude's Export API and syncs missing files to an Amazon S3 bucket.

## Prerequisites

- Python 3.12
- An active [Amplitude API Key and Secret Key](https://amplitude.com/docs/apis/analytics/export)
- AWS credentials with write permissions (`s3:PutObject`, `s3:ListBucket`) to your target S3 bucket

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory of the project using the template below. Both Amplitude and AWS credentials are stored here.

```env
# Amplitude Credentials
AMP_API_KEY=your_amplitude_api_key
AMP_SECRET_KEY=your_amplitude_secret_key

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=your_aws_region
AWS_BUCKET_NAME=your_s3_bucket_name
```

## Usage

### 1. Extract Data from Amplitude

Run the extraction script to download yesterday's hourly event data from Amplitude and uploads it to the s3 bucket:

```bash
python main.py
```

Ensure your S3 bucket is created and your `.env` configuration contains your AWS credentials.

#### Workflow & Directory Structure

The `amplitude_extract()` function:

1. **Fetch & Download:** Calls the Amplitude Export API for yesterday's hourly data and saves raw `.zip` archives locally in the `/data` folder.
2. **Decompress:** Extracts `.gz` files into `/{start_time}-{end_time}` directories.
3. **Unpack:** Unpacks all `.json` files (one per hour) into the `/extracted_jsons` directory.

The `s3_load()` function:

- **Idempotent Upload:** The script checks the contents of your S3 bucket prior to uploading. Only `.json` files that are not already present in the target S3 bucket will be uploaded.

> **API Reference:** For information on status codes, rate limits, and API specs, visit the [Amplitude Export API Documentation](https://amplitude.com/docs/apis/analytics/export).

## Directory Structure

```text
.
├── .env                    # Project configuration & credentials
├── requirements.txt        # Python package dependencies
├── main.py                 # The main script, automatically calls all other dependencies
├── modules/                # The folder containing functions
├──── log_initialise.py     # Initialise the logging
├──── amplitude_extract.py  # Amplitude extraction script
├──── load_function.py      # S3 loader script
├── data/                   # Downloaded .zip files
├── log/                    # Logs folder
├──── {start}-{end}/        # Decompressed .gz files
└──── extracted_jsons/      # Final output .json files (1+ per hour)
```

## Author

Svetlana Brazukevich

## License

MIT
