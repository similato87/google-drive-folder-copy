# Google Drive Folder Copy

This repository contains a script to copy all files and folders from a shared Google Drive folder to your own Google Drive folder using Google Colab and PyDrive2. This allows you to easily make copies of shared content directly in your browser.

## Features

- Recursively copies all files and subfolders from a shared Google Drive folder.
- Ensures that you have a copy of the shared content even if the original owner stops sharing.

## Prerequisites

- A Google account with access to Google Drive.
- Basic knowledge of Google Colab.

## Setup Instructions

### Step 1: Obtain Folder IDs

1. **Shared Folder ID**:
   - Open the shared folder in Google Drive.
   - The URL will look something like this: `https://drive.google.com/drive/folders/SHARED_FOLDER_ID`.
   - Copy the `SHARED_FOLDER_ID` from the URL.

2. **Your Own Folder ID**:
   - Open your destination folder in Google Drive.
   - The URL will look something like this: `https://drive.google.com/drive/folders/MY_OWN_FOLDER_ID`.
   - Copy the `MY_OWN_FOLDER_ID` from the URL.

### Step 2: Check Permissions

- Ensure you have read access to the shared folder.
- Ensure you have write access to your own destination folder.

### Step 3: Run the Script

1. Open [Google Colab](https://colab.research.google.com/) and create a new notebook.
2. Copy the contents of `copy_drive_folder.py` into a cell in the notebook.
3. Replace `SHARED_FOLDER_ID` and `MY_OWN_FOLDER_ID` with the IDs obtained in Step 1.
4. Run the cell to execute the script.

## Time Estimates

- **Obtain Folder IDs**: 2-5 minutes
- **Check Permissions**: 2-5 minutes
- **Run the Script**: 10-30 minutes (depending on the size of the folder and internet speed)

## Script

The script is located in the file `copy_drive_folder.py`.

### Usage

1. **Copy**: Copy the script into a new cell in a Google Colab notebook.
2. **Edit**: Replace the placeholder folder IDs with your actual folder IDs.
3. **Execute**: Run the cell to start copying files and folders.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
