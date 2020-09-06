# START OF CODE
# Written by Aryan Sahel and Ethan Clarke:) last updated September 5, 2020.
# Virtual Assistant.py ©

# This is the code for a simple chatbot/virtual assistant. It is currently capable of:
# 1. Responding to courtesies.
# 2. Displaying the date and time.
# 3. Performing searches on wikipedia.
# 4. Performing google searches.
# 5. Displaying stock market data.
# 6. Setting a timer.
# 7. Setting an alarm.
# 8. Sending a text message.
# 9. Sending a message on whatsapp.
# 10. Translating a text.


#TODO
# FEAT 1. create bailout function accessible at any time that restarts/accelerates bot
#      2. automatically determine if text or speech input is to be taken
#      3. simplify/combine else and exceptions in main while loop




# THINGS TO ADD:
# 1. Weather report
# 2. Play music on spotify
# 3. Better UI 

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

#Used to switch between different values of time
import time

# Used for timer/alarm beeping
import winsound

#Used for sending messages
import smtplib

#Used for sending a whatsapp message
import pywhatkit

#Used for analysing stocks
import yfinance as yf

#Used for plotting the data as a graph
import matplotlib.pyplot as plt

#Used to hide the password entered by the user for security purposes
import getpass

#Used for translating the text in the language translator function
from googletrans import Translator

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

#Startup instructions.
print()
print("Virtual Assistant is running...")
print()
print("Let's log you in!")
name = input("Please enter your name: ")
email = input("Please enter your gmail account: ")
#The password will be hidden for maximum secrecy.
password = getpass.getpass("Please enter your password: ")
print("You're all set to go!")

# Initialize the recognizer for microphone.
r = sr.Recognizer()

# A dictionary containing common greetings as keys and their responses as values.
common_greetings = dict(hello="Hello, My name is BlueBelle and I am your virtual assistant.",
                        origin="I was hidden in the crypts of the human brain until Linwood Computers Inc. brought me to life.",
                        health="I am doing very well, how about yourself?",
                        wiki="What would you like me to search for you today?",
                        timer="How many seconds would you like to set a timer for?",
                        alarm="When would you like to set an alarm for?",
                        number = "Please enter the number of the person you would like to message along with the country code",
                        carrier = "Please enter the receiver's carrier",
                        text_msg = "What message would you like to send?",
                        msg_time = "Please enter the time when you would like to send the message",
                        google = "What do you want to search for on the web?",
                        stock = "What company would you like to analyse?",
                        translate = "What would you like to translate?")

#A dictionary containing a list of domain names for canadian network providers.
provider_list = dict(bell = "@txt.bell.ca",
                     fido = "@fido.ca",
                     freedom = "@txt.freedommobile.ca",
                     koodo = "@msg.telus.com",
                     rogers = "@pcs.rogers.com",
                     telus = "@msg.telus.com")

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

#Function to carry out a search on google.
def google_search():
    response("google")

    #Variable to hold the user's input.
    g_search = input("Search: ")

    #Function imported from pywhatkit that carries out the search.
    pywhatkit.search(g_search)
    
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

def stock_data():
    response("stock")
    
    #Variable to hold company stock symbol.
    tickerSymbol = input("Enter the symbol for the company: ")

    #Variables to hold start and end date of the analysis
    start_date = input("Enter the start date: ")
    end_date = input("Enter the end date: ")

    #Function to obtain the stck market data
    data = yf.download(tickerSymbol, start_date, end_date)

    #Functions to plot the data as a graph
    data.Close.plot()
    plt.show()

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
    
def language_translator():
    #Object having constructor properties.
    translator = Translator()

    #Storing the text to be translated.
    response("translate")
    text  = input("Enter text here ")

    #Storing the destination language.
    response("Please enter the language to which you would like to translate")
    destination = input("Enter language here: ").lower()

    try:
        #Storing the translated raw code in a variable.
        translated = translator.translate(text, dest = destination)

        #Printing the meaningful part of the translated text.
        print(translated.text)
        #Printing and saying the pronunciation out loud.
        response(translated.pronunciation)
        print(translated.pronunciation)
    except ValueError:
        print("Please enter a valid language.")

def send_message():
    response("number")
    num = input("Enter number: ")

    response("carrier")
    provider = input("Enter carrier: ").lower()
    
    response("text_msg")
    message = input("Enter message: ")

    #Establishes an imap with gmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    #Logs the user into their gmail account
    server.login(email, password)

    #Used to send the message
    server.sendmail( name, num + provider_list.get(provider), message)

    print("Message sent successfully!")

def whatsapp():
    response("number")
    num = input("Enter number: ")

    response("text_msg")
    wapp_message = input("Enter message: ")

    response("msg_time")

    #We have to placeholders for time i.e. hour and minute.
    #This is because the pywhatkit.sendwhatmsg function needs them as separate arguments.
    msg_hour = int(input("Enter time hour in 24h format: "))
    msg_min = int(input("Enter time minute: "))

    #Used to send whatsapp message at the deisgnated time
    pywhatkit.sendwhatmsg(num, wapp_message, msg_hour, msg_min)

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

            elif MyText == "i want to search for something on wikipedia" or MyText == "4":
                wiki_search()

            elif MyText == "i want to set a timer" or MyText == "5":
                timer_setup()

            elif MyText == "i want to set an alarm" or MyText == "6":
                alarm_setup()
            
            elif MyText == "i want to send a message" or MyText == "7":
                send_message()
            
            elif MyText == "i want to send a whatsapp message" or MyText == "8":
                whatsapp()
            
            elif MyText == "i want to search for something" or MyText == "9":
                google_search()
            
            elif MyText == "i want to analyse stocks" or MyText == "10":
                stock_data()

            elif MyText == "i want to translate some text" or MyText == "11":
                language_translator()

            else:
                response("Sorry I don't understand.")

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        response("Request is unavailable.")

    except sr.UnknownValueError:
        response("I'm not sure I understand.")

# END OF CODE.
