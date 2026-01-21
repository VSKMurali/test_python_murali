from pypdf import PdfReader, PdfWriter

# Define input and output PDF file paths
input_pdf = r"C:\Users\mural\Downloads\MicrosoftEdgeDropFiles\Default\farshore_farm_16.pdf"
output_pdf = r"C:\Users\mural\Downloads\MicrosoftEdgeDropFiles\Default\output_compressed.pdf"

# Open the PDF file
reader = PdfReader(input_pdf)
writer = PdfWriter()

# Reduce image quality and compression
for page in reader.pages:
    page.compress_content_streams()  # Compress page content
    writer.add_page(page)

# Save the compressed PDF
with open(output_pdf, "wb") as f:
    writer.write(f)

print(f"Compressed PDF saved at: {output_pdf}")
