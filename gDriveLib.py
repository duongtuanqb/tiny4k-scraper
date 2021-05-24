import re
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from os import path



def extractFileId(links):
    links = re.findall(r"\b(?:https?:\/\/)?(?:drive\.google\.com[-_&?=a-zA-Z\/\d]+)",links)  
    fileIDs = [re.search(r"(?<=/d/|id=|rs/).+?(?=/|$)", link)[0] for link in links]
    print(fileIDs)
    return fileIDs

def upload(file_obj,filename,parent):
    file = drive.CreateFile({"title":filename,'parents': [{'id': parent}]})
    file.SetContentFile(file_obj)
    print(f'uploading to: {parent} - title: {filename}')
    file.Upload()
    return file['id']

def create_credential():
    auth_and_save_credential()

def create_drive_manager():
    gAuth = GoogleAuth()
    typeOfAuth = None
    if not path.exists("credentials.txt"):
        typeOfAuth = input("type save if you want to keep a credential file, else type nothing")
    bool = True if typeOfAuth == "save" or path.exists("credentials.txt") else False
    authorize_from_credential(gAuth, bool)
    drive: GoogleDrive = GoogleDrive(gAuth)
    return drive


def authorize_from_credential(gAuth, isSaved):
    if not isSaved:
        auth_no_save(gAuth)
    if isSaved and not path.exists("credentials.txt"):
        create_credential()
        gAuth.LoadCredentialsFile("credentials.txt")
    if isSaved and gAuth.access_token_expired:
        gAuth.LoadCredentialsFile("credentials.txt")
        gAuth.Refresh()
        print("token refreshed!")
        gAuth.SaveCredentialsFile("credentials.txt")
    gAuth.Authorize()
    print("authorized access to google drive API!")


def auth_and_save_credential():
    gAuth = GoogleAuth()
    gAuth.LocalWebserverAuth()
    gAuth.SaveCredentialsFile("credentials.txt")
def auth_no_save(gAuth):
    gAuth.LocalWebserverAuth()

def recursiveSearch(folderID):
    files = []
    folder = drive.ListFile({'q': "'" + folderID + "' in parents"}).GetList()
    for i in folder:
        if(i['mimeType'] == "application/vnd.google-apps.folder"):
            for a in recursiveSearch(drive,i['id']):
                files.append(a)
        else:
            files.append({'title':i["title"],'drive-id':i['id']})
    return(files)

drive = create_drive_manager()