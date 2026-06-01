

import logging
import os 
from datetime import datetime
from from_root import from_root


main_folder = "LOG"

main_folder_path = os.path.join(from_root(),main_folder)

log_file = f"{datetime.now().strftime('%d-%B-%Y-%H-%M-%S')}.log"

log_format = ' [%(name)s - %(asctime)s - %(levelname)s - %(module)s] - %(message)s'

log_file_path  = os.path.join(main_folder_path,log_file)

os.makedirs(main_folder_path,exist_ok=True)


logging.basicConfig(
    
    level=logging.INFO,
    format = log_format,
    datefmt= "%d-%B-%Y %H-%M-%S",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]

)

logger = logging.getLogger(__name__)

