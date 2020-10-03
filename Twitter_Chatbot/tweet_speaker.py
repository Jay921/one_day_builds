import os
import playsound
import time
import speech_recognition as sr
from gtts import gTTS
import tweepy
import re

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said + '\n')
        except Exception as e:
            print("Exception: " + str(e) + '\n')
    
    return said.lower()



CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
ACCESS_KEY = 'YOUR_ACCESS_KEY'
ACCESS_SECRET = 'YOUR_ACCESS_SECRET'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

home_page_tweets = api.home_timeline()

def get_tweet_text(text, rt_text):
    rest_text = re.sub(r'http\S+', ' (Link provided) ', text)
    rest_rt_text = re.sub(r'http\S+', ' (Link provided) ', rt_text)
    
    if text.startswith('RT'):
        retweet_user = re.findall(r'RT @\w+:', rest_text)[0]
        print('\n' + str(retweet_user) + '\n')
        return " Retweeted the post of " + str(retweet_user)[3:-1] + " saying: " + str(rest_rt_text)
    
    else:
        return " said: " + rest_text


WAKE = "hey ruby"

while True:

    print("Listening... Speak now > ")
    user_in_text = get_audio()

    if user_in_text.count(WAKE) > 0:

        if "hello" or "hi" or "g'day" or "hey" or "hey ruby" in user_in_text:
            print("Ruby is speaking > \n")
            speak("Hello, what would you like me to do?")

        print("Speak now > ")
        user_in_text = get_audio()

        if "tweets" in user_in_text:

            print("Ruby is speaking > \n")
            speak("Here are your most recent tweets")

            for i in range(len(home_page_tweets)):
                id_str = home_page_tweets[i].__dict__['id']
                status = api.get_status(id_str, tweet_mode = "extended") 
                full_text = status.full_text  
                rt_full_text = ""

                print('\n' + home_page_tweets[i].__dict__['author'].name + '\n')


                if full_text.startswith('RT'):
                    try:
                        rt_full_text = status.retweeted_status.full_text
                    except AttributeError:  # Not a Retweet
                        rt_full_text = status.full_text

                    print(rt_full_text + '\n')

                else:
                    print(full_text + '\n')

                speak(str(home_page_tweets[i].__dict__['author'].name) + get_tweet_text(full_text, rt_full_text))

                print('-'*200)

        if "stop listening" in user_in_text:
            speak("Ok, good bye")
            break
