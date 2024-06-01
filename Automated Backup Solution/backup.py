import os
import shutil
import subprocess
from datetime import datetime

# Function to perform backup
def backup(source_dir, destination):
    try:
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"backup_{timestamp}.zip"

        # Zip the source directory
        shutil.make_archive(backup_filename, 'zip', source_dir)

        # Move the zip file to the destination
        shutil.move(backup_filename + '.zip', destination)

        return True, f"Backup successful. File '{backup_filename}.zip' created."
    except Exception as e:
        return False, f"Backup failed: {str(e)}"

# Function to upload backup to cloud storage (e.g., AWS S3)
def upload_to_s3(source_file, bucket_name):
    try:
        subprocess.run(["aws", "s3", "cp", source_file, f"s3://{bucket_name}/"])
        return True, "Upload to S3 successful."
    except Exception as e:
        return False, f"Upload to S3 failed: {str(e)}"

# Directory to backup
source_directory = "/path/to/source/directory"

# Remote server details
remote_server = "user@remote.server.com:/path/to/remote/backup/directory"

# Cloud storage details (if applicable)
s3_bucket_name = "your-s3-bucket-name"

# Perform backup
success, message = backup(source_directory, remote_server)

# Upload to cloud storage (if backup was successful)
if success:
    source_file = os.path.join(os.getcwd(), message.split("'")[1])
    success_s3, message_s3 = upload_to_s3(source_file, s3_bucket_name)
    if success_s3:
        message += "\n" + message_s3
    else:
        message += "\nUpload to S3 failed. " + message_s3

# Print backup status
print(message)
