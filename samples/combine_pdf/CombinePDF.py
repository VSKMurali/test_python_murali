from pypdf import PdfReader, PdfWriter


def combine_pdfs(pdf_list, output_path):
    # Create a PdfWriter object
    pdf_writer = PdfWriter()

    # Iterate through the list of PDF files in the specified order
    for pdf in pdf_list:
        # Open the PDF file
        pdf_reader = PdfReader(pdf)

        # Add each page to the writer object
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    # Write out the combined PDF
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"Combined PDF saved as {output_path}")


# Usage
pdf_files = [
    r"C:\Users\mural\Desktop\infy_last_3_months_payslip\print_out_old.pdf",  # This PDF will be second in the combined document
    r"C:\Users\mural\Desktop\infy_last_3_months_payslip\fsp_May_20160613.pdf",
    r"C:\Users\mural\Desktop\infy_last_3_months_payslip\fsp_April_20160510.pdf",
    r"C:\Users\mural\Desktop\infy_last_3_months_payslip\fsp_March_20160413.pdf",
    r"C:\Users\mural\Desktop\infy_last_3_months_payslip\joint_declare_2.pdf"
]
output_pdf = r"C:\Users\mural\Desktop\infy_last_3_months_payslip\print_out.pdf"

combine_pdfs(pdf_files, output_pdf)
