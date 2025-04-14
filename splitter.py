import fitz  # PyMuPDF
import os

def split_file(input_pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    doc = fitz.open(input_pdf_path)
    if len(doc) != 1:
        print("This script only works with a single-page PDF.")
        return

    page = doc[0]
    width, height = page.rect.width, page.rect.height

    # A2 is 420  x 594  mm
    # A4 is 210  x 297  mm 
    # A6 is 105  x 148,5mm
    # A8 is 52,5 x 74,25mm

    mid_x = width / 2
    mid_y = height / 2

    # Define the 4 rectangles
    tiles = [
        fitz.Rect(0, 0, mid_x, mid_y),            # Top-left
        fitz.Rect(mid_x, 0, width, mid_y),        # Top-right
        fitz.Rect(0, mid_y, mid_x, height),       # Bottom-left
        fitz.Rect(mid_x, mid_y, width, height),   # Bottom-right
    ]

    for i, rect in enumerate(tiles):
        new_doc = fitz.open()
        new_page = new_doc.new_page(width=mid_x, height=mid_y)
        new_page.show_pdf_page(new_page.rect, doc, 0, clip=rect)
        output_path = os.path.join(output_folder, f"tile_{i + 1}.pdf")
        new_doc.save(output_path)
        new_doc.close()
        print(f"Saved: {output_path}")

    doc.close()

# === Usage ===
input_pdf = "Map.pdf"
output_dir = "split_output"

split_file(input_pdf, output_dir)
