from gtts import gTTS  
from gtts.lang import tts_langs  
import os  
import tempfile  
import logging  
from io import BytesIO  
import pygame  
from datetime import datetime  
import langdetect  
  
# Setup logging  
logging.basicConfig(  
  filename=f'tts_app_{datetime.now().strftime("%Y%m%d")}.log',  
  level=logging.INFO,  
  format='%(asctime)s - %(levelname)s - %(message)s'  
)  
  
class TextToSpeech:  
  def __init__(self):  
   self.initialize_audio()  
   self.load_languages()  
  
  def initialize_audio(self):  
   """Initialize pygame mixer for audio playback"""  
   try:  
    pygame.mixer.init()  
    logging.info("Audio system initialized successfully")  
   except Exception as e:  
    logging.error(f"Failed to initialize audio system: {e}")  
  
  def load_languages(self):  
   """Load all available languages from gTTS"""  
   try:  
    self.languages = tts_langs()  
    logging.info(f"Loaded {len(self.languages)} languages successfully")  
   except Exception as e:  
    logging.error(f"Failed to load languages: {e}")  
    self.languages = {"en": "English"}  # Fallback to English only  
  
  def create_audio(self, text, language):  
   """Create audio from text using selected language"""  
   try:  
    tts = gTTS(text=text, lang=language)  
    audio_fp = BytesIO()  
    tts.write_to_fp(audio_fp)  
    return audio_fp  
   except Exception as e:  
    logging.error(f"Failed to create audio: {e}")  
    return None  
  
  def play_audio(self, audio_fp):  
   """Play the generated audio"""  
   try:  
    audio_fp.seek(0)  
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:  
      tmp_file.write(audio_fp.read())  
      tmp_file_path = tmp_file.name  
  
    pygame.mixer.music.load(tmp_file_path)  
    pygame.mixer.music.play()  
    while pygame.mixer.music.get_busy():  
      pygame.time.Clock().tick(10)  
    pygame.mixer.music.unload()  
    os.unlink(tmp_file_path)  
  
   except Exception as e:  
    logging.error(f"Failed to play audio: {e}")  
  
  def detect_language(self, text):  
   """Detect the language of the input text"""  
   try:  
    language = langdetect.detect(text)  
    return language  
   except Exception as e:  
    logging.error(f"Failed to detect language: {e}")  
    return "en"  # Fallback to English  
  
  def speak(self, text):  
   """Speak the given text"""  
   try:  
    language = self.detect_language(text)  
    audio_fp = self.create_audio(text, language)  
    if audio_fp:  
      self.play_audio(audio_fp)  
   except Exception as e:  
    logging.error(f"Failed to speak text: {e}")
