from PIL import Image, ImageDraw, ImageFont
import os

def generate_certificate(name, date, category, year):
    # Paths
    template_path = "templates/sap_template.png"
    font_path = "fonts/72-Bold.ttf"
    output_img_path = f"output/{name.replace(' ', '_')}_certificate.png"
    output_pdf_path = f"output/{name.replace(' ', '_')}_certificate.pdf"

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

    # Create output directory if not exists
    os.makedirs("output", exist_ok=True)

    # Save as PNG
    certificate.save(output_img_path, "PNG")

    # Save as PDF
    certificate.save(output_pdf_path, "PDF", resolution=100.0)

    print(f"✅ Certificate saved as PDF: {output_pdf_path}")

# Example usage
if __name__ == "__main__":
    generate_certificate(
        name="Ligory.A",
        date="26th May 2024",
        category="Innovation Star",
        year="2025"
    )
