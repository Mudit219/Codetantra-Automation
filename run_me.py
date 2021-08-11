import codetantra
import schedule
import time
import concurrent.futures
import threading
import os
import datetime
from dotenv import load_dotenv


course_dict = {
    'OS':['EG 301 Operating Systems theory - Prof. B Thangaraju','09:30'],
    'OS_lab':['EG 301 Operating Systems Lab - Prof. B Thangaraju','16:00'],
    'PL':['CS305 Programming Languages - Prof. Sujit Kumar Chakrabarti','11:30'],
    'VR':['AI 825 Visual Recognition by Prof. Dinesh Babu Jayagopi & Prof. Viswanath G','11:30'],
    'NC1':['NC 824 Cyber Security Fundamentals with toolsand techniques for defense - Prof. Harish Ramani','09:30'],
    'NC2':['NC 824 Cyber Security Fundamentals with toolsand techniques for defense - Prof. Harish Ramani','11:30'],
    'NC3': ['NC 824 Cyber Security Fundamentals with toolsand techniques for defense by Prof. Mohanram C','01:36'],
    'CG1':['CS 606 Computer Graphics - Prof. Jaya Sreevalsan Nair','16:00'],
    'CG2':['CS 606 Computer Graphics - Prof. Srikanth T K & Prof. Jaya Sreevalsan Nair','14:00'],
    'HSS':['DT 219 Societal Platform Thinking - Prof. Ramesh Sundararaman','16:00'],
    'ST':['CS 731  Software Testing - Prof. Meenakshi D Souza','11:30'],
    'DV':['CSDS 732  Data Visualization - Prof. Jaya Sreevalsan Nair','09:30'],
    'SPM':['DT 311  Software Product Management - Haragopal Mangipudi','11:30'],
    'NSW':['AI 608  Network Science for the web - Prof. Srinath Srinivasa','13:30']
    }

dotenv_path = os.path.join(os.getcwd(),'.env')
load_dotenv(dotenv_path)        
PATH_CHROME = os.getenv('PATH_CHROME')
PATH_FIREFOX = os.getenv('PATH_FIREFOX')
URL = os.getenv('URL')

live_courses = []
live_threads = []

# Here I have declared the hold on function which makes the course object and start attending its session.
def hold_on(code,session):
    global live_courses
    c = codetantra.platform_access(PATH_CHROME,URL,COURSE=course_dict[code],session=session)
    if(c.open_url() == 0):
        c.close_session()
        print('Attempting to reconnect')
        hold_on(code,session)
    else:
        print("Internet Connection Established")
        live_courses.append(c)
        c.attend()

def hold_my_thread(code,session):
    global live_threads
    course_thread = threading.Thread(target=hold_on,args=(code,session))
    course_thread.start()
    live_threads.append(course_thread)

def scheduler(code,session_day,session_date="live"):
    if(session_date=="live"):
        # Waking PC from hiberante mode
        course_time=course_dict[code][1]
        wake_time=datetime.time(int(course_time.split(':')[0]),int(course_time.split(':')[1]))
        wake_time=datetime.datetime.combine(datetime.date.today(),wake_time) + datetime.timedelta(seconds=-30)
        wake_time=session_day + str(wake_time.hour)+":"+str(wake_time.minute)+":"+str(wake_time.second)
        # print(wake_time)
        wake_up = f'sudo rtcwake -m no -l -t "$(date +%s -d {wake_time})"'
        os.system(wake_up)
        # Scheduling threads.
        getattr(schedule.every(),session_day).at(course_time).do(hold_my_thread,code,session_date)
    else:
        # print("Hello_world_0")
        hold_my_thread(code,session_date)

if __name__ == '__main__':
    start = time.perf_counter()
    # 24-Mar-2021
    # scheduler('PL','monday','24-Mar-2021')
    # scheduler('OS_lab','monday')
    # scheduler('OS','tuesday')
    # scheduler('VR','tuesday')
    # scheduler('HSS','tuesday')
    # scheduler('PL','wednesday')
    # scheduler('CG1','wednesday')
    # scheduler('OS','thursday')
    # scheduler('VR','thursday')
    # scheduler('HSS','thursday')
    # scheduler('NC1','friday')
    # scheduler('NC2','friday')
    # scheduler('CG2','friday')
    scheduler('ST','monday')
    scheduler('DV','tuesday')
    scheduler('SPM','tuesday')
    scheduler('ST','wednesday')
    scheduler('DV','thursday')
    scheduler('SPM','thursday')
    scheduler('NSW','friday')
    # scheduler('NSW','friday','6-Aug-2021')    
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.submit(hold_on,'PL','live')
    #     executor.submit(hold_on,'CG1','live')
    final = time.perf_counter()
    print(f'{final-start} second(s)')
    while True:
        schedule.run_pending()
        # print("length: " + str(len(live_courses)))
        # Stopping the sessions and joining threads
        if(len(live_courses)!=0):
            course = live_courses[-1]
            if(course.session != "live"):
                live_courses.pop()
                thread_1 = live_threads[-1]
                thread_1.join()
                print(f"Thread {thread_1.getName()} joined")
                live_threads.pop()
                break
            course_info = course.get_course()
            curr_time = datetime.datetime.now().strftime('%H'+':'+'%M')
            # print(course_info[1])
            FMT = '%H:%M'
            tdelta = datetime.datetime.strptime(curr_time, FMT) - datetime.datetime.strptime(course_info[1], FMT)
            tdelta = tdelta.total_seconds()
            tdelta = tdelta/60
            # print(tdelta)
            if(int(tdelta)>=100):
                course.close_session()
                print(f"Session of {course.get_course()[0]} has ended...")
                live_courses.pop()
                thread_1 = live_threads[-1]
                thread_1.join()
                print(f"Thread {thread_1.getName()} joined")
                live_threads.pop()
                # print(thread_1.isAlive())

            # if(course.live == True):
            #     course.live_actions()
            # print()

    # Before : 20.056427884002915 second(s)
