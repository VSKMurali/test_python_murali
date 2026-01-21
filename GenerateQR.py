import qrcode

# Coordinates for the location (latitude and longitude)
latitude = 37.7749
longitude = -122.4194

# Generate the Google Maps URL
location_url = f"https://maps.google.com/?q={latitude},{longitude}"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=8,
    border=2,
)
qr.add_data(location_url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill='black', back_color='white')

# Save the image
img.save("location_qr_code.png")

print("QR code generated and saved as location_qr_code.png")
