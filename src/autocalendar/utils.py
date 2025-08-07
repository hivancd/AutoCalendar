
import winreg
import win32security
from os.path import expandvars


def username_to_sid(username):
    sid, domain, type = win32security.LookupAccountName(None, username)
    return win32security.ConvertSidToStringSid(sid)

def get_downloads_path(user):
    """
    Get the Downloads folder path for a given Windows user.
    
    Args:
        user (str): The username of the Windows user.
        
    Returns:
        str: The full path to the Downloads folder for the specified user.
    """
    # Convert username to SID
    sid = username_to_sid(user)  
    sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
    key = winreg.OpenKey(
            winreg.HKEY_USERS,
            rf"{sid}\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        )
    downloads, _ = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")
    winreg.CloseKey(key)

    return expandvars(downloads)

if __name__ == "__main__":
    user = "hian"  # Replace with the actual username
    downloads_path = get_downloads_path(user)
    print(f"Downloads path for user '{user}': {downloads_path}")