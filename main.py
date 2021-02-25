import requests
import json
import time


#  -----键入个人信息

userKey = ''
expectSec = 441  # 期待的耗时，单位：秒
testType = 1  # 0为自测 1为考试
testWeek = 16  # 测试周


#  ----------



def isChinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


#  -----------请求头

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'skl.hdu.edu.cn',
    'Origin': 'https://skl.hduhelp.com',
    'Referer': 'https://skl.hduhelp.com/?token=' + userKey,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/4.9.2',
    'X-Auth-Token': userKey
}

#  -----------

# ------单词本初始化
file = open('四级.txt', 'r', encoding='utf-8')
dict = {}  # 单词本

for line in file.readlines():  # 依次读取每行
    line = line.strip()  # 去掉每行头尾空白
    if line != '':
        lines = line.split('\t', 1)
        dict[lines[0].strip()] = lines[1].strip()
file.close()

# -------------

print('正在获取并解析题目...')
response = requests.get('https://skl.hdu.edu.cn/api/paper/new?type={0}&week={1}'.format(testType,testWeek), headers=headers)
data = json.loads(response.text)

submit = {}
submit['list'] = []
for list in data['list']:
    if isChinese(list['title']):
        if list['answerA'] in dict and dict[list['answerA']].find(list['title']) != -1:
            answer = 'A'
        elif list['answerB'] in dict and dict[list['answerB']].find(list['title']) != -1:
            answer = 'B'
        elif list['answerC'] in dict and dict[list['answerC']].find(list['title']) != -1:
            answer = 'C'
        elif list['answerD'] in dict and dict[list['answerD']].find(list['title']) != -1:
            answer = 'D'
        else:
            answer = 'B'
    elif list['title'] in dict:
        if dict[list['title']].find(list['answerA']) != -1:
            answer = 'A'
        elif dict[list['title']].find(list['answerB']) != -1:
            answer = 'B'
        elif dict[list['title']].find(list['answerC']) != -1:
            answer = 'C'
        elif dict[list['title']].find(list['answerD']) != -1:
            answer = 'D'
        else:
            answer = 'B'
    else:
        answer = 'B'
    submit_single = {}
    submit_single['input'] = answer
    submit_single['paperDetailId'] = list['paperDetailId']
    submit['list'].append(submit_single)
submit['paperId'] = data['paperId']

# -------------
print(f'延时{expectSec}秒...')
time.sleep(expectSec)

print("开始答题...")
requests.options("https://skl.hdu.edu.cn/api/paper/save", headers=headers)

response = requests.post("https://skl.hdu.edu.cn/api/paper/save", json=submit, headers=headers)

# --------------
print('答题结束！！情况如下：\n')
data = json.loads(response.text)

print('学号：', data['studentId'])
print('专业：', data['major'])
print('学年：', data['schoolYear'])
print('学期： 第', data['semester'], '学期')
print('###成绩：', data['mark'], '分')
print('耗时：', data['totalTime'] / 1000, '秒')

