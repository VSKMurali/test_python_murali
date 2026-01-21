import PyPDF2


def remove_pdf_password(input_pdf, output_pdf, password):
    try:
        # Open the encrypted PDF file
        with open(input_pdf, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            # Check if the PDF is encrypted
            if reader.is_encrypted:
                reader.decrypt(password)

            # Create a PdfWriter object
            writer = PyPDF2.PdfWriter()

            # Add all pages to the writer
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                writer.add_page(page)

            # Write the output PDF without password
            with open(output_pdf, "wb") as output_file:
                writer.write(output_file)

        print(f"Password removed and saved as {output_pdf}")
    except Exception as e:
        print(f"An error occurred: {e}")


input_pdf_path = "Jan-2025.pdf"
output_pdf_path = "Jan-2025-decrypted.pdf"
pdf_password = "23-05-1985"

remove_pdf_password(input_pdf_path, output_pdf_path, pdf_password)
