# Install PyDrive2 if not already installed
!pip install pydrive2

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
import os

# Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

# Folder IDs
shared_folder_id = '*********************************'  # Replace with actual shared folder ID
my_own_folder_id = '*********************************'  # Replace with your own folder ID

# Function to list files in a folder
def list_files_in_folder(folder_id):
    try:
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        return file_list
    except Exception as e:
        print(f"Failed to list files in folder with ID: {folder_id}, Error: {e}")
        return []

# Function to recursively copy files and folders
def copy_files_and_folders(source_folder_id, dest_folder_id, files_copied):
    items = list_files_in_folder(source_folder_id)
    for item in items:
        try:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Create the same folder in the destination folder
                new_folder = drive.CreateFile({'title': item['title'], 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': dest_folder_id}]})
                new_folder.Upload()
                print(f"Copied folder: {item['title']}")
                # Recursively copy the contents of the folder
                copy_files_and_folders(item['id'], new_folder['id'], files_copied)
            else:
                # Copy the file
                copied_file = drive.CreateFile({'title': item['title'], 'parents': [{'id': dest_folder_id}], 'mimeType': item['mimeType']})
                item.GetContentFile(item['title'], mimetype=item['mimeType'])
                copied_file.SetContentFile(item['title'])
                copied_file.Upload()
                os.remove(item['title'])  # Clean up the downloaded file
                files_copied.append(item['title'])
                print(f"Copied file: {item['title']}")
        except Exception as e:
            print(f"Failed to copy item: {item['title']}, Error: {e}")

# Track copied files
files_copied = []

# Start copying process
copy_files_and_folders(shared_folder_id, my_own_folder_id, files_copied)

# Report copied files
print("\nCopy Summary:")
print(f"Total files copied: {len(files_copied)}")
for file_name in files_copied:
    print(file_name)
