from flask import Flask, render_template, request, redirect, url_for, send_file, flash
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Load sample data for quick testing
with open('sample_data.json', 'r', encoding='utf-8') as f:
SAMPLE = json.load(f)


@app.route('/', methods=['GET'])
def index():
# Show form with sample data pre-filled
return render_template('index.html', data=SAMPLE)


@app.route('/generate', methods=['POST'])
def generate():
# Collect form data
data = request.form.to_dict(flat=False)
# Convert single-value lists to scalars where appropriate
normalized = {}
for k, v in data.items():
if len(v) == 1:
normalized[k] = v[0]
else:
normalized[k] = v


# Handle file upload (photo)
photo = request.files.get('photo')
if photo and photo.filename:
filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
photo.save(filename)
normalized['photo'] = filename


# Validate input (utils)
ok, errors = validate_input(normalized)
if not ok:
for e in errors:
flash(e, 'danger')
return redirect(url_for('index'))


# Which template
template = normalized.get('template_choice', 'classic')


# Render HTML resume
html = render_resume_html(template, normalized)


# If user asked for PDF, generate and send
download_type = normalized.get('download', 'html')
if download_type == 'pdf':
pdf_path = generate_pdf_if_requested(html)
if pdf_path:
return send_file(pdf_path, as_attachment=True)
else:
flash('PDF generation not available on this system. Showing HTML preview instead.', 'warning')


# Otherwise show preview page
return render_template('preview.html', resume_html=html)


if __name__ == '__main__':
app.run(debug=True)
