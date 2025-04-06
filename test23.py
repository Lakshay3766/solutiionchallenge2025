import speech_recognition as sr
from googletrans import Translator

def speech_to_text_auto_detect():
    # Initialize recognizer and translator
    recognizer = sr.Recognizer()
    translator = Translator()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening... Speak in any language.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise

        try:
            # Capture audio from the user
            audio = recognizer.listen(source, timeout=10)

            # Recognize speech using Google Web Speech API
            print("Processing...")
            recognized_text = recognizer.recognize_google(audio)

            # Detect the language of the recognized text
            detected_language = translator.detect(recognized_text).lang

            # Translate the text into its native script if necessary
            if detected_language != 'en':  # Only translate if it's not English
                native_script_text = translator.translate(
                    recognized_text, src='en', dest=detected_language).text
            else:
                native_script_text = recognized_text

            # Display the recognized text in its native format
            print(f"Recognized Text ({detected_language}): {native_script_text}")
            print(f"Detected Language: {detected_language}")

            return native_script_text, detected_language
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error with the recognition service: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None, None

# Example Usage
# if _name_ == "_main_":
speech_to_text_auto_detect()