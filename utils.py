# utils.py — fixed, clean version

import os
from jinja2 import Environment, FileSystemLoader
import pdfkit

# Map template names to template file paths
TEMPLATE_MAP = {
    'classic': 'resume_classic.html',
    'modern': 'resume_modern.html',
    'twocol': 'resume_twocol.html',
    'minimal': 'resume_minimal.html',
    'creative': 'resume_creative.html',
}

# ------------------------------------------------------
# VALIDATION
# ------------------------------------------------------

def validate_input(data):
    """Basic validation for required fields."""
    errors = []

    if not data.get("full_name") and not data.get("first_name"):
        errors.append("Please provide your name.")

    if not data.get("email"):
        errors.append("Please provide an email address.")

    return (len(errors) == 0, errors)

# ------------------------------------------------------
# RENDER HTML TEMPLATE
# ------------------------------------------------------

def render_resume_html(template_key, data):
    """Render the selected resume template."""
    template_file = TEMPLATE_MAP.get(template_key, "resume_classic.html")

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=True
    )

    tmpl = env.get_template(template_file)
    html = tmpl.render(data=data)
    return html

# ------------------------------------------------------
# GENERATE PDF (OPTIONAL)
# ------------------------------------------------------

def generate_pdf_if_requested(html_string, output_path="output_resume.pdf"):
    """Generate a PDF from HTML using pdfkit / wkhtmltopdf."""
    try:
        wkhtml = os.environ.get("WKHTMLTOPDF")
        config = pdfkit.configuration(wkhtmltopdf=wkhtml) if wkhtml else None

        pdfkit.from_string(
            html_string,
            output_path,
            configuration=config
        )
        return output_path

    except Exception as e:
        print("PDF generation failed:", e)
        return None
