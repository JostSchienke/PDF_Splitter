import fitz  # PyMuPDF
import os

def split_a2_to_a4(input_pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    doc = fitz.open(input_pdf_path)
    if len(doc) != 1:
        print("This script only works with a single-page PDF.")
        return

    page = doc[0]
    width, height = page.rect.width, page.rect.height

    # A2 is 420 x 594 mm → 1190.55 x 1683.78 points (1 mm = ~2.8346 pt)
    # A4 is 210 x 297 mm → so 1/4 of A2 in 2x2 tiles

    mid_x = width / 2
    mid_y = height / 2

    # Define the 4 rectangles for A4-sized quarters
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
        output_path = os.path.join(output_folder, f"A4_tile_{i + 1}.pdf")
        new_doc.save(output_path)
        new_doc.close()
        print(f"Saved: {output_path}")

    doc.close()

# === Usage ===
input_pdf = "Map.pdf"
output_dir = "split_output"

split_a2_to_a4(input_pdf, output_dir)
