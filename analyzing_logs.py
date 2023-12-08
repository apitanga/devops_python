# Example of a script for parsing log files

# Define the log file's path
log_file_path = '/var/log/myapp.log'

# Open the log file
with open(log_file_path, 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Check if the line contains an error message
        if 'ERROR' in line:
            # Extract the timestamp (assuming it's at the start of the line)
            timestamp = line.split(' ')[0]
            print(f"Error found at {timestamp}: {line.strip()}")
