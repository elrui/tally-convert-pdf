import os
import shutil
import logging
import configparser
from pdf2image import convert_from_path

# Configuration loader function
def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

# Get script path
script_path = os.path.dirname(os.path.realpath(__file__))

# Load configuration
config_path = os.path.join(script_path, 'config.ini')
config = load_config(config_path)

# Read config parameters
source = config.get('paths', 'source')
target = config.get('paths', 'target')
dpi    = config.getint('image', 'dpi')

# If logs route is not provided, use script directory
logs_path = config.get('paths', 'logs')
if not logs_path.strip():
    logs_path = script_path

os.makedirs(target, exist_ok=True)
os.makedirs(logs_path, exist_ok=True)

# Config  logging
log_file = os.path.join(logs_path, 'pdf_conversion.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Starting conversion process.")

# Process each pdf on source directory
counter = 0
for file in os.listdir(source):
    if file.lower().endswith('.pdf'):
        base_name, _ = os.path.splitext(file)
        pdf_path  = os.path.join(source, file)
        csv_path = os.path.join(source, f"{base_name}.csv")
        
        # Verify if CSV exists. If not, skip processing
        if os.path.exists(csv_path):
            try:
                # Convert PDF to JPG image
                pages = convert_from_path(pdf_path, dpi=dpi, fmt='jpeg')
                image = pages[0]  # Assuming always one page

                jpg_path = os.path.join(target, f"{base_name}.jpg")
                image.save(jpg_path, 'JPEG')
                logging.info(f"Converted to JPG: {base_name}.jpg")
            except Exception as e:
                logging.error(f"Conversion error for {file} to JPG: {e}")
                continue

            try:
                # MOve PDF and CSV to target directory
                shutil.move(pdf_path, os.path.join(target, file))
                shutil.move(csv_path, os.path.join(target, f"{base_name}.csv"))
                logging.info(f"Moved: {file} and {base_name}.csv to {target}")

                counter += 1
            except Exception as e:
                logging.error(f"Error moving files: {base_name}: {e}")
        else:
            logging.warning(f"CSV not found for {file}. Skipping processing.")
    else:
        continue

logging.info(f"End of conversion process. {counter} files processed.")
