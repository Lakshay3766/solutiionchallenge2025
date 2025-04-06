import speech_recognition as sr  
  
class SpeechToText:  
  def __init__(self):  
   self.languages = {  
    "English": "en-US",  
    "Hindi": "hi-IN",  
    "Kannada": "kn-IN",  
    "Telugu": "te-IN",  
    "Tamil": "ta-IN",  
    "Marathi": "mr-IN",  
    "Gujarati": "gu-IN",  
    "Bengali": "bn-IN"  
   }  
  
  def transcribe_audio(self, language):  
   # Create a speech recognition object  
   recognizer = sr.Recognizer()  
  
   # Use the microphone as the audio source  
   with sr.Microphone() as source:  
    # Adjust the energy threshold to reduce background noise  
    recognizer.adjust_for_ambient_noise(source)  
  
    # Display a message to the user  
    print("Please say something...")  
  
    # Listen for audio from the microphone  
    audio = recognizer.listen(source)  
  
    try:  
      # Transcribe the audio using the specified language  
      transcript = recognizer.recognize_google(audio, language=self.languages[language])  
  
      # Display the transcription text in the same language as the spoken input  
      if language == "Hindi":  
       print("आपका कथन: " + transcript)  
      elif language == "Kannada":  
       print("ನಿಮ್ಮ ಹೇಳಿಕೆ: " + transcript)  
      elif language == "Telugu":  
       print("మీ ప్రకటన: " + transcript)  
      elif language == "Tamil":  
       print("உங்கள் கூற்று: " + transcript)  
      elif language == "Marathi":  
       print("तुमचा कथन: " + transcript)  
      elif language == "Gujarati":  
       print("તમારો કથન: " + transcript)  
      elif language == "Bengali":  
       print("আপনার বক্তব্য: " + transcript)  
      else:  
       print("You said: " + transcript)  
  
    except sr.UnknownValueError:  
      print("Could not understand what you said")  
  
    except sr.RequestError as e:  
      print("Error: {0}".format(e))  
  
  def start_transcription(self, language):  
   self.transcribe_audio(language)  
  
# Example usage:  
speech_to_text = SpeechToText()  
speech_to_text.start_transcription("English")
