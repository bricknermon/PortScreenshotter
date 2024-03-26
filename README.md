# PortScreenShotter

PortScreenShotter is a Python tool designed to capture screenshots of web pages served on HTTP (80) and HTTPS (443) ports. It facilitates network audits by quickly visualizing accessible web content across different IP addresses.

## Installation

First, clone this repository:

```git clone https://github.com/bricknermon/PortScreenshotter```

Then navigate into the project directory:

```cd PortScreenShotter```

Install the required packages:

```pip install -r requirements.txt```


## Usage

1. Update the `open_port_443_80_scannedForContent.csv` file with the IPs and domains you wish to scan.
2. Run the scripts:

```python crawler.py``` (Ensures content is hosted on open port, optimizes screenshot runtime. Run first.)

```python screenshot.py``` 


Results, including paths to screenshots for accessible pages, will be logged in `open_80_443_scan_results.csv`.

## Requirements

- Python 3.x
- Selenium
- openpyxl
- Pillow

Ensure Google Chrome and ChromeDriver are installed and available in your PATH.

## Contributing

Contributions to PortScreenShotter are welcome! Feel free to fork the repository, make your changes, and submit a pull request. If you encounter any issues or have suggestions for improvements, please open an issue.
