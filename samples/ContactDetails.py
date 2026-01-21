import qrcode

# Your contact details
name = "Your Name"
email = "your.email@example.com"
phone1 = "+1234567890"
phone2 = "+0987654321"
linkedin_url = "https://www.linkedin.com/in/yourprofile"

# Create vCard data
vcard_data = f"""
BEGIN:VCARD
VERSION:3.0
FN:{name}
EMAIL:{email}
TEL;TYPE=WORK,VOICE:{phone1}
TEL;TYPE=CELL,VOICE:{phone2}
URL:{linkedin_url}
END:VCARD
"""

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=8,
    border=2,
)
qr.add_data(vcard_data)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="#D303FC", back_color='white')

# Save the image
img.save("contact_qr_code.png")

print("QR code generated and saved as contact_qr_code.png")
