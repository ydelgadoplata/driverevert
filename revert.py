"""
At the end of 2022, one of my servers was attacked by a Ransomware, sadly a lot of files were lost and a lot more upload to the Google Drive server. In order to revert all the files to a date before the attacked, I had to create the following script.

This script execute a Search of all files in a specific folder, given a word that is common for all files and check for all the version of that specific file then, the script delete the version associatted to the day of the modification. After locate and delete the affected version, the script rename the file name, removing the wrong extension.

This is not an opimized script, but is great to revert the most files you have access to if you faced a ransomware attack

Feel free to suggest changes!

"""

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
    Prints the names and ids of the first 100 files in a specific folder the user has access to.
    If the folder has more than 100 files, you must run the script as many times as needed.
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
        #Change the date for the date of your attack
        attack_date = 'Use the date of the attack (AAAA-MM-DD)'
        #Find the correct folder name and paste it on the following line.
        folder_id = '---Pase the Folder ID here---'
        #Extension of all files affected by Ransomware. Please change the extension for the one that correspond to your attacked files
        attack_extension = '.lockfiles'
        # Call the Drive v3 API to search in an specific folder.
        print('Looking for files...')
        results = service.files().list(
            q=f"'{folder_id}' in parents and name contains '{attack_extension}'", 
            fields="nextPageToken, files(id, name)").execute()

        """
        Uncomment the following lines to execute a global search accross all Google Drive
        Be aware of some HttpErrors that could be shown in the console. This errorrs would give you clue of what could happened.    
        """
        #results = service.files().list(
        #    q=f"name contains '*.lockfiles'",
        #    fields="nextPageToken, files(id, name)").execute()    
        
        #Put files in an object to get all fields and metadata info of the request
        items = results.get('files', [])
        total_files = len(items)
        proccesed = total_files

        if not items:
            print('No files found.')
            return
        print('{0} files were found'.format(total_files))
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            try:
                #After requesting the files, this request get all the revisions of each files
                revisions_results = service.revisions().list(fileId=item['id']).execute()
                revisions = revisions_results.get("revisions", [])
                if not revisions:
                    print('No versions found')
                print('Versions found:')
                for n, rev in enumerate(revisions):
                    print(f"{n} {rev['modifiedTime']}")
                    if rev['modifiedTime'].startswith(attack_date):
                        try:
                            print('---')
                            print('Trying to delete the version of the attack...')
                            service.revisions().delete(fileId=item['id'], 
                                revisionId=rev['id']).execute()
                            print(f'Version deteled')
                            print(f'Trying to change the name of the file')
                            new_name = {'name': item['name'].replace(attack_extension, '')}
                            #This request changes the name of the file, by removing the extension of the file
                            service.files().update(
                                fileId=item['id'],
                                body=new_name,
                                fields='name').execute()
                            print(u'OK -> Name changed!')
                            break
                        except HttpError as error:
                            print(f'An error occurred: {error.status_code}, under uri:{error.uri}')      
                print('---')
                if not proccesed == 0:
                    proccesed = proccesed - 1
                    print(u'Still {0} files pending for processing'.format(proccesed))
                    print('---')   
            except HttpError as error:
                print(f'An error occurred: {error}')        
        print('Congrats! this request is done. Try another folder and execute the scipt again!') 
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()