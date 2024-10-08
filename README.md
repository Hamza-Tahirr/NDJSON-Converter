# NDJSON-Converter
 This application converts flat text data files into NDJSON (Newline Delimited JSON) format using predefined column specifications from CSV files. The application reads specification files from the `specs/` directory and data files from the `data/` directory, then writes the output in the `output/` directory. 

# Data File Converter to NDJSON

## Overview

This application converts flat text data files into NDJSON (Newline Delimited JSON) format using predefined column specifications from CSV files. The application reads specification files from the `specs/` directory and data files from the `data/` directory, then writes the output in the `output/` directory.

## Problem Definition

You have two types of files:
1. **Specification Files**: Describe the structure of the data files. These are located in the `specs/` directory and have a `.csv` extension. They specify:
   - Column name
   - Column width (in characters)
   - Data type (STRING, BOOLEAN, INTEGER)
   
2. **Data Files**: Contain the raw data that need to be parsed and converted. These are located in the `data/` directory and have a `.txt` extension. Each data file corresponds to a specification file, which determines how the data should be parsed.

The application processes each data file using its associated specification file and generates an NDJSON file for each data file. Each line in the NDJSON file represents a JSON object.

### Example:
#### Specification file (`specs/testformat1.csv`):
| column name | width | datatype |
|-------------|-------|----------|
| name        | 10    | TEXT     |
| valid       | 1     | BOOLEAN  |
| count       | 3     | INTEGER  |

#### Data file (`data/testformat1_2021-07-06.txt`):
```bash
Diabetes  1  1
Asthma    0-14
Stroke    1122
```

#### Output file (`output/testformat1_2021-07-06.ndjson`):
```bash
{"name": "Diabetes", "valid": true, "count": 1}
{"name": "Asthma", "valid": false, "count": -14}
{"name": "Stroke", "valid": true, "count": 122}
```


## Directory Structure
```bash
NDJSON-Converter/
│
├── data/               # Directory containing data files (.txt)
│   └── testformat1_2021-07-06.txt
│
├── specs/              # Directory containing specification files (.csv)
│   └── testformat1.csv
│
├── output/             # Directory for output NDJSON files (.ndjson)
│   └── (generated files will go here)
│
├               # Directory containing source code
├── converter.py    # Python script with main code logic
│
└── README.md           # Documentation file explaining the project

```

## Setup and Usage

### Prerequisites

- Python 3.12
- Ensure you have imported the required modules:

```bash
import csv
import json
import os
```

## Running the Application

1. Place your specification files in the `specs/` directory.

2. Place your data files in the `data/` directory.

3. Run the converter from the root directory:

   ```bash
     python converter.py
   ```

4. Output files will be generated in the `output/` directory.

## Example Workflow

1. Data File: `data/testformat1_2021-07-06.txt`
2. Specification File: `specs/testformat1.csv`
3. Generated NDJSON: `output/testformat1_2021-07-06.ndjson`

## Error Handling

1. The program handles missing or malformed files gracefully:
   - If the specification file is missing, the program will print an error and skip processing the data file.
   - If the data file is missing, an appropriate error will be logged.
   - Any malformed data line will log an error and skip that line, but the rest of the file will continue processing.

## Code Explanation

`converter.py`

The code processes each data file according to its specification:

1. Specification Parsing: Reads the `specs/` CSV files to get the column definitions (name, width, datatype).
2. Data Parsing: Reads the `data/` text files and slices each line based on the column widths defined in the specification file.
3. Type Conversion: Converts text into JSON-compatible types (`TEXT`, `BOOLEAN`, `INTEGER`).
4. NDJSON Output: Each parsed line from the data file is converted into a JSON object and written as a line in the NDJSON output file.
   
## Main Functions:

1. `read_specification(spec_file)`: Reads and validates the specification file from `specs/`.
2. `parse_line(line, columns)`: Parses a single line of the data file using the specification.
3. `process_data_file(data_file, spec_file)`: Orchestrates reading the data and writing the output.
4. `main()`: Loops through the files in `data/` and processes each file.

## Unit Tests (Discussion)

Although unit tests are not required, here’s an overview of the tests we would add:

1. Test for Specification Parsing:
   Ensure the `read_specification` function correctly parses the CSV and handles missing or incorrect columns.
2. Test for Data Parsing:
   Verify that `parse_line` correctly slices the line, handles different data types (e.g., `TEXT`, `BOOLEAN`, `INTEGER`), and handles errors (such as malformed lines).
3. Test for End-to-End Processing:
   Simulate processing a file pair (data + specification) and ensure the correct `NDJSON` output is generated.
4. Edge Cases:
   Test with files that are too short, have incorrect values (e.g., `BOOLEAN` not being `0` or `1`), or other unexpected issues.

## Extensions and Improvements (Discussion Points)

1. Unit Testing Framework: We could integrate `unittest` or `pytest` for automated testing.
2. Logging: Implement a logging system to log errors into a file for better traceability.
3. CLI Integration: Allow the program to accept custom input/output directories from the command line.
4. Error Handling Improvements: Additional handling for more specific edge cases (e.g., partially corrupt files).
   
## Conclusion

This project demonstrates how to read and process data files based on flexible specifications, converting them to NDJSON format. The approach ensures robustness, handles errors gracefully, and is easy to extend for future requirements.

You can add a `requirements.txt` in the root directory for future purposes.
