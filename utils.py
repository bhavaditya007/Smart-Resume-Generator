import os
from jinja2 import Environment, FileSystemLoader
import pdfkit


TEMPLATE_MAP = {
'classic': 'resume_classic.html',
'modern': 'resume_modern.html',
'twocol': 'resume_twocol.html',
'minimal': 'resume_minimal.html',
'creative': 'resume_creative.html',
}


# Basic validation
def validate_input(data):
errors = []
if not data.get('first_name') and not data.get('full_name'):
errors.append('Please provide your name.')
if not data.get('email'):
errors.append('Please provide an email.')
return (len(errors) == 0, errors)


# Render the selected Jinja2 template into an HTML string
def render_resume_html(template_key, data):
template_file = TEMPLATE_MAP.get(template_key, 'resume_classic.html')
env = Environment(loader=FileSystemLoader('templates'))
tmpl = env.get_template(template_file)
html = tmpl.render(data=data)
return html


# Try to generate a PDF using pdfkit (requires wkhtmltopdf installed)
def generate_pdf_if_requested(html_string, output_path='output_resume.pdf'):
try:
config = None
# If WKHTMLTOPDF env var provided, use it
wkhtml = os.environ.get('WKHTMLTOPDF')
if wkhtml:
config = pdfkit.configuration(wkhtmltopdf=wkhtml)
pdfkit.from_string(html_string, output_path, configuration=config)
return output_path
except Exception as e:
print('PDF generation failed:', e)
return None
