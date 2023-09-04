import requests
import json
url = 'https://querycourse.ntust.edu.tw/querycourse/api/courses'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Content-Type': 'application/json',
}

data = {
    'Semester': '1121',
    'CourseNo': '',
    'CourseName': '網際網路與應用',
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

print(response.status_code)  # 打印响应状态码
print(response.text)  # 打印响应内容
