from flask import Flask, request, send_file
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to certificate generation page"

@app.route("/generate-certificate", methods=["POST"])
def generate_certificate():
    data = request.json
    name = data["name"]
    date = data["date"]
    category = data["category"]
    year = data["year"]
    # Paths
    template_path = "templates/sap_template.png"
    font_path = "fonts/72-Bold.ttf"

    # Load template
    certificate = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(certificate)

    # Fonts
    category_name_font = ImageFont.truetype(font_path, 37.3)
    year_font = ImageFont.truetype(font_path, 20)
    date_font = ImageFont.truetype(font_path, 18)

    # Coordinates
    coords = {
        "name": (220, 265),
        "date": (180, 568),
        "year": (448, 471),
        "category": (290, 130)
    }

    if len(name.split()) == 1 or len(name) < 7:
        name_x = coords["name"][0] + 150  
    else:
        name_x = coords["name"][0]
    
    # Center the name horizontally
    image_width = 855
    name_width = draw.textlength(name, font=category_name_font)
    name_x = (image_width - name_width) // 2
    draw.text((name_x, coords["name"][1]), name, fill="#00008B", font=category_name_font)

    # Center the category horizontally
    image_width = 855
    category_width = draw.textlength(category, font=category_name_font)
    category_x = (image_width - category_width) // 2
    draw.text((category_x, coords["category"][1]), category, fill="Black", font=category_name_font)

    # Draw fields with specified colors
    draw.text(coords["date"], date, fill="gray", font=date_font)
    draw.text(coords["year"], year, fill="black", font=year_font)

    pdf_bytes = BytesIO()
    certificate.save(pdf_bytes, format="PDF", resolution=100.0)
    pdf_bytes.seek(0)
   
    return send_file(pdf_bytes, download_name=f"{name}_certificate.pdf", mimetype="application/pdf")
    

# Example usage
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
