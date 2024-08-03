# copy_drive_folder.py

# Install PyDrive2
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

# IDs of the shared folder and your own destination folder (replace with the actual folder IDs)
shared_folder_id = 'SHARED_FOLDER_ID'  # Replace with the actual shared folder ID
my_own_folder_id = 'MY_OWN_FOLDER_ID'  # Replace with your own folder ID

# Function to list files in a folder
def list_files_in_folder(folder_id):
    try:
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        return file_list
    except Exception as e:
        print(f"Failed to list files in folder with ID: {folder_id}, Error: {e}")
        return []

# Function to recursively copy files and folders
def copy_files_and_folders(source_folder_id, dest_folder_id):
    items = list_files_in_folder(source_folder_id)
    for item in items:
        try:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Create the same folder in the destination folder
                new_folder = drive.CreateFile({'title': item['title'], 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': dest_folder_id}]})
                new_folder.Upload()
                print(f"Copied folder: {item['title']}")
                # Recursively copy the contents of the folder
                copy_files_and_folders(item['id'], new_folder['id'])
            else:
                # Copy the file
                copied_file = drive.CreateFile({'title': item['title'], 'parents': [{'id': dest_folder_id}], 'mimeType': item['mimeType']})
                item.GetContentFile(item['title'])
                copied_file.SetContentFile(item['title'])
                copied_file.Upload()
                os.remove(item['title'])  # Clean up the downloaded file
                print(f"Copied file: {item['title']}")
        except Exception as e:
            print(f"Failed to copy item: {item['title']}, Error: {e}")

# Copy all files and folders from the shared folder to your own folder
copy_files_and_folders(shared_folder_id, my_own_folder_id)
