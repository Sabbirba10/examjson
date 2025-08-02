# Exam JSON

This project Exam JSON is also called PDF to JSON Converter for BRACU Exam Schedule which provides a utility for converting PDF files containing examination schedules into JSON format. The main functionality is implemented in the `src/convert.py` file, which processes PDF tables and extracts relevant data.

## Features

- Extracts course information, section numbers, examination dates, start and end times, room assignments, and department details from PDF files.
- Standardizes date and time formats to ensure consistency in the output JSON.
- Validates entries to ensure that only complete and relevant data is included in the final output.

## Requirements

To run this project, you need to install the following dependencies:

- `pdfplumber`: A library for extracting information from PDF files.

You can install the required dependencies by running:

```
pip install -r requirements.txt
```

## Usage

To convert a PDF file to JSON format, use the following command:

```
python3 src/convert.py input.pdf output.json
```

Replace `input.pdf` with the path to your PDF file and `output.json` with the desired path for the output JSON file.

## Example

Given a PDF file named `schedule.pdf`, you can convert it to JSON by executing:

```
python3 src/convert.py input.pdf output.json
```

This will generate a `schedule.json` file containing the extracted examination schedule data.

## Usage with convert2.py

To use the enhanced converter script (`convert2.py`), run:

```
python3 src/convert2.py input.pdf output.json
```

Replace `input.pdf` with your PDF file and `output.json` with your desired output file name.

This script extracts additional metadata, such as page number, line number, row text, and bounding box coordinates for each entry.

## Usage with convert3.py (Manual Course Code Entry)

The `convert3.py` script allows you to convert a PDF exam schedule to JSON and **manually specify the course code** for all entries. This is useful for PDFs containing a single course.

### How to Use

1. Open a terminal and navigate to your project directory.
2. Run the script with:

   ```
   python3 src/convert3.py input.pdf output.json
   ```

   Replace `input.pdf` with the path to your PDF file and `output.json` with your desired output file name.

3. When prompted, enter the course code (e.g., `ENG101`) and press Enter.

### Example

```
$ python3 src/convert3.py ENG101.pdf ENG101.json
Enter the course code for this PDF: ENG101
Processing ENG101.pdf...
PDF contains 1 pages
Extracted global headers: ['Section', 'Mid Date', 'Start Time', 'End Time', 'Room.', 'Dept.']
Processing page 1...
  Found 1 tables on page 1
    Added entry: Course=ENG101, Section=1
    Added entry: Course=ENG101, Section=2
...
Converted PDF data has been written to ENG101.json
```

All entries in the output JSON will have the course code you provided.

---

**Note:**

- Make sure you have installed the required dependencies (e.g., `pdfplumber`).
- You can install dependencies with:
  ```
  pip3 install - requirements.txt
  ```
