import pyttsx3
from tkinter import *
from googletrans import Translator
from gtts import gTTS
import os
import requests

# Initialize pyttsx3 engine and translator
engine = pyttsx3.init()
translator = Translator()

# Function to convert text to speech
def text_to_speech():
    text = text_input.get("1.0", "end-1c")  # Get text from the text box
    if text.strip():  # Check if there's any text to convert
        engine.say(text)
        engine.runAndWait()

# Function to set male voice
def set_male_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Male voice
    status_label.config(text="Voice: Male")

# Function to set female voice
def set_female_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice
    status_label.config(text="Voice: Female")

# Function to translate and convert text to speech in Telugu
def translate_and_speak_telugu():
    text = text_input.get("1.0", "end-1c")
    if text.strip():
        translated_text = translator.translate(text, src="en", dest="te").text
        tts = gTTS(translated_text, lang="te")
        tts.save("telugu_audio.mp3")
        os.system("start telugu_audio.mp3")  # Play the audio
        status_label.config(text="Translated and Speaking in Telugu")

# Function to translate and convert text to speech in Hindi
def translate_and_speak_hindi():
    text = text_input.get("1.0", "end-1c")
    if text.strip():
        translated_text = translator.translate(text, src="en", dest="hi").text
        tts = gTTS(translated_text, lang="hi")
        tts.save("hindi_audio.mp3")
        os.system("start hindi_audio.mp3")  # Play the audio
        status_label.config(text="Translated and Speaking in Hindi")

# Function to fetch word meaning using Free Dictionary API
def get_word_meaning():
    word = text_input.get("1.0", "end-1c").strip()
    if word:
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            if response.status_code == 200:
                data = response.json()
                meanings = data[0]["meanings"]
                meaning_text = "\n".join([f"{item['partOfSpeech']}: {', '.join([d['definition'] for d in item['definitions']])}" for item in meanings])
            else:
                meaning_text = "Word not found in dictionary."
        except Exception as e:
            meaning_text = f"Error fetching meaning: {e}"
    else:
        meaning_text = "Please enter a word to find its meaning."

    # Display the meaning in a popup window
    meaning_window = Toplevel(root)
    meaning_window.title(f"Meaning of '{word}'")
    Label(meaning_window, text=meaning_text, wraplength=400, font=("Arial", 12)).pack(pady=10, padx=10)
    Button(meaning_window, text="Close", command=meaning_window.destroy, font=("Arial", 12), bg="red").pack(pady=5)

# Function to simulate fake news detection (Removed)
# def detect_fake_news():
#     ...

# Function to display a news block with fake news detection (Updated to reload news)
def display_news_block(title, points):
    news_block = Frame(news_frame, bg="lightgray", bd=2, relief=SOLID)
    news_block.pack(pady=10, padx=10, fill=BOTH, expand=True)

    # Title of the news block
    Label(news_block, text=title, font=("Arial", 16, "bold"), bg="lightgray").pack(pady=5)

    # Points of the news block
    points_frame = Frame(news_block, bg="lightgray")
    for point in points:
        Label(points_frame, text=point, font=("Arial", 12), bg="lightgray", anchor="w").pack(pady=3, padx=10)
    points_frame.pack(pady=10)

    # Update the status based on the news
    news_block.config(bg="green")  # Simulating that all news is real for now

# Function to reload the current affairs data (this can be expanded with actual API)
def reload_current_affairs():
    global news_data
    # For simplicity, we're using static data but this can be updated with an API call
    news_data = [
        ("Government announces new tax reforms", [
            "New tax brackets introduced.",
            "Special deductions for low-income groups.",
            "Details of implementation will be announced next week."
        ]),
        ("Major earthquake hits the city", [
            "Tremors felt across the region.",
            "Rescue teams deployed to affected areas.",
            "No casualties reported yet."
        ]),
        ("New study reveals health benefits of green tea", [
            "Studies show reduced risk of heart disease.",
            "Helps improve metabolism.",
            "Recommended for daily consumption."
        ])
    ]
    
    # Clear the previous news blocks
    for widget in news_frame.winfo_children():
        widget.destroy()
    
    # Display the updated news blocks
    for title, points in news_data:
        display_news_block(title, points)

# Sample current affairs news
news_data = [
    ("Government announces new tax reforms", [
        "New tax brackets introduced.",
        "Special deductions for low-income groups.",
        "Details of implementation will be announced next week."
    ]),
    ("Major earthquake hits the city", [
        "Tremors felt across the region.",
        "Rescue teams deployed to affected areas.",
        "No casualties reported yet."
    ]),
    ("New study reveals health benefits of green tea", [
        "Studies show reduced risk of heart disease.",
        "Helps improve metabolism.",
        "Recommended for daily consumption."
    ])
]

# Create a GUI window
root = Tk()
root.title("Text-to-Speech with Translation and Fake News Detection")
root.geometry("900x800")

# Create a main frame for the entire window layout
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True)

# Create a frame for the buttons (left side)
button_frame = Frame(main_frame, width=200, bg="lightgray", padx=10)
button_frame.pack(side=LEFT, fill=Y, padx=10)

# Create a frame for the news blocks (right side)
news_frame = Frame(main_frame, bg="white", padx=10)
news_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# Add a Label and Text Input Box inside the button frame
Label(button_frame, text="Enter Text Below:", font=("Arial", 14)).pack(pady=10)
text_input = Text(button_frame, wrap=WORD, width=30, height=10, font=("Arial", 12))
text_input.pack(pady=10)

# Add Buttons for Male and Female Voices
Button(button_frame, text="Male Voice", command=set_male_voice, font=("Arial", 12), bg="lightgreen").pack(pady=5)
Button(button_frame, text="Female Voice", command=set_female_voice, font=("Arial", 12), bg="lightpink").pack(pady=5)

# Add Buttons for Translation and TTS
Button(button_frame, text="Speak in Telugu", command=translate_and_speak_telugu, font=("Arial", 12), bg="lightblue").pack(pady=5)
Button(button_frame, text="Speak in Hindi", command=translate_and_speak_hindi, font=("Arial", 12), bg="lightyellow").pack(pady=5)

# Add a Button to trigger Text-to-Speech
Button(button_frame, text="Convert to Speech (English)", command=text_to_speech, font=("Arial", 12), bg="lightgray").pack(pady=10)

# Add a Button to fetch word meaning
Button(button_frame, text="Find Word Meaning", command=get_word_meaning, font=("Arial", 12), bg="lightcoral").pack(pady=10)

# Add a Button to reload current affairs
Button(button_frame, text="Reload Current Affairs", command=reload_current_affairs, font=("Arial", 12), bg="lightblue").pack(pady=10)

# Display initial sample news blocks
for title, points in news_data:
    display_news_block(title, points)

# Add a Status Label to indicate selected voice or action
status_label = Label(button_frame, text="Voice: Default", font=("Arial", 12), fg="blue")
status_label.pack(pady=10)

# Run the event loop
root.mainloop()