# DriveRevert
This script rolls back the revision of all files given a specific folder in Google Drive using Pyhton

First step: https://developers.google.com/drive/api/quickstart/python

After you saved the credentials.json in the root folder, run "python revert.py"

## Briefing
At the end of 2022, one of my servers was attacked by a Ransomware, sadly a lot of files were lost and a lot more were uploaded to the Google Drive server. In order to revert all the files uploaded to Google Drive to a date before the attacked, I had to create the following script.

The ramsonware changed the extension of the files to (.lockfiles) so the script will search that extension to find all damaged files.

It then check if the date of the las revision matches the day of the attack, and if it is, deletes the affected revision.

After the deletion of the affected revision, the file is renamed by removing the extension.

## Final
This is not an opimized script, but it is great to revert the most files you have access to if you faced a ransomware attack

Feel free to suggest changes!


