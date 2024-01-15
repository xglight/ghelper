import os
import re
import base64
import requests
import json
from bs4 import BeautifulSoup
import pdfkit
import keyboard
import sys
import termios

username = "daniel"
url = "https://gmoj.net/senior"
userlist = {}
users = []
default_user = ""
SYSTEM = 1 # 0 Windows,1 Linux


def cls(i):
    word = ["----ghelper----","----ghelper用户管理----"]
    os.system("cls" if SYSTEM == 0 else "clear")
    print(word[i])


def start(x):
    os.system("%s " % ("start" if SYSTEM == 0 else "sudo -u " + username + " open") + x)


class menu:
    i = 0
    title = ''
    word = []
    w = 0
    behavior = []
    b = 0
    def __init__(self,title,word,behavior):
        self.title = title
        self.word = word
        self.w = len(word)
        self.behavior = behavior
        self.b = len(behavior)
        for j in range(len(behavior)):
            keyboard.add_hotkey(str(j + 1),behavior[j])
        keyboard.add_hotkey('up',self.shiftup)
        keyboard.add_hotkey('down',self.shiftdown)
        keyboard.add_hotkey('enter',self.enter)
        self.draw()
        while 1:
            continue
    def draw(self):
        cls(self.title)
        for j in range(self.w):
            print("%c" % (">" if self.i == j else " ") + str(j + 1) + "." + self.word[j])
    def shiftup(self):
        self.i = (self.w - 1 if self.i == 0 else self.i - 1)
        self.draw()
    def shiftdown(self):
        self.i = (0 if self.i == self.w - 1 else self.i + 1)
        self.draw()
    def enter(self):
        if self.i < self.b:
            self.behavior[self.i]()


def init():
    global userlist
    global users
    global default_user
    users = []
    if os.path.exists("user.json") == 0:
        userlist = {"default_user": {"username": ""},"users": {}}
        with open("user.json","w+",encoding="utf-8") as f:
            json.dump(userlist,f,indent=4,ensure_ascii=False)
        return
    elif os.path.getsize("user.json") == 0:
        userlist = {"default_user": {"username": ""},"users": {}}
        with open("user.json","w+",encoding="utf-8") as f:
            json.dump(userlist,f,indent=4,ensure_ascii=False)
        return
    with open("user.json","r",encoding="utf-8") as f:
        userlist = json.load(f)
    default_user = userlist["default_user"]["username"]
    for i in userlist["users"]:
        users.append(i)
    if default_user == "":
        return
    if (
        gmoj_login(
            default_user,base64_decry(userlist["users"][default_user]["password"])
        )
        == 0
    ):
        default_user = ""


def number():
    cls(0)
    termios.tcflush(sys.stdin,termios.TCIFLUSH) 
    start(url + "/#main/show/" + input("请输入题号："))
#
#
def topic():
    cls(0)
    termios.tcflush(sys.stdin,termios.TCIFLUSH) 
    start(url + "/#main/problemset?search=" + input("请输入搜索内容："))
#
#
def user():
    cls(0)
    termios.tcflush(sys.stdin,termios.TCIFLUSH) 
    start(url + "/#users/" + input("请输入用户名："))
