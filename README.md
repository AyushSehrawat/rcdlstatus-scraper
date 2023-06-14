# DL Details Automation

Python script to automate the process of getting the RC DL Status from parivahan.gov.in website using web scraping.

## Installation

```python
pip install -r requirements.txt
```

In addition to the above, you need to install Tessaract OCR on your system. You can download it from [here](https://tesseract-ocr.github.io/tessdoc/Installation.html).

For Windows, you can download the installer from [here](https://github.com/UB-Mannheim/tesseract/wiki). If this doesn't work, checkout [here](https://tesseract-ocr.github.io/tessdoc/Downloads.html)

## Running the script

```
python ./src/main.py
```

Edit the variables here,

```python
if __name__ == "__main__":
    dl_no = "MH03-20080022135"
    dl_dob = "01-12-1987"
    ...
```

This code can also be used with db/csv files to scrape data in bulk.