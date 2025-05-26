from flask import Flask, request, send_file
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

@app.route("/generate-certificate", methods=["POST"])
def generate_certificate():
    data = request.json
    name = data["name"]
    title = data["title"]
    desc = data["desc"]
    date = data["date"]
    category = data["category"]

    template_path = "templates/sap_template.jpg"
    font_path = "fonts/arial.ttf"

    certificate = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(certificate)

    name_font = ImageFont.truetype(font_path, 60)
    text_font = ImageFont.truetype(font_path, 30)
    title_font = ImageFont.truetype(font_path, 20)

    coords = {
        "title": (65, 395),
        "name": (70, 450),
        "desc_start": (70, 550),
        "date": (90, 845),
        "category": (685, 845)
    }

    draw.text(coords["title"], title, fill="black", font=title_font)
    draw.text(coords["name"], name, fill="black", font=name_font)
    draw.text(coords["date"], date, fill="black", font=text_font)
    draw.text(coords["category"], category, fill="black", font=text_font)

    # Wrap desc
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())
        return lines

    max_width = 900
    current_height = coords["desc_start"][1]
    line_spacing = 10
    for line in wrap_text(desc, text_font, max_width):
        draw.text((coords["desc_start"][0], current_height), line, fill="black", font=text_font)
        bbox = draw.textbbox((0, 0), line, font=text_font)
        current_height += (bbox[3] - bbox[1]) + line_spacing

    # Save PDF to memory
    pdf_bytes = BytesIO()
    certificate.save(pdf_bytes, format="PDF", resolution=100.0)
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, download_name=f"{name}_certificate.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
