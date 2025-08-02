# Exam PDF to JSON Converter

This repository contains scripts to extract and convert exam schedules from PDF files into structured JSON format. It is designed for processing university exam schedules, supporting both final and midterm exam formats.

## Directory Structure

```
exam.pdf                # Example input PDF file
general.json            # Example output JSON file (general)
bil.json                # Example output JSON file (bil)
script/
    bil.py              # Script for extracting midterm exam schedules (BIL department)
    general.py          # Script for extracting final exam schedules (General department)
```

## Requirements

- Python 3.7+
- [pdfplumber](https://github.com/jsvine/pdfplumber)

Install dependencies with:

```sh
pip install pdfplumber
```

## Usage

### For General Exam Schedules

Use [`script/general.py`](script/general.py):

```sh
python script/general.py exam.pdf general.json
```

### For BIL Exam Schedules (BIL Department)

Use [`script/bil.py`](script/bil.py):

```sh
python script/bil.py exam.pdf bil.json
```

## Script Execution Example

### General Exam Script Example

```sh
python script/general.py exam.pdf general.json
```

- **Input:** `exam.pdf` (exam schedule PDF, General department format)
- **Output:** `general.json` (JSON file with extracted general exam schedule)
- **How it works:**  
  The script reads the PDF, extracts tables or lines containing exam information, parses fields like Course, Section, Date, Time, Room, and Department, and writes them as structured JSON. Each exam entry includes metadata such as page and line number.

### BIL Exam Script Example

```sh
python script/bil.py exam.pdf bil.json
```

- **Input:** `exam.pdf` (exam schedule PDF, BIL department format)
- **Output:** `bil.json` (JSON file with extracted BIL exam schedule)
- **How it works:**  
  This script is tailored for the BIL department's exam schedule format. It processes the PDF, extracts relevant exam details, and outputs them in the same structured JSON format as the general exam script.

## Example Output

```json
{
  "metadata": {
    "source": "exam.pdf",
    "generated_at": "2025-08-02T12:00:00",
    "fields": [
      "Course",
      "Section",
      "Date",
      "Time",
      "Room",
      "Department",
      "Page Number",
      "Line Number",
      "RowText",
      "BoundingBox"
    ]
  },
  "exams": [
    {
      "Course": "CSE101",
      "Section": "1",
      "Date": "2025-08-10",
      "Time": "09:00-11:00",
      "Room": "A101",
      "Department": "CSE",
      "Page Number": 2,
      "Line Number": 5,
      "RowText": "CSE101 1 2025-08-10 09:00-11:00 A101 CSE",
      "BoundingBox": [100, 200, 300, 220]
    }
  ]
}
```

## License

MIT License

---

**Note:** This project is intended for academic and administrative use. Ensure you have permission to process and extract data from the provided documents.
