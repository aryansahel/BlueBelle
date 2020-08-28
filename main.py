# START OF CODE
# Written by Aryan Sahel and Ethan Clarke:) last updated August 20, 2020.
# Virtual Assistant.py ©

# This is the code for a simple chatbot/virtual assistant. It is currently capable of:
# 1. Responding to courtesies.
# 2. Displaying the date and time.
# 3. Performing searches on wikipedia

#TODO
# BUGS 1. if timer ends while bot is already speaking an error occurs
#      2. searching "donkey" returns "honey" from wikipedia, is there a way to double check/stop this error
# FEAT 1. create bailout function accessible at any time that restarts/accelerates bot
#      2. simplify exceptions in main try/excpetion thingy so we don't need an else statement
#      3. automatically determine if text or speech input is to be taken




# THINGS TO ADD:
# 1. Ability to send texts
# 2. Ability to dial a number
# 3. Ability to set a timer/alarm

# To remove "no parser explicitly specified" warning
# Find similar path to C:\Users\Ethan\PycharmProjects\assistant\venv\Lib\site-packages\wikipedia
# Repalce lis = BeautifulSoup(html).find_all('li')
# With lis = BeautifulSoup(html, "html.parser").find_all('li')




# This class helps to obtain the current date.
from datetime import date, datetime

# This carries out searches on wikipedia when prompted by the user.
import wikipedia

# This converts text to speech.
import pyttsx3

#This allows the human-computer interaction by detecting the microphone and spaker in the machine.
import speech_recognition as sr

# Enables timer
import threading

import time

# Defining a variable and assigning it today's date.
current_date = date.today()

# This assignment will give us the date in the format of "January 12, 2019"
date = current_date.strftime("%B %d, %Y")
print("\nThe date today is", date, ".")

# Same as for date, only this time it is gonna give us the time.
# Logic same as for obtaining date.
current_time = datetime.now()
time_set = current_time.strftime("%H:%M:%S")
print("The current time is", time_set, ".")
print("Virtual Assistant is running...")


# Initialize the recognizer for microphone.
r = sr.Recognizer()

# A dictionary contain common greetings as keys and their responses as values.
common_greetings = dict(hello="Hello, My name is BlueBelle and I am your virtual assistant.",
                        origin="I was hidden in the crypts of the human brain until Linwood Computers Inc. brought me to life.",
                        health="I am doing very well, how about yourself?",
                        wiki="What would you like me to search for you today?",
                        timer="How many seconds would you like to set a timer for?")

# Function sets up the microphone for communicating with the bot
def mic_setup():
    # use the microphone as source for input.
    with sr.Microphone() as source2:
        # wait for a second to let the recognizer adjust the energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source2, duration=0.2)

        # listens for the user's input
        audio1 = r.listen(source2)

        # Using google api to recognize audio
        MyText = r.recognize_google(audio1)
        return MyText

# Function to convert text to speech.

def speak_text(text):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to make the bot speak and write
def response(input):
    # The SpeakText function makes the computer say the results out loud.
    # It is from the pyttsx3 class.
    # It has been used all throughout the code to make the interactions possible.
    if input in common_greetings:
        print(common_greetings.get(input))
        speak_text(common_greetings.get(input))
    else:
        print(input)
        speak_text(input)

# Function to search on wikipedia
def wiki_search():
    response("wiki")

    # A new variable was required for the computer to wait for another response from the user.
    search = input("Search: ")
    search.lower()

    # Variable to hold the wikipedia result in. wikipedia.summary is an in-built function.
    # Allows wiki searches to display 4 sentences
    sentences = 4
    try:
        result = wikipedia.summary(search, sentences)
        response(result)
    except wikipedia.DisambiguationError:
        response("Sorry, you need to be more specific.")

# Function to output a message at the end of the timer
def end_time():
    response("Times up!")

# Function to set a timer
def timer_setup():
    response("timer")

    # Length of time to set timer for in seconds
    length = input("Timer: ")
    # Try to convert time from str to float
    # Exception if conversion invalid
    try:
        # Convert str to float
        length = float(length)
        # Set timer for a certain length of time that will execute end_time after
        timer = threading.Timer(length, end_time)
        timer.start()
    except ValueError:
        response("Sorry, that's not a valid time.")




# Loop infinitely for user to speak
while 1:

    # Try to take user input via text or voice
    # Exception if user input invalid
    try:
            print("\nType or say something:")
            #MyText =  mic_setup()
            MyText = input()
            MyText.lower()

            if MyText == "hello" or MyText == "hi" or MyText == "hey" or MyText == "1":
                response("hello")

            elif MyText == "how are you" or MyText == "how's it going" or MyText == "2":
                response("health")

            elif MyText == "where are you from" or MyText == "3":
                response("origin")

            elif MyText == "i want to search for something" or MyText == "4":
                wiki_search()

            elif MyText == "i want to set a timer" or MyText == "5":
                timer_setup()

            else:
                response("Sorry I don't understand.")

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        # SpeakText("Request is unavailable.")

    except sr.UnknownValueError:
        response("I'm not sure I understand.")
        # SpeakText("I'm not sure I understand.")

# END OF CODE.