# Exam PDF to JSON Converter

This repository contains scripts to extract and convert exam schedules from PDF files into structured JSON format. It is designed for processing university exam schedules, supporting both final and midterm exam formats.

## Directory Structure

```
exam.pdf                # Example input PDF file
pdf.json                # Example output JSON file (pdf)
bil.json                # Example output JSON file (bil)
script/
    bil.py              # Script for extracting midterm exam schedules (BIL department)
    pdf.py              # Script for extracting final exam schedules (general)
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

Use [`script/pdf.py`](script/pdf.py):

```sh
python script/pdf.py exam.pdf output5.json
```

### For BIL Exam Schedules (BIL Department)

Use [`script/bil.py`](script/bil.py):

```sh
python3 script/bil.py exam.pdf pdf.json
```

## Script Execution Example

### Final Exam Script Example

```sh
python3 script/bil.py exam.pdf bil.json
```

- **Input:** `exam.pdf` (Merged exam schedule PDF)
- **Output:** `bil.json` (JSON file with extracted BIL exam schedule)
- **How it works:**  
  The script reads the PDF, extracts tables or lines containing exam information, parses fields like Course, Section, Date, Time, Room, and Department, and writes them as structured JSON. Each exam entry includes metadata such as page and line number.

### Midterm Exam Script Example

```sh
python script/pdf.py exam.pdf pdf.json
```

- **Input:** `exam.pdf` (Exam schedule PDF, General department format)
- **Output:** `pdf.json` (JSON file with extracted general exam schedule)
- **How it works:**  
  This script is tailored for the BIL department's midterm schedule format. It processes the PDF, extracts relevant exam details, and outputs them in the same structured JSON format as the final exam script.

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
