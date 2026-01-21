import os
from PIL import Image

def convert_jpgs_to_pdf(folder_path, output_pdf_path):
    # List to hold all image objects
    image_list = []

    # Iterate through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.startswith("joint_declare_2") and filename.endswith(".png"):
            # Open the image file
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path).convert("RGB")
            image_list.append(img)

    # Save the images as a single PDF
    if image_list:
        image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:])
        print(f"PDF saved as {output_pdf_path}")
    else:
        print("No JPG files found in the specified directory.")

# Usage
folder_path = r"C:\Users\mural\Downloads"
output_pdf_path = os.path.join(folder_path, "joint_declare_2.pdf")

convert_jpgs_to_pdf(folder_path, output_pdf_path)
