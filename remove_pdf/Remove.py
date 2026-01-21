import os
from PyPDF2 import PdfReader, PdfWriter

def remove_password_from_pdfs(base_folder, target_folder, password):
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                source_file_path = os.path.join(root, file)
                try:
                    # Reading the encrypted PDF
                    reader = PdfReader(source_file_path)
                    if reader.is_encrypted:
                        reader.decrypt(password)  # Decrypt the PDF

                        # Create corresponding target folder structure
                        relative_path = os.path.relpath(root, base_folder)
                        target_subfolder = os.path.join(target_folder, relative_path)
                        os.makedirs(target_subfolder, exist_ok=True)

                        # Create the target file path
                        target_file_path = os.path.join(target_subfolder, file)

                        # Write the decrypted content to the new file
                        writer = PdfWriter()
                        for page in reader.pages:
                            writer.add_page(page)

                        with open(target_file_path, "wb") as output_pdf:
                            writer.write(output_pdf)
                        print(f"Password removed and saved: {target_file_path}")
                    else:
                        print(f"File is not encrypted: {source_file_path}")
                except Exception as e:
                    print(f"Failed to process {source_file_path}: {e}")


# Base folder containing the year subfolders with encrypted PDFs
base_folder = r"C:\Users\mural\Downloads\Inofsys_Form16"

# Target folder for saving the decoded PDFs
target_folder = r"C:\Users\mural\Downloads\Inofsys_Form16_Decoded"

# Replace with the actual password for your PDF files
pdf_password = "23-05-1985"

# Call the function to process and decode PDFs
remove_password_from_pdfs(base_folder, target_folder, pdf_password)
