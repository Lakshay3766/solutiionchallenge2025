import tkinter as tk    
from tkinter import Canvas, Text, Button    
from PIL import Image, ImageTk, ImageGrab    
import subprocess    
import os    
import io    
from google.cloud import vision    
from texttospeech import TextToSpeech   
from gtts import gTTS    
import pygame    
import tempfile    
import logging    
from datetime import datetime    
import speech_recognition as sr  
from googletrans import Translator  
import threading  
  
class TextToSpeech:  
   def __init__(self):  
      self.setup_logging()  
      self.initialize_audio()  
  
   def setup_logging(self):  
      logging.basicConfig(  
        filename=f'tts_{datetime.now().strftime("%Y%m%d")}.log',  
        level=logging.INFO,  
        format='%(asctime)s - %(levelname)s - %(message)s'  
      )  
  
   def initialize_audio(self):  
      try:  
        pygame.mixer.init()  
        logging.info("Audio system initialized successfully")  
      except Exception as e:  
        logging.error(f"Failed to initialize audio system: {e}")  
  
   def speak_text(self, text, language='en'):  
      try:  
        print(f"Text to speak: {text}")  # Debugging line  
        tts = gTTS(text=text, lang=language)  
  
        # Create a temporary file  
        fd, temp_file = tempfile.mkstemp(suffix='.mp3')  
        tts.save(temp_file)  
        os.close(fd)  # Close the file descriptor  
  
        # Play the audio  
        pygame.mixer.music.load(temp_file)  
        pygame.mixer.music.play()  
        while pygame.mixer.music.get_busy():  
           pygame.time.Clock().tick(10)  
        pygame.mixer.music.unload()  
  
        # Clean up  
        os.remove(temp_file)  
  
        logging.info("Text successfully converted to speech")  
        return True  
      except Exception as e:  
        logging.error(f"Failed to convert text to speech: {e}")  
        print(f"Error: {e}")  
        return False  
  
def speak_digital_text():  
   try:  
      # Get text from digital text area  
      text = text_area.get("1.0", tk.END).strip()  
  
      if text:  
        # Initialize TTS if not already initialized  
        if not hasattr(window, 'tts'):  
           window.tts = TextToSpeech()  
  
        # Convert and play  
        window.tts.speak_text(text)  
      else:  
        print("No text to speak")  
   except Exception as e:  
      print(f"Error in text to speech: {e}")  
      logging.error(f"Text to speech error: {e}")  
  
# Global variables for drawing state  
drawing_tool = None  
pen_color = "black"  # Initial pen color  
bg_image_tk = None  # Store the background image globally to avoid redrawing it multiple times  
drawn_objects = []  # List to store the drawn shapes for erasing purposes  
last_x, last_y = None, None  # To keep track of the last position for smooth drawing  
pen_thickness = 7  # Default pen thickness  
eraser_size = 10  # Default eraser size  
  
# Function to update the canvas with a background image  
def update_canvas_background(canvas, image_path):  
   global bg_image_tk  
   canvas_width = canvas.winfo_width()  
   canvas_height = canvas.winfo_height()  
   bg_image = Image.open(image_path).resize((canvas_width, canvas_height), Image.LANCZOS)  
   bg_image_tk = ImageTk.PhotoImage(bg_image)  
   canvas.create_image(0, 0, image=bg_image_tk, anchor=tk.NW)  
   canvas.image = bg_image_tk  # Keep a reference to avoid garbage collection  
  
# Function to update canvas on window resize  
def resize_canvas(event, canvas, image_path):  
   canvas.config(width=event.width, height=event.height)  
   # Only update background when resizing, not erasing it  
   update_canvas_background(canvas, image_path)  
  
# Function to handle tool selection  
def set_tool(selected_tool):  
   global drawing_tool, last_x, last_y  
   drawing_tool = selected_tool  
   last_x, last_y = None, None  # Reset last position when switching tools  
  
# Function to change pen color between black and blue  
def toggle_pen_color():  
   global pen_color  
   pen_color = "blue" if pen_color == "black" else "black"  
  
# Function to update pen thickness  
def update_pen_thickness(val):  
   global pen_thickness  
   pen_thickness = int(val)  
  
# Function to update eraser size  
def update_eraser_size(val):  
   global eraser_size  
   eraser_size = int(val)  
  
