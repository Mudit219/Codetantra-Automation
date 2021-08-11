# from testing_codetantra import COURSE
from selenium import webdriver
import pages
from dotenv import load_dotenv
import os
import datetime
from os.path import join

class platform_access:
    live=False

    def __init__(self,PATH,URL,COURSE,session='live'):
        if(PATH.find('chrome')!=-1):
            self.driver = webdriver.Chrome(PATH)
        else:
            self.driver = webdriver.Firefox(executable_path=PATH)
        self.URL = URL
        self.session = session
        self.COURSE = COURSE

    @staticmethod
    def get_credentials():
        dotenv_path = join(os.getcwd(),'.env')
        load_dotenv(dotenv_path)
        ID = os.getenv('LoginID')
        Password = os.getenv('Password')
        return (ID,Password)
    
    def get_date(self):
        if(self.session == 'live'):
            MONTH = datetime.date.today().strftime('%b')
            DAY = str(int(datetime.date.today().day))
            YEAR = datetime.date.today().year
            
        else:
            DAY, MONTH, YEAR = self.session.split('-')
            DAY = str(int(DAY))
            YEAR = int(YEAR)
        return (DAY,MONTH,YEAR)

    
    def open_url(self):
        url_req = 0
        try:
            self.driver.get(self.URL)
            self.driver.maximize_window()
            url_req = 1
        except:
            print("Couldn't connect to the internet")
        return url_req

    def attend(self):
        # print("hello world_1")
        # url_req = self.driver.get(self.URL)
        # # print("hello world_2")
        # self.driver.maximize_window()
        # print(*self.get_credentials())
        pages.loginPage(self.driver).set_credentials(*self.get_credentials())
        self.driver.implicitly_wait(20)
        pages.dashboardPage(self.driver).goto_meetings()
        self.driver.implicitly_wait(20)
        pages.timetablePage(self.driver).goto_calender(*self.get_date())
        self.driver.implicitly_wait(20)
        pages.timetablePage(self.driver).courseSlot(self.COURSE)
        self.driver.implicitly_wait(20)
        if(self.session=='live'):
            pages.timetablePage(self.driver).joinSession()
            print("Session is live.....")
            self.driver.implicitly_wait(20)
            self.live = True
            try:
                pages.live_session_options(self.driver).join_audio()
                print("Audio joined")
            except:
                print("Couldn't Join the audio")
        else: 
            try:
                pages.timetablePage(self.driver).playRecording()
            except:
                print("Recording is not available yet")
    
    def live_actions(self):
        pages.live_session_options(self.driver).mark_poll()
        # print(driver.page_source)
    def get_course(self):
        return self.COURSE
    
    def close_session(self):
        self.driver.quit()
