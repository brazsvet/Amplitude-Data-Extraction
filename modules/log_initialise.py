import logging
import os

def log_setup(log_dir:str, timestamp:str):
    """Initialising the logger.

    Args:
        log_dir (str): _description_
        timestamp (str): _description_
    """
    os.makedirs(log_dir, exist_ok = True)
    log_filename = f'{log_dir}/{timestamp}.log'

    # configure logging so messages are written to the log file
    logging.basicConfig(
        filename = log_filename,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO
    )

    # create the logger and confirm that it has been successfully set up
    return logging.getLogger()
    
