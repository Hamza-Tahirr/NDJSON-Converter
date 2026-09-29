import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(BASE_DIR, 'specs')
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

DATATYPES = ('TEXT', 'BOOLEAN', 'INTEGER')


def read_specification(spec_file):
    """Reads a specification CSV file and returns a list of column definitions."""
    spec_path = os.path.join(SPEC_DIR, spec_file)

    if not os.path.exists(spec_path):
        raise FileNotFoundError(f"Specification file not found: {spec_file}")

    columns = []

    # utf-8-sig so that specs saved from Excel (with a BOM) still match the header
    with open(spec_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)

        required_columns = ['column name', 'width', 'datatype']
        if reader.fieldnames != required_columns:
            raise ValueError(f"Specification file {spec_file} is incorrectly formatted.")

        for row in reader:
            if None in row.values():
                raise ValueError(f"Incomplete row in specification file {spec_file}: {row}")

            column_name = row['column name'].strip()
            datatype = row['datatype'].strip().upper()

            try:
                width = int(row['width'])
            except ValueError:
                width = 0
            if width <= 0:
                raise ValueError(f"Invalid width '{row['width']}' for column '{column_name}' in {spec_file}")

            if datatype not in DATATYPES:
                raise ValueError(f"Invalid datatype '{datatype}' in {spec_file}")

            columns.append({
                'name': column_name,
                'width': width,
                'datatype': datatype
            })

    return columns


def parse_line(line, columns):
    """Parses a single line of a data file using the column definitions from the specification."""
    parsed_data = {}
    start = 0

    for column in columns:
        end = start + column['width']
        field = line[start:end]
        start = end

        if not field:
            raise ValueError(f"Line is too short to extract column '{column['name']}'")

        raw_value = field.strip()

        try:
            if column['datatype'] == 'TEXT':
                parsed_value = raw_value
            elif column['datatype'] == 'BOOLEAN':
                if raw_value not in ['0', '1']:
                    raise ValueError(f"Invalid BOOLEAN value '{raw_value}'")
                parsed_value = raw_value == '1'
            elif column['datatype'] == 'INTEGER':
                parsed_value = int(raw_value)
            else:
                raise ValueError(f"Unknown datatype: {column['datatype']}")
        except ValueError as e:
            raise ValueError(f"Error parsing column '{column['name']}': {str(e)}")

        parsed_data[column['name']] = parsed_value

    return parsed_data


def process_data_file(data_file, spec_file):
    """Processes a single data file using the corresponding specification file."""
    data_path = os.path.join(DATA_DIR, data_file)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    output_name = os.path.splitext(data_file)[0] + '.ndjson'
    output_path = os.path.join(OUTPUT_DIR, output_name)

    try:
        columns = read_specification(spec_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading specification: {str(e)}")
        return

    try:
        with open(data_path, 'r', encoding='utf-8') as data_f, open(output_path, 'w', encoding='utf-8', newline='\n') as output_f:
            for line_num, line in enumerate(data_f, start=1):
                line = line.rstrip('\r\n')
                if not line:
                    continue
                try:
                    parsed_data = parse_line(line, columns)
                    output_f.write(json.dumps(parsed_data) + '\n')
                except ValueError as e:
                    print(f"Error processing line {line_num} of {data_file}: {str(e)}")
    except Exception as e:
        print(f"Error processing data file {data_file}: {str(e)}")


def main():
    if not os.path.isdir(DATA_DIR):
        print(f"Data directory not found: {DATA_DIR}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for data_file in sorted(os.listdir(DATA_DIR)):
        if data_file.endswith('.txt'):
            # testformat1_2021-07-06.txt -> specs/testformat1.csv
            spec_file = data_file.split('_')[0] + '.csv'

            try:
                process_data_file(data_file, spec_file)
            except (FileNotFoundError, ValueError) as e:
                print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