# Function to handle drawing with pen or eraser  
def draw(event, canvas):  
   global last_x, last_y, pen_thickness, eraser_size  
   if drawing_tool == "pen":  
      if last_x is None or last_y is None:  
        last_x, last_y = event.x, event.y  
        return  
      # Draw a smooth line from the last position to the current position with selected thickness  
      line = canvas.create_line(last_x, last_y, event.x, event.y, fill=pen_color, width=pen_thickness, smooth=True)  
      drawn_objects.append(line)  
      last_x, last_y = event.x, event.y  
   elif drawing_tool == "eraser":  
      # Erase drawn lines by comparing distance to the mouse pointer  
      for obj in drawn_objects:  
        coords = canvas.coords(obj)  
        # Check for lines (length is 4 for lines: x1, y1, x2, y2)  
        if len(coords) == 4:  
           x1, y1, x2, y2 = coords  
           # Check if the mouse is close enough to any part of the line (distance check)  
           if (min(abs(event.x - x1), abs(event.x - x2)) <= eraser_size and  
              min(abs(event.y - y1), abs(event.y - y2)) <= eraser_size):  
              canvas.delete(obj)  
              drawn_objects.remove(obj)  
  
# Function to reset the last pen position on button release  
def reset_last_position(event):  
   global last_x, last_y  
   last_x, last_y = None, None  
  
# Function to clear the canvas (without affecting background)  
def clear_screen(canvas, image_path):  
   canvas.delete("all")  # Delete all drawn objects from canvas  
   update_canvas_background(canvas, image_path)  # Redraw background, preserving it  
   drawn_objects.clear()  # Clear the list of drawn objects  
  
# Function to open calculator  
def open_calculator():  
   subprocess.run("calc")  
  
# Function for "Next" button functionality  
def next_sheet():  
   print("Next sheet functionality")  # Placeholder for next sheet logic  
  
# Function for "Back" button functionality  
def previous_sheet():  
   print("Previous sheet functionality")  # Placeholder for previous sheet logic  
  
# Function for "Recognize" button functionality  
def recognize_text():  
   # Get the canvas image  
   canvas = pages[0].winfo_children()[0]  
   image = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(), canvas.winfo_rooty() + canvas.winfo_height()))  
  
   # Save the image to a temporary file  
   temp_file = "temp.png"  
   image.save(temp_file)  
  
   # Create a client instance  
   client = vision.ImageAnnotatorClient()  
  
   # Load the image into memory  
   with io.open(temp_file, 'rb') as image_file:  
      content = image_file.read()  
  
   # Create a Vision API image instance  
   image = vision.Image(content=content)  
  
   # Perform text recognition  
   response = client.text_detection(image=image)  
  
   # Extract the text from the response  
   text = []  
   for page in response.full_text_annotation.pages:  
      for block in page.blocks:  
        for paragraph in block.paragraphs:  
           for word in paragraph.words:  
              for symbol in word.symbols:  
                text.append(symbol.text)  
  
   # Display the recognized text  
   text_area.delete(1.0, tk.END)  
   text_area.insert(tk.END, ' '.join(text))  
  
   # Clean up  
   os.remove(temp_file)  
  
# Function to handle drawing on diagram canvas  
def draw_diagram(event):  
   global last_x, last_y, pen_thickness  
   if last_x is None or last_y is None:  
      last_x, last_y = event.x, event.y  
      return  
   # Draw a smooth line from the last position to the current position with selected thickness  
   line = diagram_canvas.create_line(last_x, last_y, event.x, event.y, fill=pen_color, width=pen_thickness, smooth=True)  
   last_x, last_y = event.x, event.y  
  
# Function to reset the last pen position on button release for diagram canvas  
def reset_last_position_diagram(event):  
   global last_x, last_y  
   last_x, last_y = None, None  
  
