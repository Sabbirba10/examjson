import sys
import json
import re
from datetime import datetime
import pdfplumber

def clean_text(text):
    if text is None:
        return None
    return re.sub(r'\s+', ' ', text).strip()

def standardize_date(date_str):
    if not date_str or not isinstance(date_str, str):
        return date_str
    for fmt in ("%d-%b-%y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str

def extract_times(time_str):
    """Extract start and end times from a string like '11:00AM-12:30AM'"""
    if not time_str or not isinstance(time_str, str):
        return None, None
    # Normalize dashes and remove spaces around them
    time_str = time_str.replace('–', '-').replace('—', '-').replace('−', '-')
    time_str = re.sub(r'\s*-\s*', '-', time_str)
    # Match times like 11:00AM, 12:30PM, etc.
    matches = re.findall(r'(\d{1,2}:\d{2}\s*[APMapm]{2})', time_str)
    if len(matches) >= 2:
        return matches[0].replace(' ', '').upper(), matches[-1].replace(' ', '').upper()
    elif len(matches) == 1:
        return matches[0].replace(' ', '').upper(), ""
    return "", ""

def standardize_time(time_str):
    """Standardize time format to 24-hour (HH:MM)"""
    if not time_str or not isinstance(time_str, str):
        return ""
    time_str = time_str.strip().upper().replace(' ', '')
    for fmt in ("%I:%M%p", "%I:%M %p", "%H:%M"):
        try:
            dt = datetime.strptime(time_str, fmt)
            return dt.strftime("%H:%M")
        except ValueError:
            continue
    return ""

def is_valid_entry(entry):
    required_fields = ["Course", "Section", "Mid Date", "Start Time", "End Time", "Room."]
    return all(field in entry and entry[field] for field in required_fields)

def convert_pdf_to_json(pdf_path, json_path, course_code):
    print(f"Processing {pdf_path}...")

    all_entries = []
    unique_entries = set()
    global_headers = []

    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF contains {len(pdf.pages)} pages")

        first_page = pdf.pages[0]
        tables = first_page.extract_tables()

        # Try to find headers
        if tables and len(tables) > 0 and len(tables[0]) > 0:
            headers = [clean_text(cell) if cell else "" for cell in tables[0][0]]
            trimmed_headers = headers[2:]  # Skip SL and ID, just like data rows
            global_headers = []
            for header in trimmed_headers:
                h = header.lower()
                if "section" in h:
                    global_headers.append("Section")
                elif "mid exam date" in h:
                    global_headers.append("Mid Exam Date")
                elif "exam time" in h:
                    global_headers.append("Exam Time")
                elif "classroom" in h:
                    global_headers.append("Classroom")
                else:
                    global_headers.append(header)
            print(f"Extracted global headers: {global_headers}")
        else:
            print("Warning: Could not extract headers from first page!")
            global_headers = ["Section", "Mid Exam Date", "Exam Time"]

        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num}...")
            tables = page.extract_tables()
            page_text = page.extract_text() or ""
            text_lines = page_text.splitlines()
            words = page.extract_words()
            if tables:
                for table_idx, table in enumerate(tables):
                    if not table:
                        continue
                    start_row = 1 if page_num == 1 else 0
                    for row_idx, row in enumerate(table[start_row:]):
                        if not row or all(cell is None or (isinstance(cell, str) and cell.strip() == "") for cell in row):
                            continue
                        # Skip SL and ID columns
                        trimmed_row = row[2:]  # ['01', '26-Jul-25', '08:30AM-10:00AM', '07A-01C']
                        if len(trimmed_row) < 4:
                            print("Skipping short row:", trimmed_row)
                            continue
                        entry = {
                            "Section": clean_text(trimmed_row[0]),
                            "Mid Exam Date": clean_text(trimmed_row[1]),
                            "Exam Time": clean_text(trimmed_row[2]),
                            "Classroom": clean_text(trimmed_row[3])
                        }
                        minimal_entry = {
                            "Course": course_code,
                            "Section": entry["Section"],
                            "Mid Date": standardize_date(entry["Mid Exam Date"]),
                            "Room.": entry["Classroom"],
                            "Dept.": "BIL"  # <-- Set department here
                        }
                        start, end = extract_times(entry["Exam Time"])
                        minimal_entry["Start Time"] = standardize_time(start)
                        minimal_entry["End Time"] = standardize_time(end)

                        # RowText: full concatenated row as in PDF
                        row_text = ' '.join([clean_text(str(cell)) for cell in row if cell])
                        minimal_entry["RowText"] = row_text

                        # Page Number
                        minimal_entry["Page Number"] = page_num

                        # Line Number: find first matching line in PDF text
                        line_number_in_pdf = -1
                        for idx, line in enumerate(text_lines, 1):
                            if minimal_entry["Section"] and minimal_entry["Room."]:
                                if minimal_entry["Section"] in line and minimal_entry["Room."] in line:
                                    line_number_in_pdf = idx
                                    break
                        minimal_entry["Line Number"] = line_number_in_pdf

                        # BoundingBox: try to find the section in the words
                        bounding_box = None
                        try:
                            section_text = minimal_entry["Section"]
                            matches = [w for w in words if clean_text(w.get('text', '')) == section_text]
                            if matches:
                                w = matches[0]
                                # Use standard x0/x1, actual y0/y1 from word
                                bounding_box = {
                                    "x0": 89.664,
                                    "y0": float(w['top']),
                                    "x1": 506.663,
                                    "y1": float(w['bottom'])
                                }
                            else:
                                # Fallback: estimate based on row index
                                base_y = 100 + (row_idx * 15)
                                bounding_box = {
                                    "x0": 90.0,
                                    "y0": base_y,
                                    "x1": 500.0,
                                    "y1": base_y + 10
                                }
                        except Exception as e:
                            base_y = 100 + (row_idx * 15)
                            bounding_box = {
                                "x0": 90.0,
                                "y0": base_y,
                                "x1": 500.0,
                                "y1": base_y + 10,
                                "error": str(e)
                            }
                        minimal_entry["BoundingBox"] = bounding_box

                        unique_key = (
                            minimal_entry.get("Course", ""),
                            minimal_entry.get("Section", ""),
                            minimal_entry.get("Mid Date", ""),
                            minimal_entry.get("Start Time", ""),
                            minimal_entry.get("End Time", ""),
                            minimal_entry.get("Room.", "")
                        )
                        if is_valid_entry(minimal_entry) and unique_key not in unique_entries:
                            all_entries.append(minimal_entry)
                            unique_entries.add(unique_key)
                            print(f"    Added entry: {minimal_entry}")
                        elif not is_valid_entry(minimal_entry):
                            print(f"    Skipping invalid entry: {minimal_entry}")
                        else:
                            print(f"    Skipping duplicate entry: {minimal_entry}")
            else:
                print(f"  No tables found on page {page_num}")

    print(f"Total valid entries extracted: {len(all_entries)}")

    output = {
        "metadata": {
            "source": pdf_path,
            "generated_at": datetime.now().isoformat(),
            "total_entries": len(all_entries),
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
        "exams": all_entries
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Converted PDF data has been written to {json_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 src/convert4.py input.pdf output.json")
        sys.exit(1)
    pdf_path = sys.argv[1]
    json_path = sys.argv[2]
    course_code = input("Enter the course code for this PDF: ").strip()
    convert_pdf_to_json(pdf_path, json_path, course_code)