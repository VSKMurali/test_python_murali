from PyPDF2 import PdfReader, PdfWriter

def remove_last_blank_page(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Get total number of pages
    total_pages = len(reader.pages)

    # Function to check if a page is blank
    def is_blank(page):
        text = page.extract_text()
        return text is None or text.strip() == ""

    # Copy all pages except the last blank one
    for i in range(total_pages):
        if i == total_pages - 1 and is_blank(reader.pages[i]):
            print("Last page is blank, removing it.")
            continue
        writer.add_page(reader.pages[i])

    # Save the new PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)

# Example usage
remove_last_blank_page("murali_resume_2.pdf", "murali_resume_2_.pdf")