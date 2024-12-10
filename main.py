import speech_recognition as sr
import webbrowser
import google.generativeai as genai
import time
import sys
import sounddevice
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import textblob

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
geminiApi = os.getenv('GENAI_API_KEY')
genai.configure(api_key = geminiApi)
gemini = genai.GenerativeModel("gemini-1.5-flash")

def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    
    # Menggunakan file sementara agar tidak perlu menyimpan file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        audio = AudioSegment.from_mp3(temp_audio.name)
        play(audio)

def interactGemini(request):
    # Add an instruction to limit the response length to one paragraph
    convertedRequest = f"Provide answers in one short paragraph to the questions: {request}"
    response = gemini.generate_content(convertedRequest)
    return response.text

def correct_pronunciation(text):
    # Using TextBlob for minor spelling corrections based on pronunciation errors
    corrected_text = str(textblob.TextBlob(text).correct())
    return corrected_text

# Inisialisasi recognizer
recognizer = sr.Recognizer()

while True:
    # Menggunakan mikrofon sebagai sumber audio
    with sr.Microphone() as source:
        # Animasi menunggu input audio
        print("Menunggu anda berbicara", end="")
        for _ in range(3):  # Menampilkan animasi selama 3 detik
            print(".", end="", flush=True)
            time.sleep(1)
        print()  # Pindah ke baris berikutnya

        # Mengatur waktu tenang dan mendengarkan suara dari mikrofon
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

        try:
            # Mengonversi audio menjadi teks menggunakan Google Web Speech API
            text = recognizer.recognize_google(audio, language="en-US")
            
            # Toleransi kesalahan pengucapan menggunakan koreksi otomatis
            corrected_text = correct_pronunciation(text)
            print("Anda mengucapkan (dikoreksi): ", corrected_text)
            
            # Mengirim teks yang telah dikoreksi ke Gemini untuk mendapat jawaban
            response = interactGemini(corrected_text)
            print("Gemini: ", response)
            
            # Menggunakan text-to-speech dengan intonasi yang lebih alami
            text_to_speech(response)
        
        except sr.UnknownValueError:
            print("Maaf, saya tidak dapat mengenali ucapan Anda. Coba lagi.")
        except sr.RequestError as e:
            print("Error pada layanan pengenalan suara; {0}".format(e))
