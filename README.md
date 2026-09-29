# NDJSON Converter

A small Python command-line tool that converts fixed-width text files into NDJSON (newline-delimited JSON). A CSV spec for each file format gives the name, width and data type of every column. The tool uses it to slice each line into typed fields and writes one JSON object per line.

## Features

- Parses fixed-width text files column by column, using a CSV specification
- Converts values to JSON types: `TEXT` to string, `BOOLEAN` (`0`/`1`) to `true`/`false`, `INTEGER` to number (negative values supported)
- Matches each data file to its spec by file name, so several formats can be processed in one run
- Checks the spec file (header, widths, data types) before processing starts
- Reports bad lines with their line number and continues with the rest of the file
- Skips a data file if its spec is missing or invalid, and ignores empty lines

## Tech stack

- Python 3 (standard library only: `csv`, `json`, `os`)

## Project structure

```
NDJSON-Converter/
├── converter.py        # the converter
├── specs/              # format specifications (.csv)
│   └── testformat1.csv
├── data/               # input files (.txt)
│   └── testformat1_2021-07-06.txt
└── output/             # converted files (.ndjson)
    └── testformat1_2021-07-06.ndjson
```

## How it works

Each data file in `data/` is named `<format>_<anything>.txt`. The part before the first underscore selects the spec file `specs/<format>.csv`. The result is written to `output/` with the same base name and a `.ndjson` extension.

A spec file must have exactly this header:

```
column name,width,datatype
```

Every following row describes one column, in the order the columns appear in the line. Values are trimmed of surrounding spaces before conversion.

### Example

`specs/testformat1.csv`

```
column name,width,datatype
name,10,TEXT
valid,1,BOOLEAN
count,3,INTEGER
```

`data/testformat1_2021-07-06.txt`

```
Diabetes  1  1
Asthma    0-14
Stroke    1122
```

`output/testformat1_2021-07-06.ndjson`

```
{"name": "Diabetes", "valid": true, "count": 1}
{"name": "Asthma", "valid": false, "count": -14}
{"name": "Stroke", "valid": true, "count": 122}
```

In the first line, `name` is the first 10 characters (`Diabetes  `), `valid` is the next character (`1`) and `count` is the last 3 characters (`  1`).

## Setup and usage

Requirements: Python 3.8 or newer. There are no third-party packages to install.

```bash
git clone https://github.com/Hamza-Tahirr/NDJSON-Converter.git
cd NDJSON-Converter
python converter.py
```

To convert your own files:

1. Add a spec file to `specs/`, for example `specs/myformat.csv`.
2. Add one or more data files to `data/`, for example `data/myformat_2024-01-01.txt`.
3. Run `python converter.py`. The converted files appear in `output/`.

The `specs/`, `data/` and `output/` folders are found relative to `converter.py`, so the script can be run from any directory. Existing output files with the same name are overwritten.

## Error handling

- Missing spec file, or a spec with a wrong header, an incomplete row, an invalid width or an unknown data type: the error is printed and that data file is skipped.
- A line that ends before one of its columns starts, has a `BOOLEAN` value other than `0`/`1`, or has an `INTEGER` field that is not a number: the error is printed with the line number, the line is skipped, and processing continues.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
