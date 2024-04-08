import json
import os
import csv

CSV_FILENAME = os.path.join(endpath, "test_log.csv")

def process_artifact_file(filepath):
    """Extracts run_results.json from an artifacts tarfile and processes it."""
    with tarfile.open(filepath) as tar:
        for member in tar.getmembers():
            if member.name.endswith('dbt test/run_results.json'):  # Find run_results.json
                f = tar.extractfile(member)
                if f:  # Ensure file was extracted
                    data = json.load(f)
                    yield from process_run_results(data)  # We'll define this next


def process_run_results(data):
    """Processes data from the run_results.json file, extracting all timing sections."""

    for result in data['results']:
        # Create a base dictionary for this result
        result_data = {
            'dbt_version': data['metadata']['dbt_version'],
            'generated_at': data['metadata']['generated_at'],
            'invocation_id': data['metadata']['invocation_id'],
            'status': result['status'],
            'thread_id': result['thread_id'],
            'execution_time': result['execution_time'],
            'failures': result['failures'],
            'unique_id': result['unique_id'],
            'message': result['message'],
            'elapsed_time': data['elapsed_time'],
        }

        # Process timing entries
        for timing in result['timing']:
            timing_name = timing['name']
            result_data[timing_name] = timing.get('started_at') 
            result_data[timing_name + '_started_at'] = timing.get('started_at')  
            result_data[timing_name + '_completed_at'] = timing.get('completed_at') 

        yield result_data


        
# Create the output directory if it doesn't exist
os.makedirs(endpath, exist_ok=True)

# Open the CSV file for writing
with open(CSV_FILENAME, 'w', newline='') as csvfile:
    fieldnames = ['dbt_version',
                  'generated_at',
                  'invocation_id',
                  'status',
                  'thread_id',
                  'execution_time',
                  'failures',
                  'unique_id',
                  'message',
                  'elapsed_time',
                  'timing_name',
                  'compile_completed_at',
                  'compile',
                  'execute_completed_at',
                  'execute',
                  'execute_started_at',
                  'compile_started_at'
                 ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the CSV header


		# Process archive files in the startpath
    for filename in os.listdir(startpath):
        if filename.endswith('artifacts.tar.gz'): # Assuming your artifact files are named accordingly
            filepath = os.path.join(startpath, filename)
            data = process_artifact_file(filepath)
            writer.writerows(data)


list_files(endpath)
