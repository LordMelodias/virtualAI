import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes



listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5)  # Increase the timeout for better recognition
            print('Recognizing...')
            command = listener.recognize_google(voice).lower()
            print('You said:', command)
            return command
    except sr.WaitTimeoutError:
        print('Listening timed out. Please try again.')
    except sr.UnknownValueError:
        print('Sorry, I did not hear your request. Please try again.')
    except sr.RequestError:
        print('Sorry, there was an issue with the request. Please check your internet connection.')
    except Exception as e:
        print(f"Error: {e}")
    
    return ""  # Return an empty string when an error occurs




def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        except wikipedia.DisambiguationError as e:
            print(f"Multiple results found. Please specify: {', '.join(e.options)}")
            talk("Sorry, I couldn't find information about that person.")
        except wikipedia.exceptions.PageError as e:
            print(f"Page not found: {e}")
            talk("Sorry, I couldn't find information about that person.")
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        talk("Sorry, I don't understand")

while True:
    run_alexa()
