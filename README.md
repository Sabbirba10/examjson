# Exam JSON Converter

This project provides Python scripts to extract structured exam schedule data from PDF files and convert it into JSON format. It is designed to handle university exam schedules, capturing detailed metadata and row-level information from tabular PDF documents.

---

## Scripts Overview

### 1. `script/convert2.py`

**Purpose:**  
Extracts exam schedule tables from a PDF and converts them to JSON, including metadata and row-level details.

**Key Features:**

- Manual input for course code.
- Extracts fields like Course, Section, Date, Time, Room, Department, Page Number, Line Number, RowText, and BoundingBox.
- Skips adding `"Course"` to `fields_description` if any course code value is longer than 7 characters.

**Usage:**

```bash
python3 script/convert2.py input.pdf output.json
```

You will be prompted to enter the course code.

---

### 2. `script/convert3.py`

**Purpose:**  
Similar to `convert2.py`, but may include different field mappings or department logic.

**Key Features:**

- Manual course code input.
- Extracts and standardizes exam schedule data.
- Includes all metadata fields in the output.

**Usage:**

```bash
python3 script/convert3.py input.pdf output.json
```

---

### 3. `script/convert4.py`

**Purpose:**  
Enhanced version with improved deduplication and validation.

**Key Features:**

- Manual course code input.
- Deduplicates entries based on key fields.
- Skips `"Course"` in `fields_description` if any course code is longer than 7 characters.
- Prints added/skipped entries for transparency.

**Usage:**

```bash
python3 script/convert4.py input.pdf output.json
```

---

### 4. `script/convert5.py`

**Purpose:**  
Fully automated course code detection and per-page course code assignment.

**Key Features:**

- Scans every page for `SCHEDULE : <COURSECODE>` and assigns the detected course code to each page's entries.
- If no course code is found on a page, uses the last detected code.
- No manual input required unless no course code is found in the entire PDF.
- Handles duplicate course codes (does not skip them).

**Usage:**

```bash
python3 script/convert5.py input.pdf output.json
```

---

## Output Structure

- **metadata**: Information about the source PDF, generation time, and field descriptions.
- **exams**: List of extracted exam schedule entries, each with fields such as Course, Section, Date, Time, Room, Department, Page Number, Line Number, RowText, and BoundingBox.

---

## Example Output

```json
{
  "metadata": {
    "source": "exam.pdf",
    "generated_at": "2025-08-02T18:56:47.636293",
    "total_entries": 153,
    "fields_description": {
      "Course": "Course code",
      "Section": "Class section number",
      "Mid Date": "Examination date (YYYY-MM-DD)",
      "Start Time": "Exam start time (24-hour format, first in range)",
      "End Time": "Exam end time (24-hour format, last in range)",
      "Room.": "Examination room (Classroom)",
      "Dept.": "Department offering the course",
      "Page Number": "Page number from which the entry was extracted",
      "Line Number": "Line number from which the entry was extracted",
      "RowText": "Full concatenated text of the row as it appears in the PDF",
      "BoundingBox": "Coordinates of the row in the PDF (x0, y0, x1, y1)"
    }
  },
  "exams": [
    {
      "Course": "ENG101",
      "Section": "01",
      "Mid Date": "2025-07-26",
      "Start Time": "11:00",
      "End Time": "12:30",
      "Room.": "07A-01C",
      "Dept.": "ENG",
      "Page Number": 1,
      "Line Number": 5,
      "RowText": "01 26-Jul-25 11:00AM-12:30AM 07A-01C",
      "BoundingBox": {
        "x0": 89.664,
        "y0": 123.45,
        "x1": 506.663,
        "y1": 135.67
      }
    }
    // ...
  ]
}
```

---

## Requirements

- Python 3.7+
- Install dependencies:
  ```bash
  pip install pdfplumber
  ```

---

## Customization

- You can adjust the field filtering logic, department codes, or table parsing as needed in the `script/convert*.py` scripts.
- The scripts are modular and can be extended for other PDF table extraction tasks.

---

## License

This project is provided for educational and research purposes.
