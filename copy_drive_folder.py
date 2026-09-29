import re
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 1. Authenticate
print("Authenticating...", flush=True)
auth.authenticate_user()
drive_service = build('drive', 'v3')
print("Authentication successful.", flush=True)

# 2. Paste IDs or Full URLs here
SOURCE_INPUT = '1BABM5rOd-UGjECZwhiMaNys1n95lJV1j'
DEST_INPUT   = '1ctUmG7LDU1LL1-Ta07Tk03Cz9BEGF2e0'

def extract_id(drive_input):
    """Extracts alphanumeric ID if a full Google Drive URL was pasted."""
    match = re.search(r'folders/([a-zA-Z0-9_-]+)', drive_input)
    if match:
        return match.group(1)
    match_id = re.search(r'id=([a-zA-Z0-9_-]+)', drive_input)
    if match_id:
        return match_id.group(1)
    return drive_input.strip()

source_id = extract_id(SOURCE_INPUT)
dest_id = extract_id(DEST_INPUT)

# 3. Verify access to both folders
def verify_folder(folder_id, label):
    try:
        folder = drive_service.files().get(
            fileId=folder_id,
            fields='id, name, mimeType',
            supportsAllDrives=True
        ).execute()
        print(f"Verified {label}: '{folder.get('name')}' (ID: {folder_id})", flush=True)
        return True
    except HttpError as e:
        print(f"ERROR: Cannot access {label} (ID: {folder_id}). Check permissions/ID. Error: {e}", flush=True)
        return False

if not (verify_folder(source_id, "Source") and verify_folder(dest_id, "Destination")):
    raise SystemExit("Stopping: Invalid folder access.")

# 4. Copy logic with instant logging
def copy_recursive(src_id, dst_id):
    query = f"'{src_id}' in parents and trashed = false"
    page_token = None
    items = []

    print(f"\nScanning contents of folder ID: {src_id}...", flush=True)
    while True:
        res = drive_service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token,
            pageSize=100,
            includeItemsFromAllDrives=True,
            supportsAllDrives=True
        ).execute()
        items.extend(res.get('files', []))
        page_token = res.get('nextPageToken')
        if not page_token:
            break

    print(f"Found {len(items)} items to process in this folder.", flush=True)

    for item in items:
        name = item['name']
        mime = item['mimeType']
        item_id = item['id']

        if mime == 'application/vnd.google-apps.folder':
            print(f"--> Creating subfolder: {name}...", flush=True)
            new_folder = drive_service.files().create(
                body={'name': name, 'mimeType': mime, 'parents': [dst_id]},
                fields='id',
                supportsAllDrives=True
            ).execute()
            # Recurse
            copy_recursive(item_id, new_folder['id'])
        else:
            print(f"--> Server-side copying: {name}...", end=" ", flush=True)
            try:
                drive_service.files().copy(
                    fileId=item_id,
                    body={'name': name, 'parents': [dst_id]},
                    fields='id',
                    supportsAllDrives=True
                ).execute()
                print("DONE", flush=True)
            except HttpError as err:
                print(f"FAILED ({err})", flush=True)

print("\nStarting copy process...", flush=True)
copy_recursive(source_id, dest_id)
print("\nOperation completed successfully.", flush=True)
