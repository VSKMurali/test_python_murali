from gtts import gTTS

# English and Tamil reminder message
message = "Please take the medicine. தயவுசெய்து மருந்து எடுத்துக்கொள்ளுங்கள். "

# Repeat the message to make it ~90 seconds
repeat_count = 8  # Adjust if needed
full_text = " ".join([message] * repeat_count)

# Generate speech
tts = gTTS(text=full_text, lang='ta')  # 'ta' will work for Tamil + English mixed
tts.save("reminder.mp3")

print("✅ Audio file 'reminder.mp3' generated successfully.")
