from __future__ import print_function
import os.path
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from httplib2 import Http
import oauth2client
from oauth2client.client import OAuth2Credentials
import pyttsx3
import datetime as dt
import speech_recognition as SR 
import os
import re
import urllib.request
import pandas as pd
from pushbullet import Pushbullet
 




scopes = ['https://www.googleapis.com/auth/calendar']


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def getSpeech():
    r = SR.Recognizer()  
    with SR.Microphone() as source:
        print("Listening...")                                                                                       
        r.pause_threshold = 0.5
        r.energy_threshold = 200
        audio = r.listen(source) 

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in')   
        print(f"You said : {query}")
        

    except Exception as e:
        print(e)
        print("Can't hear")
        speak("Can't hear")
        return " "
    return query  

def getTomorrowRem(sen1, List1):
    dateTomm = dt.date.today() + dt.timedelta(days=1)
    temp = ""
    timestr = ""
    try:
      
        timeMatch = re.search(r'\d{2}:\d{2}', sen1)
        if timeMatch != None:

            timestr = timeMatch.group()
        else:
            timeMatch = re.search(r'\d{1}:\d{2}', sen1)
            timestr = timeMatch.group()
        
    except Exception as err:
        print("nothing found!")
    for amPm in List1:
        if amPm == "evening" or amPm == "afternoon" or amPm == "noon":
            temp = "PM"
        elif amPm == "pm" or amPm == "p.m." or amPm == "am" or amPm == "a.m.":
                        
            x = re.findall("[^.]", amPm)
            st = ''.join(x)
            print(st)
            temp = st.upper()
        else:
            temp = "AM"
    timeFinal = timestr + " " + temp                                                        
    in_time = dt.datetime.strptime(timeFinal, "%I:%M %p")
    out_time = dt.datetime.strftime(in_time, "%H:%M")
    dateFinal = dateTomm.strftime("%Y-%m-%d")
    datetimeFinal = dateFinal + "T" + out_time + ":00"
    return [datetimeFinal, dateFinal]

def getTodayRem(sen, List):
     dateTomm = dt.date.today()
     temp = ""
     timestr = ""
     try:
       
            timeMatch = re.search(r'\d{2}:\d{2}', sen)
            if timeMatch != None:
                timestr = timeMatch.group()
            else:
                timeMatch = re.search(r'\d{1}:\d{2}', sen)
                timestr = timeMatch.group()
         
     except Exception as err:
         print("nothing found!")
     for amPm in List:
         if amPm == "evening" or amPm == "afternoon" or amPm == "noon":
             temp = "PM"
         elif amPm == "pm" or amPm == "p.m." or amPm == "am" or amPm == "a.m.":
             x = re.findall("[^.]", amPm)
             st = ''.join(x)
             print(st)
             temp = st.upper()
         else:
            temp = "AM"
     timeFinal = timestr + " " + temp
     in_time = dt.datetime.strptime(timeFinal, "%I:%M %p")
     out_time = dt.datetime.strftime(in_time, "%H:%M")
     
     dateFinal = dateTomm.strftime("%Y-%m-%d")
     datetimeFinal = dateFinal+"T"+out_time+":00"
     return [datetimeFinal, dateFinal]

def getDayRem(sen2, dayF,List3):
    temp = ""
    timestr = ""
    try:
        timeMatch = re.search(r'\d{2}:\d{2}', sen2)
        if timeMatch != None:
            timestr = timeMatch.group()
        else:
            timeMatch = re.search(r'\d{1}:\d{2}', sen2)
            timestr = timeMatch.group()
         
    except Exception as err:
        print("nothing found!")
    for amPm in List3:
        if amPm == "evening" or amPm == "afternoon" or amPm == "noon":
            temp = "PM"
        elif amPm == "pm" or amPm == "p.m." or amPm == "am" or amPm == "a.m.":
            x = re.findall("[^.]", amPm)
            st = ''.join(x)
            print(st)
            temp = st.upper()
        elif amPm == "morning":
          temp = "AM"
    dict1 = {
            "sunday":0,
            "monday":1, 
            "tuesday":2, 
            "wednesday":3,
            "thursday":4, 
            "friday":5, 
            "saturday":6
            }
    reqDay = dict1[dayF]
    currDay = dt.datetime.today().weekday()
    dayDiff = ""
    if reqDay > currDay :
        dayDiff = (reqDay-currDay)-1
    else:
        dayDiff = (7-currDay)+reqDay
    dateTomm = dt.date.today() + dt.timedelta(days=dayDiff)
    dateFinal = dateTomm.strftime("%Y-%m-%d")
    timeFinal = timestr + " " + temp
    in_time = dt.datetime.strptime(timeFinal, "%I:%M %p")
    out_time = dt.datetime.strftime(in_time, "%H:%M")
    dateTimeFinal = dateFinal+"T"+out_time+":00"
   
       
    return [dateTimeFinal, dateFinal]


