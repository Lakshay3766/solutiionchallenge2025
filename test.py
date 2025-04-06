import tkinter as tk
from tkinter import Canvas, Text, Button
from PIL import Image, ImageTk
import subprocess  # For opening the calculator

# Global variables for drawing state
drawing_tool = None
pen_color = "black"  # Initial pen color
bg_image_tk = None  # Store the background image globally to avoid redrawing it multiple times
drawn_objects = []  # List to store the drawn shapes for erasing purposes
last_x, last_y = None, None  # To keep track of the last position for smooth drawing
pen_thickness = 7  # Default pen thickness
eraser_size = 10  # Default eraser size

# Function to update the canvas with a background image
def update_canvas_background(canvas):
    global bg_image_tk
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    bg_image = Image.open(r"images\lines.png").resize((canvas_width, canvas_height), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_image_tk, anchor=tk.NW)
    canvas.image = bg_image_tk  # Keep a reference to avoid garbage collection

# Function to update canvas on window resize
def resize_canvas(event):
    canvas.config(width=event.width, height=event.height)
    # Only update background when resizing, not erasing it
    update_canvas_background(canvas)

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
def draw(event):
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
def clear_screen():
    canvas.delete("all")  # Delete all drawn objects from canvas
    update_canvas_background(canvas)  # Redraw background, preserving it
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

# Function to toggle the visibility of the left section
def toggle_left_section():
    if left_frame.winfo_ismapped():  # If left_frame is currently visible
        left_frame.pack_forget()  # Hide the left section
        toggle_button.pack(anchor='nw', padx=10, pady=10)  # Move the button to the top-left
    else:
        left_frame.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.N)  # Re-show the left section
        toggle_button.pack(anchor='ne', padx=10, pady=10)  # Move the button to the top-right

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

canvas = Canvas(right_frame, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Configure>", resize_canvas)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", reset_last_position)

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
    r"images\2.png",   # Eraser tool (2.png)
    r"images\3.png",   # Calculator button (3.png)s
    r"images\4.png",   # Pen color toggle button (4.png)
    r"images\6.png"    # Next button (6.png)
]

# Create tool buttons with commands for Back and Next
back_button = create_tool_button(toolbar_box, tool_images[0], "back", previous_sheet)
pen_button = create_tool_button(toolbar_box, tool_images[1], "pen")
eraser_button = create_tool_button(toolbar_box, tool_images[2], "eraser")
calculator_button = create_tool_button(toolbar_box, tool_images[3], "calculator")
pen_color_button = create_tool_button(toolbar_box, tool_images[4], "pen_color")
next_button = create_tool_button(toolbar_box, tool_images[5], "next", next_sheet)

# Assign specific functionality to the buttons
pen_color_button.config(command=toggle_pen_color)
calculator_button.config(command=open_calculator)

# Load toggle image (same for both open and close states)
toggle_open_image = Image.open("images/toggle_open.png").resize((30, 30), Image.LANCZOS)
toggle_open_image_tk = ImageTk.PhotoImage(toggle_open_image)

# Button to toggle the visibility of the left section with images
toggle_button = Button(right_frame, image=toggle_open_image_tk, command=toggle_left_section, bg="#f5f5f5", relief="flat")
toggle_button.pack(pady=10, anchor='ne')  # Initially pack to top-right corner

# Left Section: Digital Text and Questions (previously right, now on the left)
left_frame = tk.Frame(window, bg="#f5f5f5", width=rhs_width)  # Set the width to 200
# Initially, pack the left_frame to make it visible
left_frame.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.N)

# Digital Text Area
tk.Label(left_frame, text="Digital Text", font=("Itim", 16), bg="#f5f5f5").pack(pady=10)
text_area = Text(left_frame, wrap=tk.WORD, font=("Itim", 12), height=12, bg="white", width=30)
text_area.pack(pady=10, padx=10, fill=tk.X)

# Left Section: Digital Text and Questions (continued)
tk.Label(left_frame, text="Questions", font=("Itim", 14), bg="#f5f5f5").pack(pady=20)

# Function to create question buttons
def create_question_buttons(section, start_num, parent):
    section_label = tk.Label(parent, text=f"Section {section}", font=("Itim", 12), bg="#f5f5f5")
    section_label.pack(pady=10)
    frame = tk.Frame(parent, bg="#f5f5f5")
    frame.pack(pady=10)
    for i in range(5):
        num = start_num + i
        btn = tk.Button(frame, text=f"{num}", font=("Itim", 12), bg="#a2d9e4", fg="white", width=4, height=2)
        btn.pack(side=tk.LEFT, padx=5)
# Bottom-Left Section for "Unattempted," "Answered," etc.
status_frame = tk.Frame(left_frame, bg="#f5f5f5")
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
