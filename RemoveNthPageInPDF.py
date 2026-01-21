from PyPDF2 import PdfReader, PdfWriter


def remove_page(input_pdf, output_pdf, page_number):
    """
    Remove the n-th page (1-based index) from a PDF.

    :param input_pdf: Path to input PDF
    :param output_pdf: Path to output PDF
    :param page_number: Page number to remove (1 = first page)
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    if page_number < 1 or page_number > total_pages:
        raise ValueError(f"Invalid page number {page_number}. PDF has {total_pages} pages.")

    for i in range(total_pages):
        # Skip the page to be removed
        if i == page_number - 1:
            print(f"Removing page {page_number}")
            continue
        writer.add_page(reader.pages[i])

    # Save the new PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)


# Example usage:
remove_page("murali_resume_2.pdf", "murali_resume_2_.pdf", 3)  # Removes 3rd page