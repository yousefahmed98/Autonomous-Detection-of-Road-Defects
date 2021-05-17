import RPi.GPIO as GPIO 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
from datetime import datetime
from picamera import PiCamera
from time import sleep
import os
from google.cloud import firestore
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/home/pi/Desktop/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

firebaseConfig = {
    'apiKey': "AIzaSyC0HAuRhnM7bXrXlTD4mKZY7IY0bdlBRjs",
    'authDomain': "gosafe-b7649.firebaseapp.com",
    'databaseURL': "https://gosafe-b7649-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "gosafe-b7649",
    'storageBucket': "gosafe-b7649.appspot.com",
    'messagingSenderId': "381335317590",
    'appId': "1:381335317590:web:bbd65789a6da2b4a151ff7",
    'measurementId': "G-84SGS5XN40"

}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
storage = firebase.storage()
db = firestore.client()
email = "gosafe.roadissuesdetection@gmail.com"
password = "MLLYY@2020"
user = auth.sign_in_with_email_and_password(email,password)

camera = PiCamera()
class Issue(object):
    def __init__(self,imgUrl,geoPoint,type):
        self.imgUrl = imgUrl
        self.geoPoint = geoPoint
        self.type = type

while True: 
  try:
        #GPIO.output(2,1)
        print("pushed")
        now = datetime.now()
        dt = now.strftime("%d%m%Y%H:%M:%S")
        name = dt+".jpg"
        camera.capture(name)
        print(name+" saved")
        storage.child('images/'+name).put(name)
        print("Image sent")
        url = storage.child('images/'+name).get_url(user['idToken'])
        print(url)
        location=firestore.GeoPoint(33.2, 33.8)
        issue = {u'imgUrl':url,
                 u'geoPoint': location,
                 u'type': u'test2'
                 }
        db.collection(u'issues').add(issue)
        os.remove(name)
        print("File Removed")
        #GPIO.output(2,0)
        sleep(20)
	
	
  except:
        camera.close()