from PIL import Image

# Input and output file paths
input_image = r"C:\Users\mural\Downloads\MicrosoftEdgeDropFiles\Default\20250302141513_00001.jpg"
output_image = r"C:\Users\mural\Downloads\MicrosoftEdgeDropFiles\Default\great_innovus_oct.jpg"

# Open the image
image = Image.open(input_image)

# Save with 85% quality
image.save(output_image, "JPEG", quality=70)

print(f"Compressed image saved at: {output_image}")
