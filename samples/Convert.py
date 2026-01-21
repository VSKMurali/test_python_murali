from PIL import Image

def convert_tif_to_jpg(tif_path, jpg_path):
    # Open the TIF image
    with Image.open(tif_path) as img:
        # Convert the TIF image to RGB mode
        img = img.convert("RGB")
        # Save the image in JPG format
        img.save(jpg_path, "JPEG")

# Usage
input_tif_path = "infy_offer.tif"
output_jpg_path = "infy_offer_jpg.jpg"

convert_tif_to_jpg(input_tif_path, output_jpg_path)
