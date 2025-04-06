import tkinter as tk  
from tkinter import scrolledtext  
import openai  
import threading  
  
class ChatApp:  
   def __init__(self, root):  
      self.root = root  
      self.root.title("OpenAI Chat Application")  
      self.root.geometry("600x800")  
       
      # Replace with your OpenAI API key  
      openai.api_key = 'sk-abcdqrstefghuvwxabcdqrstefghuvwxabcdqrst'  
       
      # Create GUI elements  
      self.create_widgets()  
       
   def create_widgets(self):  
      # Chat display area  
      self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=30)  
      self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  
       
      # Input field  
      self.input_field = tk.Entry(self.root, width=50)  
      self.input_field.grid(row=1, column=0, padx=10, pady=10)  
       
      # Send button  
      self.send_button = tk.Button(self.root, text="Send", command=self.send_message)  
      self.send_button.grid(row=1, column=1, padx=10, pady=10)  
       
      # Bind Enter key to send message  
      self.input_field.bind("<Return>", lambda e: self.send_message())  
       
   def send_message(self):  
      user_message = self.input_field.get()  
      if user_message.strip() == "":  
        return  
          
      # Clear input field  
      self.input_field.delete(0, tk.END)  
       
      # Display user message  
      self.chat_display.insert(tk.END, f"You: {user_message}\n\n")  
       
      # Create a thread for API call  
      threading.Thread(target=self.get_ai_response, args=(user_message,)).start()  
       
   def get_ai_response(self, user_message):  
      try:  
        # Get response from OpenAI  
        response = openai.ChatCompletion.create(  
           model="gpt-3.5-turbo",  
           messages=[  
              {"role": "user", "content": user_message}  
           ]  
        )  
          
        ai_response = response.choices[0].message.content  
          
        # Display AI response  
        self.chat_display.insert(tk.END, f"AI: {ai_response}\n\n")  
          
        # Auto-scroll to bottom  
        self.chat_display.see(tk.END)  
          
      except Exception as e:  
        self.chat_display.insert(tk.END, f"Error: {str(e)}\n\n")  
        self.chat_display.see(tk.END)  
  
def main():  
   root = tk.Tk()  
   app = ChatApp(root)  
   root.mainloop()  
  
if __name__ == "__main__":  
   main()
