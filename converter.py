import csv
import json
import os

# Define directories
SPEC_DIR = 'specs/'
DATA_DIR = 'data/'
OUTPUT_DIR = 'output/'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def read_specification(spec_file):
    """Reads a specification CSV file and returns a list of column definitions."""
    spec_path = os.path.join(SPEC_DIR, spec_file)
    
    if not os.path.exists(spec_path):
        raise FileNotFoundError(f"Specification file not found: {spec_file}")
    
    columns = []
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Validate that the specification has the required columns
        required_columns = ['column name', 'width', 'datatype']
        if reader.fieldnames != required_columns:
            raise ValueError(f"Specification file {spec_file} is incorrectly formatted.")
        
        for row in reader:
            try:
                column_name = row['column name']
                width = int(row['width'])
                datatype = row['datatype'].upper()
                
                if datatype not in ['TEXT', 'BOOLEAN', 'INTEGER']:
                    raise ValueError(f"Invalid datatype '{datatype}' in {spec_file}")
                
                columns.append({
                    'name': column_name,
                    'width': width,
                    'datatype': datatype
                })
            except KeyError as e:
                raise ValueError(f"Missing expected column in spec file {spec_file}: {str(e)}")
            except ValueError as e:
                raise ValueError(f"Error processing specification file {spec_file}: {str(e)}")
    
    return columns

def parse_line(line, columns):
    """Parses a single line of a data file using the column definitions from the specification."""
    parsed_data = {}
    start = 0
    
    for column in columns:
        end = start + column['width']
        raw_value = line[start:end].strip()  # Trim any extra whitespace
        start = end
        
        # Ensure the line has enough characters for the column
        if len(raw_value) == 0:
            raise ValueError(f"Line is too short to extract column '{column['name']}'")
        
        # Convert the value based on the datatype
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
    
    output_path = os.path.join(OUTPUT_DIR, data_file.replace('.txt', '.ndjson'))
    
    # Read specification file
    try:
        columns = read_specification(spec_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading specification: {str(e)}")
        return
    
    # Process each line of the data file
    try:
        with open(data_path, 'r', encoding='utf-8') as data_f, open(output_path, 'w', encoding='utf-8') as output_f:
            for line_num, line in enumerate(data_f, start=1):
                try:
                    parsed_data = parse_line(line, columns)
                    output_f.write(json.dumps(parsed_data) + '\n')
                except ValueError as e:
                    print(f"Error processing line {line_num} of {data_file}: {str(e)}")
    except Exception as e:
        print(f"Error processing data file {data_file}: {str(e)}")

def main():
    # Loop through all files in the data directory
    for data_file in os.listdir(DATA_DIR):
        if data_file.endswith('.txt'):
            # Extract the specification file name from the data file
            spec_file = data_file.split('_')[0] + '.csv'
            
            # Process the data file using the corresponding specification
            try:
                process_data_file(data_file, spec_file)
            except (FileNotFoundError, ValueError) as e:
                print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
