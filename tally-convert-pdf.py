__version__ = "1.1.1"

import os
import shutil
import logging
import time
import configparser
import argparse
from pdf2image import convert_from_path

# Configuration loader function
def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

# Get script path
script_path = os.path.dirname(os.path.realpath(__file__))

# Parse command-line arguments for an alternative config file
parser = argparse.ArgumentParser(description="PDF to JPG conversion script")
parser.add_argument('--config', type=str, default=os.path.join(script_path, 'config.ini'),
                    help="Path to configuration file")
args = parser.parse_args()
config_path = args.config

# Load configuration
config = load_config(config_path)

# Read config parameters
source      = config.get('paths', 'source')
target      = config.get('paths', 'target')
dpi         = config.getint('image', 'dpi')
flat_target = config.getboolean('paths', 'flat_target', fallback=False)
meta        = config.get('image', 'meta', fallback="").strip()  # New meta parameter

# If logs path is not provided, use script directory
logs_path = config.get('paths', 'logs')
if not logs_path.strip():
    logs_path = script_path

os.makedirs(target, exist_ok=True)
os.makedirs(logs_path, exist_ok=True)

# Configure logging
log_file = os.path.join(logs_path, 'pdf_conversion.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Starting conversion process using pdf2image.")

counter = 0  # Counter for processed files

# Start timer
start_time = time.time()

# Walk through all subdirectories in the source directory
for root, dirs, files in os.walk(source):
    # Compute relative path to maintain structure in target directory
    rel_path = os.path.relpath(root, source)
    
    # if flat_target is set to True, ignore subdirectories
    if flat_target:
        target_dir = target
    else:
        target_dir = os.path.join(target, rel_path)
        os.makedirs(target_dir, exist_ok=True)
    
    for file in files:
        if file.lower().endswith('.pdf'):
            base_name, _ = os.path.splitext(file)
            pdf_path = os.path.join(root, file)
            
            # If meta is provided, check for the corresponding meta file
            if meta:
                meta_file = f"{base_name}.{meta}"
                meta_path = os.path.join(root, meta_file)
                if not os.path.exists(meta_path):
                    logging.warning(f"Meta file not found for {os.path.join(rel_path, file)}. Skipping processing.")
                    continue
            # If meta is not provided, processing continues without checking for it.
            
            try:
                # Convert PDF to JPG image using pdf2image
                pages = convert_from_path(pdf_path, dpi=dpi, fmt='jpeg')
                image = pages[0]  # Assuming always one page

                jpg_path = os.path.join(target_dir, f"{base_name}.jpg")
                image.save(jpg_path, 'JPEG')
                logging.info(f"Converted to JPG: {os.path.join(rel_path, base_name)}.jpg")
            except Exception as e:
                logging.error(f"Conversion error for {os.path.join(rel_path, file)} to JPG: {e}")
                continue

            try:
                # Move PDF to target directory, maintaining structure
                shutil.move(pdf_path, os.path.join(target_dir, file))
                logging.info(f"Moved PDF: {os.path.join(rel_path, file)} to {target_dir}")
            except Exception as e:
                logging.error(f"Error moving PDF: {os.path.join(rel_path, base_name)}: {e}")
                continue

            if meta:
                try:
                    # Move meta file to target directory, maintaining structure
                    shutil.move(meta_path, os.path.join(target_dir, meta_file))
                    logging.info(f"Moved meta file: {os.path.join(rel_path, meta_file)} to {target_dir}")
                except Exception as e:
                    logging.error(f"Error moving meta file: {os.path.join(rel_path, base_name)}: {e}")
                    continue

            counter += 1

end_time = time.time()
elapsed_time = end_time - start_time
logging.info(f"Execution time: {elapsed_time:.2f} seconds")
logging.info(f"End of conversion process. {counter} files processed.")

print(f"Conversion process finished. {counter} files processed in {elapsed_time:.2f} seconds.")
