import json
import os
import csv

CSV_FILENAME = os.path.join(endpath, "dbt_log.csv")

def process_dbt_log(filepath):
    """Processes a single dbt.log file."""
    with open(filepath, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                yield data
            except json.JSONDecodeError:
                print(f"Error decoding JSON line in {filepath}: {line}")

"""
def extract_data(log_entries):
    #Extracts relevant data from log entries.
    for entry in log_entries:
        yield {
            'timestamp': entry.get('info', {}).get('ts', ''),
            'level': entry.get('info', {}).get('level', ''),
            'code': entry.get('info', {}).get('code', ''),
            'code_sign': entry.get('info', {}).get('code', '')[0],  # Extract first character
            'message': entry.get('info', {}).get('msg', ''),
            'name': entry.get('info', {}).get('name', ''),
            'thread': entry.get('info', {}).get('thread', ''),
            'invocation_id': entry.get('info', {}).get('invocation_id', ''),
            'elapsed_time': entry.get('data', {}).get('elapsed_time', ''),
            'generated_at': entry.get('data', {}).get('generated_at', ''),
            'conn_name': entry.get('data', {}).get('conn_name', ''), 
            'success': entry.get('data', {}).get('success', ''),        
        }
"""
        
def extract_data(log_entries):
    """Extracts relevant data from log entries."""
    for entry in log_entries:
        data = entry.get('data', {})
        info = entry.get('info', {})
        node_info = data.get('node_info', {})

        yield {
            'timestamp': info.get('ts', ''),
            'level': info.get('level', ''),
            'code': info.get('code', ''),
            'code_sign': info.get('code', '')[0],
            'message': info.get('msg', ''),
            'name': info.get('name', ''),
            'thread': info.get('thread', ''),
            'invocation_id': info.get('invocation_id', ''),
            'node_name': node_info.get('node_name', ''),
            'node_path': node_info.get('node_path', ''),
            'node_started_at': node_info.get('node_started_at', ''),
            'node_finished_at': node_info.get('node_finished_at', ''),
            'resource_type': node_info.get('resource_type', ''),
            'unique_id': node_info.get('unique_id', ''),
            'materialized': node_info.get('materialized', ''),
            'meta': node_info.get('meta', ''),
            'description': data.get('description', ''),
            'index': data.get('index', ''),
            'total': data.get('total', ''),
            'generated_at': data.get('generated_at', ''),
            'elapsed_time': data.get('elapsed_time', ''),
            'conn_name': data.get('conn_name', ''),
            'success': data.get('success', ''),
        }
        
# Create the output directory if it doesn't exist
os.makedirs(endpath, exist_ok=True)

# Open the CSV file for writing
with open(CSV_FILENAME, 'w', newline='') as csvfile:
    fieldnames = ['timestamp',
                  'level',
                  'code',
                  'code_sign',
                  'message',
                  'name',
                  'thread',
                  'invocation_id',
                  'node_name',
                  'node_path',
                  'node_started_at',
                  'node_finished_at',
                  'resource_type',
                  'unique_id',
                  'materialized',
                  'meta',
                  'description',
                  'index',
                  'total',
                  'generated_at',
                  'elapsed_time',
                  'conn_name',
                  'success'
                 ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the CSV header

    # Process each dbt.log file in the input directory
    for filename in os.listdir(startpath):
        if filename.endswith('dbt.log'):
            filepath = os.path.join(startpath, filename)
            log_entries = process_dbt_log(filepath)
            data = extract_data(log_entries)
            writer.writerows(data)

    """
    # Process files in the startpath 
    for filename in os.listdir(startpath):
        filepath = os.path.join(startpath, filename)
        if filename.endswith('dbt.log'):
            log_entries = process_dbt_log(filepath)
            data = extract_data(log_entries)
            writer.writerows(data)
    """

list_files(endpath)
