import fitz  # PyMuPDF


def convert_pdf_to_jpg(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)

        # Convert the page to an image
        image = page.get_pixmap()

        # Define output file path
        output_file = f"{output_folder}/RL_740968_image.jpg"

        # Save the image as JPG
        image.save(output_file)
        print(f"Saved: {output_file}")

    pdf_document.close()


# Example usage
pdf_path = r"C:\Users\mural\Desktop\infy_last_3_months_payslip\RL_740968.pdf"  # Path to your PDF file
output_folder = r"C:\Users\mural\Desktop\infy_last_3_months_payslip"  # Folder to save JPGs

convert_pdf_to_jpg(pdf_path, output_folder)