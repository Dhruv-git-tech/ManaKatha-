from fpdf import FPDF
import os

def generate_pdf(story_data, filename="story.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("ArialUnicode", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("ArialUnicode", size=12)
    
    for key, value in story_data.items():
        pdf.multi_cell(0, 10, f"{key}: {value}\n", align='L')

    output_path = os.path.join("/tmp", filename)
    pdf.output(output_path)
    return output_path
