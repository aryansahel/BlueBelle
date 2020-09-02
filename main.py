# START OF CODE
# Written by Aryan Sahel and Ethan Clarke:) last updated August 20, 2020.
# Virtual Assistant.py ©

# This is the code for a simple chatbot/virtual assistant. It is currently capable of:
# 1. Responding to courtesies.
# 2. Displaying the date and time.
# 3. Performing searches on wikipedia

#TODO
# FEAT 1. create bailout function accessible at any time that restarts/accelerates bot
#      2. automatically determine if text or speech input is to be taken
#      3. simplify/combine else and exceptions in main while loop




# THINGS TO ADD:
# 1. Ability to send texts
# 2. Ability to dial a number

# Bug fixes
# To remove "no parser explicitly specified" warning
# Find similar path to C:\Users\Ethan\PycharmProjects\assistant\venv\Lib\site-packages\wikipedia
# Replace lis = BeautifulSoup(html).find_all('li')
# With lis = BeautifulSoup(html, "html.parser").find_all('li')
#
# To get proper wikipedia search ie not getting "honey" when searching "donkey"
# Replace result = wikipedia.summary(search, sentences)
# With result = wikipedia.summary(search, sentences, auto_suggest=False)




# This class helps to obtain the current date
from datetime import date, datetime

# This carries out searches on wikipedia when prompted by the user
import wikipedia

# This converts text to speech
import pyttsx3

# This allows the human-computer interaction by detecting the microphone and spaker in the machine
import speech_recognition as sr

# Enables timer
import threading

import time

# Used for timer/alarm beeping
import winsound

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
                        timer="How many seconds would you like to set a timer for?",
                        alarm="When would you like to set an alarm for?")

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
        result = wikipedia.summary(search, sentences, auto_suggest=False)
        response(result)
    except wikipedia.DisambiguationError:
        response("Sorry, you need to be more specific.")
    except wikipedia.HTTPTimeoutError:
        response("Sorry, I could not connect to the internet.")
    except wikipedia.PageError:
        response("Sorry, I could not find what you were looking for.")
    except wikipedia.RedirectError:
        response("Sorry, I have been redirected while searching")
    except wikipedia.WikipediaException:
        response("Sorry, I have encountered an exception while searching")

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

# Function to output a message at the end of the timer and make a beeping noise
def end_time():
    print("\n\n" + "-"*100 + "\nTIMER\nTimes up! The timer has finished. Please feel free to continue with your task.\n" + "-"*100 + "\n\n")
    for i in range(5):
        time.sleep(0.06)
        winsound.Beep(700, 100)

# Function to set an alarm
def alarm_setup():
    response("alarm")
    # Getting current time
    now = datetime.now()
    cur_time = now.strftime("%H:%M:%S")
    # Getting time user wants alarm to go off at
    in_time = input("Currently the time is " + str(cur_time) + ", Alarm: ")
    try:
        # See function descriptions for explanation
        cur_time = time_parseer(cur_time)
        cur_time = hours_to_seconds(cur_time[0], cur_time[1], cur_time[2])
        out_time = time_parseer(in_time)
        out_time = hours_to_seconds(out_time[0], out_time[1], out_time[2])
        # Amount of time in seconds until alarm goes off
        length = abs(out_time - cur_time)
        length_disp = seconds_to_hours(length)
        # Gives time until alarm goes off
        print(str(length_disp[0]) + ":" + str(length_disp[1]) + ":" + str(length_disp[2]), "until the alarm ends.")
        # Start countdown till alarm goes off
        timer = threading.Timer(length, end_alarm)
        timer.start()
    except ValueError:
        response("Sorry, that's not a valid time.")

# Function to convert from S to [H,M,S]
def seconds_to_hours(seconds):
    seconds %= (24 * 60 * 60)
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return hours, minutes, seconds

# Function to convert from [H,M,S] to S
def hours_to_seconds(hours, minutes, seconds):
    seconds = seconds + (minutes * 60) + (hours * 24 * 60)
    return seconds

# Function to convert time from H:M:S format to [H,M,S]
def time_parseer(given_time):
    hours = int(given_time[0:2])
    minutes = int(given_time[3:5])
    seconds = int(given_time[6:8])
    return hours, minutes, seconds

# Function to output a message at the end of the timer and make a beeping noise
def end_alarm():
    print("\n\n" + "-"*100 + "\nALARM\nTimes up! The alarm has finished. Please feel free to continue with your task.\n" + "-"*100 + "\n\n")
    for i in range(5):
        time.sleep(0.06)
        winsound.Beep(800, 100)

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

            elif MyText == "i want to set an alarm" or MyText == "6":
                alarm_setup()

            else:
                response("Sorry I don't understand.")

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        # SpeakText("Request is unavailable.")

    except sr.UnknownValueError:
        response("I'm not sure I understand.")
        # SpeakText("I'm not sure I understand.")

# END OF CODE.
