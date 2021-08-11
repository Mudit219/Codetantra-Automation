import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class BasePage:
    def __init__(self,driver):
        self.driver = driver

class loginPage(BasePage):

    def set_credentials(self,ID,Password):
        login_id = self.driver.find_element_by_id('loginId')
        login_id.send_keys(ID)
        password = self.driver.find_element_by_id('password')
        password.send_keys(Password)
        # login_id.send_keys(Keys.RETURN)
        submit = self.driver.find_element_by_id('loginBtn')
        ActionChains(self.driver).move_to_element(submit).click(submit).perform()
    
    
class dashboardPage(BasePage):
    
    def goto_meetings(self):
        meetings = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.ID,'homeCenterDiv'))
        )
        # Here I find out that we have many classes, so instead I seached for the tage name.
        meetings = meetings.find_element_by_tag_name('a')
        ActionChains(self.driver).move_to_element(meetings).click(meetings).perform()
    

class timetablePage(BasePage):

    def goto_calender(self,DAY,MONTH,YEAR):
        sidepanel = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.ID,'datepick'))
        )
        calendar = sidepanel.find_element(By.CLASS_NAME,value='datepicker-switch')
        action1 = ActionChains(self.driver)
        action1.click(calendar)
        action1.perform()

        year_element = sidepanel.find_element_by_class_name('datepicker-months')
        year_element = year_element.find_element_by_tag_name('thead')
        current_year = year_element.find_element(By.CLASS_NAME,value='datepicker-switch').get_attribute('innerText')
        year_req = year_element.find_element(By.CLASS_NAME,value='datepicker-switch')
        for _ in range(abs(int(current_year) - YEAR)):
            if((int(current_year)-YEAR)>=0):
                prev_year = year_element.find_element_by_class_name('prev')
                ActionChains(self.driver).move_to_element(prev_year).click(prev_year).perform()
                self.driver.implicitly_wait(5)
                year_req = year_element.find_element(By.CLASS_NAME,value='datepicker-switch')
                break
        print(year_req.get_attribute('innerText'))

        month_element = sidepanel.find_element_by_class_name('datepicker-months')
        month_element = month_element.find_element_by_tag_name('tbody')
        months = month_element.find_elements(By.TAG_NAME,value='span')
        mon_req = None
        for mon in months:
            if(mon.get_attribute('innerText')==MONTH):
                mon_req = mon
        print(mon_req.get_attribute('innerText'))
        # Some text are not visible with simple .text attribute, therefore use this method
        ActionChains(self.driver).move_to_element(mon_req).click(mon_req).perform()

        day_element = sidepanel.find_element_by_tag_name('tbody')
        days = day_element.find_elements(By.CLASS_NAME,value='day')
        day_req = None
        for day in days:
            if(day.get_attribute('innerText') == DAY and day.get_attribute('class') == 'day'):
                day_req = day
        print(day_req.get_attribute('innerText'))
        ActionChains(self.driver).move_to_element(day_req).click(day_req).perform()

    def courseSlot(self,COURSE):
        time_slots = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.ID,'calendar'))
        )
        time_slots = time_slots.find_element_by_class_name('fc-view-container')
        time_slots = time_slots.find_element_by_tag_name('tbody')
        time_slots = time_slots.find_element_by_class_name('fc-content-skeleton')
        time_slots = time_slots.find_elements(By.TAG_NAME,value='a')
        for slot in time_slots:
            if(slot.get_attribute('title') == COURSE[0]):
                # print(f"THis is the time {slot.find_element_by_class_name('fc-time').get_attribute('data-start')}")
                ActionChains(self.driver).move_to_element(slot).click(slot).perform()
                break
        print(f'Attending {COURSE[0]} at {COURSE[1]}')

    def playRecording(self):
        session_link = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.ID,'recordingStatusText'))
        )
        session_link = session_link.find_element_by_class_name('text-success')
        print(session_link.get_attribute('href'))
        session_link.click()
        # ActionChains(self.driver).move_to_element(session_link).click(session_link)
        print('Playing Recorded')
    
    def joinSession(self):
        session_link = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.ID,'meetingSummary'))
        )
        # session_link = session_link.find_element_by_class_name('col-12 col-md-4 my-1')
        session_link = session_link.find_element_by_tag_name('a')
        print(session_link.get_attribute('href'))
        session_link.click()
        # session_link.send_keys(Keys.ESCAPE)
        self.driver.implicitly_wait(5)
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        # print('Session is live.......')

    
class live_session_options(BasePage):

    def join_audio(self):
        self.driver.switch_to.frame('frame')
        audio_listn = self.driver.find_element_by_class_name('animationsEnabled')
        audio_listn = audio_listn.find_element_by_class_name('portal--27FHYi')
        audio_listn = audio_listn.find_element_by_class_name('content--IVOUy')
        audio_listn = audio_listn.find_element_by_tag_name('span')
        audio_listn = audio_listn.find_elements_by_tag_name('button')
        audio_button = None
        for b in audio_listn:
            if(b.get_attribute('aria-label')=='Listen only'):
                audio_button = b
                # print('Hello')
                break
        audio_button = audio_button.find_element_by_tag_name('span')
        ActionChains(self.driver).move_to_element(audio_button).click(audio_button).perform()
        self.driver.switch_to.default_content()
    
    def mark_poll(self):
        self.driver.switch_to.frame('frame')
        polls = self.driver.find_element_by_id('app')
        try:
            polls = polls.find_element_by_class_name('overlay--Arkp5')
            polls = polls.find_elements_by_tag_name('button')
            my_poll = None
            for b in polls:
                if(b.get_attribute('aria-label')=='A'):
                    my_poll = b
                    break
            if(my_poll!=None):
                print(my_poll)
            my_poll = my_poll.find_element_by_id('pollAnswerDescA')
            ActionChains(self.driver).move_to_element(my_poll).click(my_poll).perform()
            
        except:
            pass
        self.driver.switch_to.default_content()