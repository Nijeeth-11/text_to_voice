
from gtts import gTTS
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Define your passage (this is just an example)
passage = """In the early 21st century, rapid technological advancements have reshaped various industries, with artificial intelligence (AI) emerging as one of the most transformative forces. AI encompasses a wide range of applications, from machine learning to natural language processing, and it has the potential to revolutionize sectors such as healthcare, finance, and transportation. However, as AI continues to evolve, there are ethical concerns that must be addressed, including issues related to job displacement, privacy, and security.
"""

# Convert text to speech
tts = gTTS(text=passage, lang='en')
# Save the audio as an MP3 file
tts.save("output_audio.mp3")
'---------------------------------------------------------------------------'

import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Load the audio file
audio_file = "output_audio.mp3"

# Convert MP3 to WAV using pydub
from pydub import AudioSegment
audio = AudioSegment.from_mp3(audio_file)
audio.export("output_audio.wav", format="wav")

# Use speech recognition to transcribe the audio
with sr.AudioFile("output_audio.wav") as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)

print("Transcribed Text: ", text)

'---------------------------------------------------------------------------'

from transformers import pipeline

# Load summarization model from Hugging Face
summarizer = pipeline('summarization')

# Text from speech recognition
text = "The recognized text from the audio."

# Get the summary
summary = summarizer(text, max_length=100, min_length=50, do_sample=False)

print("Summary:", summary[0]['summary_text'])

import sqlite3

# Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect('summaries.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table to store summaries if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    summary TEXT
)
''')

# Insert the summary into the table
summary_text = passage
cursor.execute('INSERT INTO summaries (summary) VALUES (?)', (summary_text,))

# Commit the changes and close the connection
conn.commit()
conn.close()


