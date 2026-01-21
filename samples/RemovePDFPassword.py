import os
import PyPDF2


def remove_password_from_pdfs(directory, password):
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory, filename)
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    if reader.is_encrypted:
                        reader.decrypt(password)

                    writer = PyPDF2.PdfWriter()
                    # Add all pages to the writer
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        writer.add_page(page)

                    # Construct output file path with prefix "decrypted_"
                    output_file_path = os.path.join(directory, f"decrypted_{filename}")
                    with open(output_file_path, "wb") as output_file:
                        writer.write(output_file)

                    print(f"Decrypted and saved: {output_file_path}")


    except Exception as e:
        print(f"An error occurred: {e}")


# Usage
directory_path = r"C:\Users\mural\Desktop\fsp_salary_certficates"
pdf_password = "murali242"

remove_password_from_pdfs(directory_path, pdf_password)
