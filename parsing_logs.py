import os
import shutil

# Path to the directory where logs are stored
log_dir = "/var/log/myapp"

# Path to the directory where old logs will be moved
archive_dir = "/var/archive/myapp"

# Check if the archive directory exists, create if not
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

# List all files in the log directory
for filename in os.listdir(log_dir):
    if filename.endswith(".log"):  # Check for log files
        file_path = os.path.join(log_dir, filename)
        archive_path = os.path.join(archive_dir, filename)

        # Move the log file to the archive directory
        shutil.move(file_path, archive_path)
        print(f"Archived {filename}")
