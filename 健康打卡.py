# coding=UTF-8
import requests
import json
import datetime
import urllib
import hashlib

class MyError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class Dk():
    def Sign_In(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "65",
            "Origin": "https: //health.fjlzit.net",
            "Connection": "close",
            "Referer": "https://health.fjlzit.net/stu/",
            "Cookie": "JSESSIONID=61E02E7689E462FA4278C1B64970C64B",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        data = {
            "userCode": self.us,
            "userPwd": self.pw
        }
        s = requests.session()
        url = "https://health.fjlzit.net/api/mStuApi/token.do"
        s = s.post(url, data=data, headers=headers)
        self.accessToken = s.text[s.text.find("accessToken") + 14:-3]  # 获取token
        name = s.text[s.text.find("studentName") + 14:s.text.find("studentName") + 17]
        if s.text == '{"message":"用户名不存在或密码错误。","isSuccess":false,"data":{}}':
            raise MyError("账号或密码错误")
        print( name +"账号登录成功")

    def Get_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "accessToken": self.accessToken,
            "Content-Type": "application/json",
            "Content-Length": "19",
            "Origin": "https://health.fjlzit.net",
            "Connection": "close",
            "Referer": "https://health.fjlzit.net/stu/",
            "Cookie": "JSESSIONID=61E02E7689E462FA4278C1B64970C64B",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        data = {"page": "1", "rows": "9"}
        a = requests.post("https://health.fjlzit.net/api/mStuApi/queryByStuEpidemicHealthReport.do", headers=headers,
                          data=data)
        a = eval(a.text)  # 转为字典
        a = a["rows"]
        self.date = []  # 未打卡
        self.complete = []  # 已打卡
        for i in a:
            if i["dataStatus"] == "2":  # 根据dataStatus 来区分是否打卡
                self.complete.append(i)
            else:
                self.date.append(i)
        if self.complete==[]:
            raise MyError("未找到已填日报数据，请手动填一次日报")
        print("获取打卡数据成功")


    def Get_olddata(self):
        if self.date == []:
            raise MyError("没有未做日报的记录，")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "accessToken": self.accessToken,
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "41",
            "Origin": "https://health.fjlzit.net",
            "Connection": "close",
            "Referer": "https://health.fjlzit.net/stu/",
            "Cookie": "JSESSIONID=61E02E7689E462FA4278C1B64970C64B",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        data = {"healthId": (self.complete[0])["healthId"]}  # 获取首个已打卡的信息
        a = requests.post("https://health.fjlzit.net/api/mStuApi/getModelByIdEpidemicHealthReport.do", headers=headers,
                          data=data)
        self.updata = a.text
        self.updata = self.updata.replace("\\", "")
        self.updata = self.updata[36:-4]
        self.updata = "{" + self.updata + "}"  # 转换成字典
        self.updata = json.loads(self.updata)

    def Send_Out(self):
        for i in self.date:
            a = {"healthId": i["healthId"],
                 "rosterId": self.updata["rosterId"],
                 "march": self.updata["march"],
                 "isGoHubei": "2",
                 "isBackHubei": "2",
                 "isPassHubei": "2",
                 "isGoWenzhou": "2",
                 "isBackWenzhou": "2",
                 "isPassWenzhou": "2",
                 "isContactHubei": "2",
                 "isContactWenzhou": "2",
                 "isOutProvince": "2",
                 "isGoAbroad": "2",
                 "isTouchOut": "2",
                 "isSick": "2",
                 "symptomAndHandle": "无",
                 "otherThing": "无",
                 "dataDate": i["dataDate"],
                 "dataType": i["dataType"],
                 "dataStatus": "2",
                 "endTime": i["endTime"],
                 "liveState": "2",
                 "nowAddress": self.updata["nowAddress"],
                 "nowAddressDetail": self.updata["nowAddressDetail"],
                 "nowTiwenState": "1",
                 "nowHealthState": "1",
                 "counsellorApprovalStatus": "未审核",
                 "temperature": self.updata["temperature"],
                 "isContactViralPatient": "2",
                 "isHealthCodeGreen": "1",
                 "isPossessionQuarantine": "2",
                 "isNucleicAcidPositive": "2",
                 "isGfxReturn": "2",
                 "isJwReturn": "2",
                 "isContactPatient": "2",
                 "isContactRiskArea": "2",
                 "isHealthCodeOk": "2",
                 "details": ""
                 }
            s = str(len(a))
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate",
                "accessToken": self.accessToken,
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": s,
                "Origin": "https://health.fjlzit.net",
                "Connection": "close",
                "Referer": "https://health.fjlzit.net/stu/",
                "Cookie": "JSESSIONID=61E02E7689E462FA4278C1B64970C64B",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache"
            }
            data = {"healthId": a}
            a = requests.post("https://health.fjlzit.net/api/mStuApi/updateHealthReportEpidemicHealthReport.do",
                              headers=headers, data=a)
            if a.text=='{"isSuccess":true,"data":{}}':
                print(i["dataDate"] +"  "+ datetime.datetime.now().strftime('%R') +"  打卡成功")
            else:
               raise MyError("提交的数据有误，请检查。")

isuspw = [
    [“帐户”，“密码”，“姓名”],
    [“账号”，“密码”，“姓名”]＃可添加多个账号
    ]
for user_passwd in isuspw:
    user=Dk()
    user.us=user_passwd[0]   # 账号
    user.pw=user_passwd[1].encode('utf-8')  # 密码
    md5 = hashlib.md5()
    md5.update(user.pw)
    user.pw = md5.hexdigest()
    try:
        user.Sign_In()
        user.Get_data()
        user.Get_olddata()
        user.Send_Out()
    except MyError as e:
        print(user_passwd[2],end="")
        print(e)
    except:
        print ("未知错误")
    print("-----------------------------------------------------------------------")
