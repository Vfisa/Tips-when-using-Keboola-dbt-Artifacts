from datetime import datetime

CSV_TIMING_FILENAME = os.path.join(endpath, "model_timing.csv")

def process_model_timing(filepath):
    """Processes a single model_timing.json file."""
    with open(filepath, 'r') as file:
        data = json.load(file)
        for entry in data:
          
            # Filename for PK
            entry['filename'] = filename
            
            # Time Difference Calculation
            start_time = datetime.strptime(entry['timeStarted'], '%Y-%m-%dT%H:%M:%S.%fZ')
            end_time = datetime.strptime(entry['timeCompleted'], '%Y-%m-%dT%H:%M:%S.%fZ')
            time_diff = end_time - start_time
            entry['duration'] = time_diff.total_seconds()  # In seconds
            
            yield entry


# Open timing CSV file for writing 
with open(CSV_TIMING_FILENAME, 'w', newline='') as timing_csvfile:

    # Fieldnames and writer for timing CSV
    timing_fieldnames = ['filename', 'id', 'name', 'status', 'thread', 'timeStarted', 'timeCompleted', 'dependsOn', 'duration']
    timing_writer = csv.DictWriter(timing_csvfile, fieldnames=timing_fieldnames)
    timing_writer.writeheader()

    # Process files in the startpath
    for filename in os.listdir(startpath):
        if filename.endswith('model_timing.json'):
            filepath = os.path.join(startpath, filename)
            data = process_model_timing(filepath)
            timing_writer.writerows(data)
            
list_files(endpath)