# Function to recognize diagram  
def recognize_diagram():  
   # Get the diagram canvas image  
   image = ImageGrab.grab(bbox=(diagram_canvas.winfo_rootx(), diagram_canvas.winfo_rooty(), diagram_canvas.winfo_rootx() + diagram_canvas.winfo_width(), diagram_canvas.winfo_rooty() + diagram_canvas.winfo_height()))  
  
   # Save the image to a temporary file  
   temp_file = "temp.png"  
   image.save(temp_file)  
  
   # Create a client instance  
   client = vision.ImageAnnotatorClient()  
  
   # Load the image into memory  
   with io.open(temp_file, 'rb') as image_file:  
      content = image_file.read()  
  
   # Create a Vision API image instance  
   image = vision.Image(content=content)  
  
   # Perform object detection  
   response = client.object_localization(image=image)  
  
   # Extract the detected objects from the response  
   objects = []  
   for object_ in response.localized_object_annotations:  
      objects.append(object_.name)  
  
   # Display the detected objects  
   diagram_label.config(text="Detected Objects: " + ', '.join(objects))  
  
   # Clean up  
   os.remove(temp_file)  
  
# Function to handle speech-to-text functionality  
def speech_to_text_auto_detect():  
   # Initialize recognizer and translator  
   recognizer = sr.Recognizer()  
   translator = Translator()  
  
   # Use the default microphone as the audio source  
   with sr.Microphone() as source:  
      print("Listening... Speak in any language.")  
      audio = recognizer.listen(source)  
  
      try:  
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
  
        # Insert the recognized text into the digital text area  
        text_area.delete(1.0, tk.END)  
        text_area.insert(tk.END, native_script_text)  
        text_area.see(tk.END)  
        text_area.update_idletasks()  # Update the GUI to show the recognized text  
      except sr.UnknownValueError:  
        print("Could not understand the audio.")  
      except sr.RequestError as e:  
        print(f"Error with the recognition service: {e}")  
      except Exception as e:  
        print(f"An error occurred: {e}")  
  
def start_speech_to_text():  
   threading.Thread(target=speech_to_text_auto_detect).start()  
  
# Create the main application window  
window = tk.Tk()  
window.title("Assistive Exam Paper UI")  
window.geometry("1280x800")  
window.configure(bg="#a2d9e4")  
  
# Right section reduced width (updated)  
rhs_width = 200  # Reduced width of the right section  
  
# Header Section covering full width  
header_label = tk.Label(window, text="Test Mode", font=("Itim", 16), bg="#a2d9e4", pady=10)  
header_label.pack(fill=tk.X)  
  
# Right Section for Canvas and Tools (previously left, now on the right)  
right_frame = tk.Frame(window, bg="white")  
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  
  
# Create 5 pages with different background images  
pages = []  
for i in range(1):  
   page_frame = tk.Frame(right_frame, bg="white")  
   page_frame.pack(fill=tk.BOTH, expand=True)  
   canvas = Canvas(page_frame, bg="white", highlightthickness=0)  
   canvas.pack(fill=tk.BOTH, expand=True)  
   image_path = f"images\\lines{i}.png"  
   update_canvas_background(canvas, image_path)  
   canvas.bind("<Configure>", lambda event, canvas=canvas, image_path=image_path: resize_canvas(event, canvas, image_path))  
   canvas.bind("<B1-Motion>", lambda event, canvas=canvas: draw(event, canvas))  
   canvas.bind("<ButtonRelease-1>", reset_last_position)  
   pages.append(page_frame)  
  
# Add a sample question to the first page  
question_label = pages[0].winfo_children()[0].create_text(10, 10, text="Q1: Sample Question", font=("Itim", 14), anchor=tk.NW)  
  
# Add some extra space for OCR  
ocr_space = pages[0].winfo_children()[0].create_rectangle(10, 50, 500, 200, fill="white", outline="black")  
  
# Toolbar Section  
toolbar_frame = tk.Frame(right_frame, bg="white", highlightthickness=0)  
toolbar_frame.pack(side=tk.BOTTOM, pady=10)  
  
toolbar_box = tk.Frame(toolbar_frame, bg="#ffffff", padx=10, pady=10)  
toolbar_box.pack()  
  
# Function to create tool buttons  
def create_tool_button(parent, image_path, tool_name, command=None):  
   image = Image.open(image_path).resize((50, 50), Image.LANCZOS)  
   photo = ImageTk.PhotoImage(image)  
   button = tk.Button(parent, image=photo, bg="#ffffff", relief="flat", command=command or (lambda: set_tool(tool_name)))  
   button.image = photo  # Keep a reference to avoid garbage collection  
   button.pack(side=tk.LEFT, padx=5)  
   return button  
  
