# Tally Convert PDF

This script converts PDF files to JPG images and moves the original PDF and corresponding metadata files to a target directory. It uses the `pdf2image` library for PDF to image conversion.

## Motivation

Originally this was designed to take a directory (or hierarchy) containing PDFs together with metadata (scanned tally reports from polling stations, with an auxiliary text file containing the results in digital format), and convert the report to an image easy to handle and publish, together with the original meta-information.

## Requirements

- Python 3.6+
- `pdf2image` library
- `pillow` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/tally-convert-pdf.git
    cd tally-convert-pdf
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Edit the `config.ini` file to set the source and target directories and the DPI for image conversion:

```ini
[paths]
source = ./origin
target = ./target
logs = 
flat_target = False

[image]
dpi = 300
meta = csv
```

- `source`: Directory containing the PDF files to be converted.
- `target`: Directory where the converted JPG images and original PDF/metadata files will be moved.
- `logs`: Directory for log files. If left empty, the script directory will be used.
- `flat_target`: If set to `True`, subdirectories in the source directory will not be replicated in the target. Notice that this can have undesired effects if filenames are not unique.
- `dpi`: DPI (dots per inch) setting for image conversion.
- `meta`: Extension of the metadata files (e.g., `csv`).

## Usage

Run the script:

```sh
python tally-convert-pdf.py
```

You can also specify an alternative configuration file:

```sh
python tally-convert-pdf.py --config /path/to/your/config.ini
```

The script will process each PDF file in the source directory, convert it to a JPG image, and move the original PDF and corresponding metadata file to the target directory.

## Logging

Logs are saved in the `pdf_conversion.log` file in the specified logs directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
