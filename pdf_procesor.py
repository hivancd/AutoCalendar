from pypdf import PdfReader

import os
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

reader = PdfReader("Comunicación de inicio.pdf")
    
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

model= OpenAIModel(
    'gpt-4o',
    provider=OpenAIProvider(api_key=api_key),
)

agent = Agent(  
    'openai:gpt-4o',
    system_prompt='''You are a helpful assistant that extracts information from PDF documents and provides concise and exact answers. 
    for the following PDF document, you are going to analyze every page and in each page you will look for the following information:
    1. The date of the document.
    2. The sender of the document.
    3. If the document refers to a payment or not.
    4. If the document refers to a payment, you should provide:
    1. The payment amount or "tasa"
    2. The due date of the payment
    3. The payment method if available 
    4. A small description of the payment reason
    If you don't find any of the information, you should return "Not found" for that specific information.
    If the document does not mention any of the information at all, you should return "None".
    ''',  
)

text = ""
for page in reader.pages:
    text = text + page.extract_text()
    
result = agent.run_sync(text)  
print(result.output)
print("-----------------------------------------------------------------------------------------------------------------------------------------------")

