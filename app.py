from flask import Flask, render_template, request, send_file
import pdfkit
import base64

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ---------------- GENERATE + PREVIEW ----------------
@app.route("/generate", methods=["POST"])
def generate():
    raw = request.form.to_dict(flat=False)

    # Normalize keys
    data = {}
    for k, v in raw.items():
        data[k.replace("[]", "")] = v

    # Theme
    data["theme"] = request.form.get("theme", "blue")

    # Section order
    section_order = {
        "summary": int(request.form.get("order_summary", 1)),
        "skills": int(request.form.get("order_skills", 2)),
        "education": int(request.form.get("order_education", 3)),
        "experience": int(request.form.get("order_experience", 4)),
        "certificates": int(request.form.get("order_certificates", 5)),
    }

    data["section_order"] = [
        s for s, _ in sorted(section_order.items(), key=lambda x: x[1])
    ]

    # Photo → base64
    photo = request.files.get("photo")
    if photo and photo.filename:
        encoded = base64.b64encode(photo.read()).decode("utf-8")
        data["photo_base64"] = [encoded]
    else:
        data["photo_base64"] = []

    template = data.get("template_choice", ["classic"])[0]

    from utils import render_resume_html
    resume_html = render_resume_html(template, data)

    return render_template("preview.html", resume_html=resume_html)


# ---------------- PDF DOWNLOAD ----------------
@app.route("/download/pdf", methods=["POST"])
def download_pdf():
    resume_html = request.form.get("resume_html")

    config = pdfkit.configuration(
        wkhtmltopdf="/usr/bin/wkhtmltopdf"
    )

    options = {
        "enable-local-file-access": None,
        "print-media-type": None,
        "margin-top": "20mm",
        "margin-bottom": "20mm",
        "margin-left": "20mm",
        "margin-right": "20mm",
        "encoding": "UTF-8",
        "quiet": ""
    }

    pdfkit.from_string(
        resume_html,
        "resume.pdf",
        configuration=config,
        options=options
    )

    return send_file("resume.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