#
#
#def pwd_input():
#    chars = []
#    while True:
#        try:
#            newChar = msvcrt.getch().decode(encoding="utf-8")
#        except:
#            return input("error")
#        if newChar in "\r\n":
#            break
#        elif newChar == "\b":
#            if chars:
#                del chars[-1]
#                msvcrt.putch("\b".encode(encoding="utf-8"))
#                msvcrt.putch(" ".encode(encoding="utf-8"))
#                msvcrt.putch("\b".encode(encoding="utf-8"))
#        else:
#            chars.append(newChar)
#            msvcrt.putch("*".encode(encoding="utf-8"))
#    return "".join(chars)
#
#
#headers = {
#    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
#}
#cookies = 1
#
#
#def base64_encry(plaintext):
#    base64_encry = str(base64.b64encode(plaintext.encode("utf-8")))
#    return base64_encry[base64_encry.find("'") + 1 : len(base64_encry) - 1]
#
#
#def base64_decry(ciphertext):
#    base64_decry = (base64.b64decode(ciphertext)).decode("utf-8")
#    return str(base64_decry)
#
#
#def gmoj_login(username,password):
#    geturl = "https://gmoj.net/junior/index.php/main/home"
#    r = requests.get(geturl,headers=headers)
#    global cookies
#    cookies = r.cookies
#    cookies = requests.utils.dict_from_cookiejar(cookies)
#    b = BeautifulSoup(r.text)
#    secretkey = b.find("script").text
#    prekey = secretkey[secretkey.find("saltl") + 7 : secretkey.find(";") - 1]
#    lastkey = secretkey[
#        secretkey.find("saltr") + 7 : secretkey.find(";",secretkey.find("saltr")) - 1
#    ]
#    posturl = "https://gmoj.net/senior/index.php/main/login"
#    postdata = {"username": username,"password": prekey + password + lastkey}
#    pr = requests.post(posturl,cookies=cookies,headers=headers,data=postdata)
#    return pr.text == "success"
#
#
def login():
    a=menu(1,["用户选择","新建用户","管理用户","退出"],[])
