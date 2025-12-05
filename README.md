# Smart Resume Generator (Python / Flask)


A Flask web app that collects user information and renders resumes in multiple templates.


## Features
- 5 templates (Classic, Modern, Two-column, Minimal, Creative)
- Preview and download as HTML / PDF (PDF requires `pdfkit` + `wkhtmltopdf`)
- Simple validation and sample data


## Setup
1. Create a virtualenv: `python -m venv venv && source venv/bin/activate`
2. Install deps: `pip install -r requirements.txt`
3. (Optional) Install wkhtmltopdf for PDF export. On Ubuntu: `sudo apt install wkhtmltopdf`
4. Run: `python app.py` and open `http://127.0.0.1:5000`.


## Notes
- If you don't want to install `wkhtmltopdf`, the app still renders HTML previews which can be printed to PDF from the browser.