def getWhatsAppText():
    API_KEY = 'o.XFwX1wCRg5fBQbptpD96KPE8VEHL1zad'
    pb = Pushbullet(API_KEY)
    pushes = pb.get_pushes()
    latest = pushes[0]
    url = latest['file_url']
    file_path = "chat.txt"
    urllib.request.urlretrieve(url, file_path)
    # data cleanup
    with open(file_path, mode='r', encoding="utf8") as f:
        data = f.readlines()
    finalLen = len(data)
    initLen = finalLen-10
    preFinalList = data[initLen:finalLen]
    finalList = ""
    temp = []
    for item in preFinalList:
        temp = item.split(":")
      
        if len(temp)==4:
            finalList = finalList + (temp[1]+"-"+temp[2]+":"+temp[3])
        else:
            finalList = finalList + (temp[1]+"-"+temp[2])
                 
    return finalList


def setEvent(sen, dtfinal, dfinal, timezone):
    event = {
             'summary': sen,
             'location': 'None',
             'description': sentence,
             'start': {
             'dateTime': dtfinal,
             'timeZone': timezone,
                                 },
             'end': {
             'dateTime': dfinal + 'T' + '23:59:00',
             'timeZone': timezone,                    
              },
             'recurrence': [
             'RRULE:FREQ=DAILY;COUNT=2'
             ],
             'reminders': {
             'useDefault': False,
             'overrides': [
                 {'method': 'email', 'minutes': 24 * 60},
                 {'method': 'popup', 'minutes': 10},
             ],
            },
         }
    event = service.events().insert(calendarId=calendar_id, body=event).execute()     
    print(event.get('htmlLink'))
    print("Reminder set!")
  

                   
if __name__ == "__main__" :
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials = creds)
    print(creds)
    result = service.calendarList().list().execute()
    result['items'][0]
    calendar_id = result['items'][0]['id']
    timezone = 'Asia/Kolkata'
    print("Select mode of operation")
    print("1. WhatsApp Mode")
    print("2. Voice Mode")
    opt = int(input())
    while True:
        sentence = ""
        if opt == 1:
            temp = getWhatsAppText()
            sentence = temp.lower()
           
        else:
            sentence = getSpeech().lower()
           
        print(sentence)
        senList = sentence.split()
        print(senList)
        iftomm = 0
        day = ""
        print(senList)
        for item in senList:
            if item == "tomorrow":
                iftomm = 1

            elif item == "sunday" or item == "monday" or item == "tuesday" or item == "wednesday" or item == "thursday" or item == "friday" or item == "saturday":
                iftomm = 2
                day = item
        if iftomm == 1:
            retDateTomm = getTomorrowRem(sentence, senList)
            print(retDateTomm[0], end = ", ")
            print(retDateTomm[1])
            setEvent(sentence, retDateTomm[0], retDateTomm[1], timezone)
        elif iftomm == 2:
           
            retDateDay = getDayRem(sentence, day, senList)
            print(retDateDay[0], end = ", ")
            print(retDateDay[1])
            setEvent(sentence, retDateDay[0], retDateDay[1], timezone)
            
        else:
            retDateTod = getTodayRem(sentence,senList)
            print(retDateTod[0], end = ", ")
            print(retDateTod[1])
            setEvent(sentence, retDateTod[0], retDateTod[1], timezone)
        