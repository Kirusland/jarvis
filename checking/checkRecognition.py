import speech_recognition

r = speech_recognition.Recognizer()
with speech_recognition.Microphone(device_index=1) as source:
    print("Сккажите что-нибудь...")
    audio = r.listen(source)

query = r.recognize_google(audio, language="ru-RU")
print(query.lower())