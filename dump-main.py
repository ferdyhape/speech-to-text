import speech_recognition as sr
import sounddevice
import webbrowser  # Impor webbrowser di luar fungsi

# Fungsi untuk membuka browser
def open_browser():
    webbrowser.open('https://www.google.com')

def open_youtube():
    webbrowser.open('https://www.youtube.com')

def open_file_manager():
    webbrowser.open('file:///home/')

def analyze_text(text):
    if "buka browser" in text.lower():
        open_browser()
        print("Browser berhasil dibuka.")
    elif "buka youtube" in text.lower():
        open_youtube()
        print("Youtube berhasil dibuka.")
    elif "buka file manager" in text.lower():
        open_file_manager()
        print("File manager berhasil dibuka.")
    else:
        print("Perintah tidak dikenali.")

# Inisialisasi recognizer
recognizer = sr.Recognizer()

while True:
    # Menggunakan mikrofon sebagai sumber audio
    with sr.Microphone() as source:
        print("Silakan berbicara...")

        # Mengatur waktu tenang dan mendengarkan suara dari mikrofon
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.listen(source)

        try:
            # Mengonversi audio menjadi teks menggunakan Google Web Speech API
            text = recognizer.recognize_google(audio, language="id-ID")
            analyze_text(text)
            print("Anda mengucapkan: ", text)
        except sr.UnknownValueError:
            # print("Maaf, saya tidak bisa mengenali ucapan.")
            pass
        except sr.RequestError as e:
            print("Error pada layanan pengenalan suara; {0}".format(e))
        


