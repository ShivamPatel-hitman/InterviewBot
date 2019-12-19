from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from answer_processing import assess_answer
from kivy.graphics.texture import Texture
#from keras.models import load_model
from kivy.clock import Clock
import mysql.connector
from keras.preprocessing.image import img_to_array
from answer_processing import assess_answer
import speech_recognition as sr
import pyttsx3 as py
import numpy as np
import time
import random
import cv2

mydb = mysql.connector.connect(host="database-questions.cuto4xre5w7k.ap-south-1.rds.amazonaws.com",user="admin",passwd="shivam123",auth_plugin='mysql_native_password',database='Mydb')
mycursor = mydb.cursor()

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '500')
Config.write()

class Time (Label):
    def update(self,text):
        self.text = time.strftime('%H:%M:%S')
        self.engine = py.init()
        self.engine.setProperty('rate',160)
        self.engine.say(str(text))
        self.engine.runAndWait()
        self.engine.stop()
class Intro(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.namel = Label(size_hint=(0.5,0.55),pos_hint={'x':0,'y':0.5})
        self.namel.text = 'Enter Your Name : '
        self.add_widget(self.namel)
        self.el = Label(size_hint=(0.5,0.55),pos_hint={'x':0,'y':0.1})
        self.el.text = 'Enter Your Email : '
        self.add_widget(self.el)
        
        self.name = TextInput(size_hint=(0.5,0.5),pos_hint={'x':0.5,'y':0.5})
        self.add_widget(self.name)
        self.email = TextInput(size_hint=(0.5,0.55),pos_hint={'x':0.5,'y':0})
        self.add_widget(self.email)
        
        self.btn_click = Button(text='Start',size_hint=(1,0.1))
        #self.message = 'Hello welcome to interview'
        self.btn_click.bind(on_press = self.transit)
        #self.add_widget(self.message)
        self.add_widget(self.btn_click)
        self.lbl = Label(size_hint=(0.48,1),pos_hint={'x':0.5,'top':1})
        print('before text')
        #self.lbl.text = 'Hello {0}, Welcome to interview'.format(self.name.text)
        print(self.name.text)
        self.add_widget(self.lbl)
         #replace here
        

    def up(self,_):
        self.engine = py.init()
        self.engine.setProperty('rate',160)
        self.engine.say('Hello welcome to interview')
        self.engine.runAndWait()
        self.engine.stop()
    

    def transit(self,isinstance):
        self.engine = py.init()
        self.engine.setProperty('rate',160)
        self.engine.say('Hello {0},  welcome to interview'.format(self.name.text))
        self.engine.runAndWait()
        self.engine.stop()
        app.screen_manager.current = 'info'
    
            

class Startpage(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.img=Image(size_hint=(0.5,0.8),pos_hint={'x':0,'y':0.4})
        self.txt = TextInput(size_hint=(0.48,1),pos_hint={'x':0.5,'top':1})

        self.first = True

        self.tx2 = Label(size_hint=(0.5,0.5),pos_hint={'x':0,'y':0.01})
        self.lbl = Label(size_hint=(0.48,1),pos_hint={'x':0.5,'top':1})
        #self.lbl.text = 'Hello world this is shivam patel'
        #self.label(self.lbl,'Hello world this is shivam')
        self.add_widget(self.img)
        self.add_widget(self.lbl)
        #self.add_widget(self.txt)
        self.add_widget(self.tx2)
        
        mycursor.execute('select * from codes')
        q = mycursor.fetchall()
        self.paths = []
        self.statements = []
        self.answers = []
        for i in q:
            self.paths.append(i[0])
            self.statements.append(i[1])
            self.answers.append(i[2])
        mycursor.execute('select count(path) from codes')
        num_codes = mycursor.fetchone()
        self.num_codes = [i for i in range(0,num_codes[0])]


        #self.code=Image(size_hint=(0.48,1),pos_hint={'x':0.5,'top':1})
        #self.code.source = 'E:\\Facial-Expression-Detection-master\\master.png'
        
        #self.add_widget(self.code)
        
        self.total_marks =0
        self.marks = 0
        self.r = sr.Recognizer()
        
        #self.code = False
        
        self.btn = (Button(text= "Answer",size_hint= (0.1,0.1),pos_hint= {'right':1}))
        self.btn.bind(on_press = self.verify)
        #self.btn.bind(on_press = self.label)
        
        self.add_widget(self.btn)
        #self.weakness= []
        self.btn_listen = (Button(text='Listen',size_hint= (0.1,0.1),pos_hint= {'left':1}))
        self.btn_listen.bind(on_press = self.listen)
        self.add_widget(self.btn_listen)
        
        self.txt = TextInput(size_hint= (0.8,0.1),pos_hint={'x':0.1,'y':0,'down':1})
        self.add_widget(self.txt)
        self.qcount = 0
        self.count = 0
        self.a = ''
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)
        self.mode = 'none'
        self.path = 'E:\\interview_bot\\FaceDetection-master\\haarcascade_frontalface_default.xml'
        self.i = 0
        self.code=Image(size_hint=(0.48,1),pos_hint={'x':0.5,'top':1})
        #self.add_widget(self.code)
        
        #self.emotion_classifier = load_model('C:\\Users\\Shivam Patel\\Downloads\\_mini_XCEPTION.102-0.66.hdf5', compile=False)
        #self.EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised","neutral"]
        
        self.faceClass = cv2.CascadeClassifier(self.path)
        
        
        mycursor.execute('SELECT count(Q) FROM Questions')
        total_ques = mycursor.fetchone()
        self.num_hr = [i for i in range(1,total_ques[0])]
        print(self.num_hr)
        
        self.run1()
        #layout = FloatLayout(size=(800,500))

    # def say(self,to_say):
    #     self.engine.setProperty('rate',160)
    #     self.lbl.text = to_say
    #     self.engine.say('  '+to_say)
        
    #     self.engine.runAndWait()
    #     self.engine.stop()
    def update_label(self,text):
        self.text = time.strftime('%H:%M:%S')
        self.engine = py.init()
        self.engine.setProperty('rate',160)
        self.engine.say(self.q)
        self.engine.runAndWait()
        self.engine.stop()

    def say(self,to_say):
        self.lbl.text = to_say
        self.engine = py.init()
        self.engine.setProperty('rate',160)
        self.engine.say('  '+to_say)
        self.engine.runAndWait()
        self.engine.stop()
    
    def change_label(self,text_label):
        #self.say('click')
        self.lbl.text = str(text_label)
        #time = Time()
        Clock.schedule_once(self.update_label, 1) #replace here
        
    def change_label_code(self,text_label):
        #self.say('click')
        self.tx2.text = str(text_label)
        #time = Time()
        Clock.schedule_once(self.update_label_code, 1) #replace here

    def update_label_code(self,text):
        self.text = time.strftime('%H:%M:%S')
        self.engine = py.init()
        self.engine.setProperty('rate',160)
        self.engine.say(self.tx2.text)
        self.engine.runAndWait()
        self.engine.stop()

    


    def verify(self,isinstance):
        if self.count>5 and self.count<7:
            ans = self.txt.text
            #ans = self.audio_ans
            print(ans)
            print(self.q)
            #self.marks = assess_answer(self.a,ans)
            self.marks = 1
            self.lock = True
            if self.marks<1:
                #self.weakness.append(self.q)
                pass
            self.total_marks += self.marks
            print(self.marks)
            self.run1()
        elif self.count<=5:
            self.run1()
        else:
            ans = self.txt.text
            if ans == self.answers[self.i]:
                print('correct')
            print(self.answers[self.i])
            print(ans)
            
            self.run1()
    
    def listen(self,isinstance):
        print('say now')
        if self.count <= 5:
            with sr.Microphone() as source:
                audio = self.r.listen(source,timeout=2,phrase_time_limit=10)
                user_input = self.r.recognize_google(audio)
            print(user_input)
        
        elif self.count>5 and self.count<9:
            with sr.Microphone() as source:
                audio = self.r.listen(source,timeout=2,phrase_time_limit=3)
                user_input = self.r.recognize_google(audio)
            print(user_input)
            self.marks = assess_answer(self.a,user_input)
            self.total_marks += self.marks
            print(self.marks)
        else:
            print('You better write down answer')
        

        
        if self.count>=15:
            self.quit(self.total_marks)
        else:
            self.run1()

    def fetch(self):
        if self.count <=5:

            self.count +=1 
            i = random.choice(self.num_hr)
            print(len(self.num_hr))
            self.num_hr.remove(i)
            mycursor.execute('SELECT Q FROM Questions WHERE id={0}'.format(i))
            question = mycursor.fetchone()
            #self.count += 1
            #self.say(question[0])
            return question[0]
            #return 'hello'
        else:
            self.mode = 'TECH'
            return 'good'

    def fetch_tech(self):
        self.count+=1
        return 'are you there?','yes'
        

    def fetch_code(self):
        self.code=Image(size_hint=(0.48,1),pos_hint={'x':0.5,'top':1})
        if len(self.num_codes)!=0:
            self.i = random.choice(self.num_codes)
            self.num_codes.remove(self.i)
            self.lbl.text = ' '
            self.code.source = self.paths[self.i]
            print(self.paths[self.i])
            self.ans = self.answers[self.i]
            self.tx2.text = self.statements[self.i]
            self.count += 1
            self.first = False
            self.change_label_code(self.statements[self.i])
        self.add_widget(self.code)
        
    

    def run1(self):
        print('Run')
        if self.count<=5:
            if self.count!=0:
                self.q = self.fetch()
                # put change label function here
                # self.lbl.text = self.q
                self.change_label(self.q)
            else:
                self.q = self.fetch()
                self.lbl.text = str(self.q)
                
        

        elif self.count > 5 and self.count <= 7:
            #self.mode = 'Code'
            self.q,self.a  = self.fetch_tech()
                
        else:
            #self.q,self.a = self.fetch_code(
            if self.first:
                self.fetch_code()
            else:
                self.remove_widget(self.code)
                self.fetch_code()
            


    # def disp_text(self,disp):
    #     self.lbl.text = disp
    #     self.lock = False


    def quit(self,marks):
        #say('Wait while we assess your result')
        print('Quitting')
        if marks>10:
            self.lbl.text = 'you are pass'
            #self.say('You are selected')
        else:
            self.lbl.text = 'you are fail'
            #self.say('Better luck next time')
    
    def update(self, dt):
        
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        
        #cv2.imshow("CV2 Image", frame)
        # convert it to texture

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (48, 48))

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        
        self.faces = self.faceClass.detectMultiScale(frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(1,1),
        flags = cv2.CASCADE_SCALE_IMAGE
            )

        for (x, y, w, h) in self.faces:
            #print(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            img = frame[y:y + h, x:x + w]
            


        
        cv2.imshow('myapp',frame)
        
        #print('22')

        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img.texture = texture1





class NoApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.connect_page = Intro() 
        screen = Screen(name = 'startpage')
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.info_page = Startpage()
        #self.info_page.button1.bind(on_click=exit)
        screen = Screen(name = 'info')
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

app = NoApp()
app.run()


