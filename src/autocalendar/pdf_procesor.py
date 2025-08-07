from pypdf import PdfReader

import os
import os.path
from datetime import datetime, date

from pydantic import BaseModel
from pydantic_ai import Agent, ToolOutput 
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def read_pdf(file_path):
    """Read a PDF file and return its text content."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

class Payment(BaseModel):
    document_name: str = ""
    document_date: str
    sender: str
    is_payment: bool 
    payment_amount: str  
    """The ammount of the payment, if it is a tasa, it should be the exact amount."""
    due_date: date  
    '''Only the exact day of the due date of the payment, if it is relative take the date of the document as reference, don't include nothing but the date in RFC3339 format in this answer.'''
    payment_method: str  
    payment_reason: str
    
    
    def payment_to_event(self):
        """Convert the payment information to a calendar event format."""
            
        event={"summary": f"{self.payment_reason}" if self.payment_reason else "Payment Event",
        "description": f"{self.payment_amount} FORMA DE PAGO: {self.payment_method} RAZÓN: {self.payment_reason} DOCUMENTO: {self.document_name} FECHA DEL DOCUMENTO: {self.document_date} ENVIADO POR: {self.sender}",
        "start": {
            "date": f"{self.due_date}",
        },
        "end": {
            "date": f"{self.due_date}",
        }}
        return event

SCOPES = ["https://www.googleapis.com/auth/calendar.events.owned"]


def mark_calendar(file_path, api_key, token_path="token.json"):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    
    # First, loading the model and extracting the payment information    
    # Loading the AI model
    # Create an agent to extract payment information
    try:
        agent = Agent(  
        'openai:gpt-4.1',
        system_prompt='''You are a helpful assistant that extracts information from PDF documents and provides concise and exact answers. 
        for the following PDF document, you are going to analyze every page and in each page you will look for the following information:
        1. The date of the document.
        2. The sender of the document.
        3. If the document refers to a payment or not.
        4. If the document refers to a payment, you should provide:
        1. The payment amount or "tasa"
        2. Only the exact day of the due date of the payment, if it is relative take the date of the document as reference, don't include nothing but the date in RFC3339 format in this answer.
        3. The payment method if available 
        4. A very short reason for the payment
        If you don't find any of the information, you should return "Not found" for that specific information.
        If the document does not mention any of the information at all, you should return "None".
        Translate the information to Spanish if it is in another language.
        ''',  
        output_type=ToolOutput(Payment),
        )
    
        # Run the agent to extract information
        print(f"Processing file: {file_path}")
        text = read_pdf(file_path)
        print(f"Extracted text from PDF: {text[:10]}...")  # Print the first 500 characters of the text for debugging
        # print(agent.capture_run_messages())
        # print(api_key)
        result = agent.run_sync(text)
        # print(f"Extracted result: {result.output.document_name}")
        payment = result.output
        # print(payment.payment_to_event())
        
    except HttpError as error:
        return(f"An error occurred: {error}")
        
    
    if payment.is_payment is False:
        return("The document does not refer to a payment.")
        
    # Next, we mark the date in the calendar:
    # Credentials for the Google Calendar API
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials=os.path.join(script_dir, "credentials.json")
    print(f"Using credentials from: {credentials}")
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
      # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())  
    print("Credentials loaded successfully.")
    # Create the event from the extracted information    
    service = build("calendar", "v3", credentials=creds)
    print(f"Creating event for payment: {payment.payment_reason} on {payment.due_date}")
    event = service.events().insert(calendarId="primary", body=payment.payment_to_event()).execute()
    return(f"Event created: {event.get('htmlLink')}")


if __name__ == "__main__":
    # Example usage
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Comunicación de inicio.pdf")  # Replace with your PDF file path
    mark_calendar(file_path)