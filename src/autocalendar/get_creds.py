from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import os

import subprocess

SCOPES = ["https://www.googleapis.com/auth/calendar.events.owned"]

def write_token_creds():
    """Get Google Calendar credentials for the application."""
   
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials=os.path.join(script_dir, "credentials.json")
    token_path = os.path.join(script_dir, "token.json")
    print(f"Using credentials from: {credentials}")
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        return
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials, SCOPES
        )
        creds = flow.run_local_server(host='localhost',
            port=0, 
            authorization_prompt_message='Please visit this URL: {url}', 
            success_message='The auth flow is complete; you may close this window.',
            open_browser=True
        )#port=0
        subprocess.run(['start http://localhost:0/'], shell=True)
        
      # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())  
    print("Credentials loaded successfully.")
    
if __name__ == "__main__":
    write_token_creds()
    print("Token credentials written to token.json.")