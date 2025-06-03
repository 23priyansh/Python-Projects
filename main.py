
# it is incomplete because gemini is not supporting in this and api is exhausted.

# error - Gemini error: 404 models/gemini-pro is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.


# jarvis

import speech_recognition as sr
import webbrowser
import pyttsx3                                    # text to speech
import musicLibrary
import requests
import google.generativeai as genai                # Gemini API

# pip install pocketsphinx

recognizer = sr.Recognizer()                      # To recognize speech from audio
engine = pyttsx3.init()                           # Initialize pyttsx3 for text to speech

newsapi = "37f467ba4174437987dc24db90d4e718"              # API key

# Configure Gemini
genai.configure(api_key="")    # Replace with your Gemini API key

def speak(text):                                  # Function to convert text to speech
    engine.say(text)
    engine.runAndWait()

def processcommand(c):                            # Function to handle recognized commands
    print("Command received:", c)
    # Add more commands here
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open facebook" in c.lower():
        speak("Opening facebook")
        webbrowser.open("https://www.facebook.com")

    elif "open youtube" in c.lower():
        speak("Opening youtube")
        webbrowser.open("https://www.youtube.com")

    elif "open linkedin" in c.lower():
        speak("Opening linkedin")
        webbrowser.open("https://www.linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song] 
        webbrowser.open(link)  

    elif "news" in c.lower(): 
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")

        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])

            if articles:
                speak("Here are the top headlines")
                for article in articles[:5]: 
                    speak(article['title'])
            else:
                speak("Sorry, I could not find any news.")

    else:
        # If the command is not recognized, send it to Gemini
        try:
            speak("Let me think about it.")
            model = genai.GenerativeModel('gemini-pro')
            gemini_response = model.generate_content(c)
            answer = gemini_response.text
            print("Gemini says:", answer)
            speak(answer)
        except Exception as e:
            print("Gemini error:", e)
            speak("Sorry, I couldn't find an answer.")

# This should NOT be inside processcommand function, so no indentation here:
if __name__ == "__main__":

    speak("Initializing Jarvis...")

    while True:
        # listen for the wake word "jarvis"
        # obtain audio from the microphone

        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening for jarvis word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes, I am listening")
                
                with sr.Microphone() as source:
                    print("Jarvis is active...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)

                    processcommand(command)

        except Exception as e:
            print("Error: {0}".format(e))