# Define the image paths for the tools  
tool_images = [  
   r"images\a.png",  # Back button (a.png)  
   r"images\1.png",  # Pen tool (fb.png)  
   r"images\2.png",  # Eraser tool (2.png)  
   r"images\3.png",  # Calculator button (3.png)s  
   r"images\4.png",  # Pen color toggle button (4.png)  
   r"images\6.png",  # Next button (6.png)  
   r"images\6.png"  # Recognize button (7.png)  
]  
  
# Create tool buttons with commands for Back and Next  
back_button = create_tool_button(toolbar_box, tool_images[0], "back", previous_sheet)  
pen_button = create_tool_button(toolbar_box, tool_images[1], "pen")  
eraser_button = create_tool_button(toolbar_box, tool_images[2], "eraser")  
calculator_button = create_tool_button(toolbar_box, tool_images[3], "calculator")  
pen_color_button = create_tool_button(toolbar_box, tool_images[4], "pen_color")  
next_button = create_tool_button(toolbar_box, tool_images[5], "next", next_sheet)  
recognize_button = create_tool_button(toolbar_box, tool_images[6], "recognize", recognize_text)  
  
# Assign specific functionality to the buttons  
pen_color_button.config(command=toggle_pen_color)  
calculator_button.config(command=open_calculator)  
  
speech_to_text_button = tk.Button(toolbar_box, text="Speech to Text", command=start_speech_to_text)  
speech_to_text_button.pack(side=tk.LEFT, padx=5)  
  
# Left Section: Digital Text and Diagram (previously right, now on the left)  
left_frame = tk.Frame(window, bg="#f5f5f5", width=rhs_width)  # Set the width to 200  
left_frame.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.N)  
  
# Digital Text Area  
digital_frame = tk.Frame(left_frame, bg="#f5f5f5")  
digital_frame.pack(pady=10, fill=tk.X)  
  
tk.Label(digital_frame, text="Digital Text", font=("Itim", 16), bg="#f5f5f5").pack(pady=10)  
text_area = Text(digital_frame, wrap=tk.WORD, font=("Itim", 12), height=12, bg="white", width=30)  
text_area.pack(pady=10, padx=10, fill=tk.X)  
  
# Add TTS button  
tts_button = tk.Button(  
   digital_frame,  
   text="🔊 Speak Recognized Text",  
   command=lambda: speak_digital_text(),  
   font=("Itim", 12),  
   bg="#4CAF50",  
   fg="white",  
   pady=5  
)  
tts_button.pack(pady=5)  
  
# Diagram Section  
diagram_label = tk.Label(left_frame, text="Diagram", font=("Itim", 14), bg="#f5f5f5")  
diagram_label.pack(pady=20)  
  
diagram_frame = tk.Frame(left_frame, bg="#f5f5f5")  
diagram_frame.pack(pady=10)  
  
diagram_canvas = Canvas(diagram_frame, width=400, height=300, bg="white", highlightthickness=0)  
diagram_canvas.pack()  
diagram_canvas.bind("<B1-Motion>", draw_diagram)  
diagram_canvas.bind("<ButtonRelease-1>", reset_last_position_diagram)  
  
recognize_diagram_button = tk.Button(left_frame, text="Recognize Diagram", command=recognize_diagram)  
recognize_diagram_button.pack(pady=10)  
  
# Bottom-Left Section for "Unattempted," "Answered," etc.  
status_frame = tk.Frame(left_frame, bg="#ffffff")  
status_frame.pack(pady=20)  
  
# Function to create status labels  
def create_status_label(text, color):  
   frame = tk.Frame(status_frame, bg="#f5f5f5")  
   frame.pack(side=tk.LEFT, padx=10)  
   canvas = tk.Canvas(frame, width=30, height=30, bg="#f5f5f5", highlightthickness=0)  
   canvas.pack(side=tk.LEFT)  
   canvas.create_oval(5, 5, 25, 25, fill=color, outline=color)  
   label = tk.Label(frame, text=text, font=("Itim", 12), bg="#f5f5f5")  
   label.pack(side=tk.LEFT, padx=5)  
  
# Create status labels for different question states  
create_status_label("Unattempted", "#ff6f61")  
create_status_label("Answered", "#98c379")  
create_status_label("Marked for Review", "#e06c75")  
  
# Run the application  
window.mainloop()
