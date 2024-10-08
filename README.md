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
