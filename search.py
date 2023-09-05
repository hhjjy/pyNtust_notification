import requests
import json
import send
import time
import schedule
import logging
import inspect

logging.basicConfig(filename='record.log', level=logging.INFO)

from datetime import datetime
url = 'https://querycourse.ntust.edu.tw/querycourse/api/courses'
courses = [
    "ET4606701",#網際網路與應用
    # "ECG003301",#通識課for 測試 
]


def get_time_now():
    # 获取当前时间
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    # 打印当前时间
    return formatted_now
# 2. 搜尋完成後，如果比對結果是可以選課的立即通知
# 3. 訂閱功能
# 定義格式
# ---------
# 程式名稱：
# 執行內容：
# 狀態：
def send_notification(action_name:str,content:str):
    url = r"https://maker.ifttt.com/trigger/Receive_NTUST_data/with/key/csemUFkrDzx8-tXknTeWGx "
    program_def_name = "台科大課程通知<br>"
    program_def_action = action_name+"<br>"
    program_content = f"{content}<br>"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "value1":program_def_name+program_def_action+program_content
    }

    response = requests.post(url, headers=headers, 
                            data=json.dumps(data).encode("utf-8"))
    if response.status_code != 200 :
        logging.error(f"{inspect.currentframe().f_code.co_nam} 傳送失敗！")
    # print(response.status_code)  # 打印响应状态码
    # print(response.text)  # 打印响应内容
# send_notification("查詢課程中","課程{}:選課人數...")
def search_for_course_info(ID:str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Content-Type': 'application/json',
    }

    data = {
        'Semester': '1121',
        'CourseNo': f'{ID}',
        'CourseName': '',
        'CourseTeacher': '',
        'Dimension': '',
        'CourseNotes': '',
        'ForeignLanguage': 0,
        'OnlyGeneral': 0,
        'OnleyNTUST': 0,
        'OnlyMaster': 0,
        'OnlyUnderGraduate': 0,
        'OnlyNode': 0,
        'Language': 'zh'
    }

    response = requests.post(url, headers=headers, 
                            data=json.dumps(data).encode("utf-8"))

    # print(response.status_code)  # 打印响应状态码
    # print(response.text)  # 打印响应内容
    return response.text

def search_job():
    logging.info(f"{get_time_now() }开始执行操作：{inspect.currentframe().f_code.co_name} ")
    select = False
    temp = ""
    for course in courses:
        try:
            json_struct = json.loads(search_for_course_info(course))
            course_name = json_struct[0]["CourseName"]
            cousr_choose_stud_nums = int(json_struct[0]["ChooseStudent"])
            course_Restrict_stud_nums = int(json_struct[0]["Restrict1"])
            print(course_name,end=" ")
            if (cousr_choose_stud_nums < course_Restrict_stud_nums):
                temp += f"{course} {course_name}可以選課了！<br>"
                print("可以選課了！")
                select = True
            else :
                temp += f"{course} {course_name}還不能選喔！<br>"
                print("還不能選喔！QQ")
        except Exception as e:
            logging.error("发生错误：{}".format(e))
            temp += f"找不到課程{course}！<br>"
    if select:
        send_notification("你有課程可以選了！",temp)

#確保程式仍在運作
def morning_job():
    logging.info(f"{get_time_now() }开始执行操作：{inspect.currentframe().f_code.co_name} ")
    send_notification("程式仍在工作中！","")

#每天早上定期傳送一個顯示當前狀態的通知 
#其他時間都照
#如果可以選課了！
# 傳送訊息確保正常運作！

#測試
# search_job()
#正常執行狀態
schedule.every(5).minutes.do(search_job)
schedule.every(4).hours.do(morning_job)
while(True):
    print(get_time_now())
    schedule.run_pending()
    time.sleep(1)