import fitz  # PyMuPDF
from pathlib import Path

input_file = Path("C:/Users/mural/Downloads/muralimanickaathmarao_13Sep_3.pdf")
output_file = Path("C:/Users/mural/Downloads/murali_resume.pdf")

# Open the PDF file
pdf_document = fitz.open(input_file)

# Retrieve the current metadata
metadata = pdf_document.metadata
print("Old Title:", metadata.get("title"))

# Update the title in the metadata
metadata["title"] = "Murali-Java-SpringBoot-Resume"

# Set the new metadata to the document
pdf_document.set_metadata(metadata)

# Specify the page number to delete (0-indexed)
#page_number = 2

# Delete the page
#pdf_document.delete_page(page_number)

# Save the modified PDF
pdf_document.save(output_file)

#print(f"Page {page_number + 1} deleted successfully!")
