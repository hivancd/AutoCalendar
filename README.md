# PDF Payment Extractor & Calendar Automator

> **Automate bill management:** This tool watches your Downloads folder for new PDF files (invoices, bills, receipts, etc.), uses OpenAI GPT-4 (via `pydantic_ai`) to analyze document content, extracts payment details if found, and schedules smart reminders in your Google Calendar.

---

## 📜 Table of Contents
- [PDF Payment Extractor \& Calendar Automator](#pdf-payment-extractor--calendar-automator)
  - [📜 Table of Contents](#-table-of-contents)
  - [📌 About](#-about)
  - [✨ Features](#-features)
  - [🛠️ Architecture](#️-architecture)
  - [📦 Requirements](#-requirements)
  - [⚙️ Configuration](#️-configuration)
  - [🏁 Usage](#-usage)
  - [📬 Contact](#-contact)

---

## 📌 About
This Python application streamlines your bill tracking workflow using AI. It monitors the `Downloads` folder, processes each new PDF file with GPT-4 (via `pydantic_ai`), identifies if the document concerns an upcoming payment, and—if so—automatically creates a Google Calendar event with the due date, amount, and a short description.

---

## ✨ Features
- **Automatic folder monitoring** for new PDF files.
- **LLM-powered text extraction**: Uses GPT-4 to parse PDF content intelligently.
- **Smart invoice detection**: Differentiates between payment-related and unrelated documents.
- **Payment info extraction**: Pulls out due dates, amounts, and descriptions.
- **Google Calendar integration**: Schedules a calendar event with extracted payment facts.
- Clear, human-readable event summaries for each payment.

---

## 🛠️ Architecture

| Component             | Stack / Service           |
|-----------------------|--------------------------|
| File Monitoring       | Python (`watchdog`/`os`) |
| PDF Text Extraction   | PyMuPDF or similar       |
| LLM Analysis          | OpenAI GPT-4 via `pydantic_ai` |
| Data Modeling & Validation | `pydantic`         |
| Calendar Automation   | Google Calendar API      |
| Config/Secrets        | `.env` + `python-dotenv` |

---

## 📦 Requirements

- Python 3.8+
- OpenAI account and API key with GPT-4 access
- Google Cloud project & service account for Calendar API
- WinSW file
- The following Python libraries:
  - `pydantic_ai`
  - `openai`
  - `PyMuPDF`
  - `watchdog`
  - `google-api-python-client` & `google-auth`
  - `python-dotenv`
  - `auto-py-to-exe`

---

## ⚙️ Configuration

1. **Environment Variables:**  
  Create a `.env` file with your OpenAI API key and Calendar API credentials:

2. **Google Calendar API Setup:**
   - Create a Google Cloud project.
   - Enable the Calendar API.
   - Create service account credentials and share your Google calendar with the service account email.

3. **How to convert python code to pdf**
    - Install modules: PyInstaller and auto-py-to-exe
    - Run: 'auto-py-to-exe' in cmd
    - Once in UI scroll to settings and Import json config
    - Import the .json config file called 'executable config.json' in 'src/autocalendar'
    - Select output folder for the exe file
    - Download and follow instructions of WinSW for using the exe as a windows services
    - For getting the google api credentials run get creds.exe and follow the instructions
  
---

## 🏁 Usage


---

## 📬 Contact
Hivan Cañizares – hivancdiaz@gmail.com  