#        if x == b"w" and i > 1:
#            i -= 1
#        elif x == b"s" and i < 4:
#            i += 1
#        elif x == b"\r":
#            if i == 1:
#                if choose_user() == 1:
#                    return
#            elif i == 2:
#                if create_user() == 1:
#                    return
#            elif i == 3:
#                manage_user()
#            else:
#                return
#
#
#def manage_user():
#    i = 1
#    global default_user
#    while 1:
#        cls(1)
#        sum = len(userlist["users"])
#        j = 1
#        for u in userlist["users"]:
#            print("%c%d.%s" % (">" if i == j else " ",j,u))
#            j += 1
#        print("%c%d.退出" % (">" if i == 4 else " ",sum + 1))
#        x = msvcrt.getch()
#        if x == b"w" and i > 1:
#            i -= 1
#        elif x == b"s" and i < sum + 1:
#            i += 1
#        elif x == b"\r":
#            if i == sum + 1:
#                return
#            username = userlist["users"][users[i - 1]]["username"]
#            password = base64_decry(userlist["users"][users[i - 1]]["password"])
#            k = 1
#            while 1:
#                cls()
#                print("用户：%s" % username)
#                print("%c1.修改密码" % (">" if k == 1 else " "))
#                print("%c2.修改账号" % (">" if k == 2 else " "))
#                print("%c3.删除用户" % (">" if k == 3 else " "))
#                print("%c4.退出" % (">" if k == 4 else " "))
#                y = msvcrt.getch()
#                if y == b"w" and k > 1:
#                    k -= 1
#                elif y == b"s" and k < 4:
#                    k += 1
#                elif y == b"\r":
#                    if k == 1:
#                        cls()
#                        print("请输入密码：",end="")
#                        new_password = pwd_input()
#                        print("")
#                        user = {
#                            username: {
#                                "username": username,
#                                "password": base64_encry(new_password),
#                            }
#                        }
#                        userlist["users"]["users"].update(user)
#                        with open("user.json","w+",encoding="utf-8") as f:
#                            json.dump(userlist,f,indent=4,ensure_ascii=False)
#                        return
#                    elif k == 2:
#                        cls()
#                        print("请输入账号：",end="")
#                        new_username = pwd_input()
#                        print("")
#                        user = {
#                            username: {
#                                "username": new_username,
#                                "password": base64_encry(password),
#                            }
#                        }
#                        userlist["users"].update(user)
#                        with open("user.json","w+",encoding="utf-8") as f:
#                            json.dump(userlist,f,indent=4,ensure_ascii=False)
#                        return
#                    elif k == 3:
#                        if users[i - 1] == default_user:
#                            default_user = ""
#                        userlist["users"].pop(users[i - 1])
#                        users.pop(i - 1)
#                        i = 1
#                        with open("user.json","w+",encoding="utf-8") as f:
#                            json.dump(userlist,f,indent=4,ensure_ascii=False)
#                        init()
#                        return
#                    else:
#                        return
#
#
#def choose_user():
#    i = 1
#    global default_user
#    while 1:
#        cls(1)
#        sum = len(userlist["users"])
#        j = 1
#        print(sum)
#        for u in userlist["users"]:
#            print("%c%d.%s" % (">" if i == j else " ",j,u))
#            j += 1
#        x = msvcrt.getch()
#        if x == b"w" and i > 1:
#            i -= 1
#        elif x == b"s" and i < sum:
#            i += 1
#        elif x == b"\r":
#            username = userlist["users"][users[i - 1]]["username"]
#            password = base64_decry(userlist["users"][users[i - 1]]["password"])
#            f = 1
#            if gmoj_login(username,password):
#                print("成功！")
#                default_user = users[i - 1]
#            else:
#                print("失败")
#                f = 0
#            pause = os.system("pause")
#            return f
#
#
#def create_user():
#    global default_user
#    cls()
#    print("----ghelper创建用户----")
#    username = input("请输入用户名：")
#    print("请输入密码：",end="")
#    password = pwd_input()
#    print("")
#    if gmoj_login(username,password):
#        print("成功！")
#        default_user = username
#        user = {username: {"username": username,"password": base64_encry(password)}}
#        userlist["users"].update(user)
#        userlist["default_user"].update({"username": username})
#        with open("user.json","w+",encoding="utf-8") as f:
#            json.dump(userlist,f,indent=4,ensure_ascii=False)
#        init()
#    else:
#        print("失败！")
#        f = 0
#    pause = os.system("pause")
#    return f
#
#
#def html_to_pdf(html,to_file):
#    path_wkthmltopdf = r"D:\\LRK\\python\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
#    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
#    pdfkit.from_file(html,to_file,configuration=config)
#
#
#def get_html(b,id):
#    for i in b.find_all(class_="btn btn-mini btn_copy"):
#        i.decompose()
#    with open("data\\" + id + ".html","w+",encoding="utf-8") as f:
#        f.write("<head>\n")
#        f.write('  <meta charset="utf-8">\n')
#        f.write("</head>\n")
#        f.write(str(b.find(class_="row-fluid")))
#        f.write(str(b.find(id="problem_show_container").find(class_="span9")))
#        f.write(str(b.style))
#        f.write(str(b.find(type="text/javascript")))
#    html_to_pdf("data\\" + id + ".html",id + ".pdf")
#
#
#def get_markdown(b,id):
#    cls()
#    print("抱歉，markdown采集正在研发中...")
#    pause = os.system("pause")
#
#
#def get_problem():
#    cls()
#    id = input("请输入题号：")
#    url = "https://gmoj.net/senior/index.php/main/show/" + id
#    r = requests.get(url,cookies=cookies,headers=headers)
#    b = BeautifulSoup(r.text)
#    if b.find(style="margin-top: 4px") == None:
#        get_html(b,id)
#    else:
#        get_markdown(b,id)
#
#
#def get_match():
#    url = "https://gmoj.net/senior/index.php/contest/"
#    cls()
#    id = input("请输入比赛id：")
#    problem_url = url + "problems/" + id
#    r = requests.get(problem_url,headers=headers,cookies=cookies)
#    b = BeautifulSoup(r.text)
#    for i in b.find_all("a"):
#        i.extract()
#    for i in b.find_all("td"):
#        print(i.string)
#    pause = os.system("pause")


def main():
    init()
    print("用户：%s" % ("未登录" if (default_user == "") else default_user))
    a=menu(0,["搜索题号","搜索题目","搜索用户",\
            "用户管理（登录）","题目下载","比赛爬取","退出"],
            [number,topic,user,login])
main()
