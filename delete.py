#This script makes a global search accross all Google Drive and deletes all files that have a specific keyword

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.metadata', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.appdata']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 100 files the user has access to.
    After finish the first files, you must run the script again.
    """
    creds = None
    results = None
    items = None
    revisions = None
    revisions_results = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        #Write the name of the file you want to delete
        to_search = 'write_the_name_of_file.extension'
        # Call the Drive v3 API
        print('Looking for files...')
        results = service.files().list(
            q=f"name contains '{to_search}'",
            fields="nextPageToken, files(id, name)").execute()    
        items = results.get('files', [])
        total_files = len(items)
        proccessed = total_files

        if not items:
            print('No files found.')
            return
        print('{0} files found'.format(total_files))
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            try:
                service.files().delete(fileId=item['id']).execute()
                print('File deleted')   
                print('---')
                if not proccessed == 0:
                    proccessed = proccessed - 1
                    print(u'{0} files left for processing'.format(proccessed))
                    print('---')   
            except HttpError as error:
                print(f'An error occurred: {error}')        
        print('Congrats, the script has finished. Change the name of the file and execute again!') 
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()