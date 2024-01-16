import msvcrt
import os
import re
import base64
import requests
import json
from bs4 import BeautifulSoup
import pdfkit

url = "https://gmoj.net/senior"
userlist = {}
users = []
default_user = ""


def init():
    global userlist
    global users
    global default_user
    users = []
    if os.path.exists("user.json") == 0:
        userlist = {"default_user": {"username": ""}, "users": {}}
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(userlist, f, indent=4, ensure_ascii=False)
        return
    elif os.path.getsize("user.json") == 0:
        userlist = {"default_user": {"username": ""}, "users": {}}
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(userlist, f, indent=4, ensure_ascii=False)
        return
    with open("user.json", "r", encoding="utf-8") as f:
        userlist = json.load(f)
    default_user = userlist["default_user"]["username"]
    for i in userlist["users"]:
        users.append(i)
    if default_user == "":
        return
    if (
        gmoj_login(
            default_user, base64_decry(userlist["users"][default_user]["password"])
        )
        != 1
    ):
        default_user = ""

def pwd_input():
    chars = []
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("error")
        if newChar in "\r\n":
            break
        elif newChar == "\b":
            if chars:
                del chars[-1]
                msvcrt.putch("\b".encode(encoding="utf-8"))
                msvcrt.putch(" ".encode(encoding="utf-8"))
                msvcrt.putch("\b".encode(encoding="utf-8"))
        else:
            chars.append(newChar)
            msvcrt.putch("*".encode(encoding="utf-8"))
    return "".join(chars)


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}
cookies = 1


def base64_encry(plaintext):
    base64_encry = str(base64.b64encode(plaintext.encode("utf-8")))
    return base64_encry[base64_encry.find("'") + 1 : len(base64_encry) - 1]


def base64_decry(ciphertext):
    base64_decry = (base64.b64decode(ciphertext)).decode("utf-8")
    return str(base64_decry)


def gmoj_login(username, password):
    geturl = "https://gmoj.net/junior/index.php/main/home"
    try:
        r = requests.get(geturl, headers=headers,timeout=1)
    except TimeoutError:
        print("timeout")
        pause = os.system("pause")
        return -1
    except:
        print("login error")
        pause = os.system("pause")
        return -1
    global cookies
    cookies = r.cookies
    cookies = requests.utils.dict_from_cookiejar(cookies)
    b = BeautifulSoup(r.text,"html.parser")
    secretkey = b.find("script").text
    prekey = secretkey[secretkey.find("saltl") + 7 : secretkey.find(";") - 1]
    lastkey = secretkey[
        secretkey.find("saltr") + 7 : secretkey.find(";", secretkey.find("saltr")) - 1
    ]
    posturl = "https://gmoj.net/senior/index.php/main/login"
    postdata = {"username": username, "password": prekey + password + lastkey}
    pr = requests.post(posturl, cookies=cookies, headers=headers, data=postdata)
    return pr.text == "success"


def login():
    i = 1
    while 1:
        cls = os.system("cls")
        print("----ghelper用户管理（登录）----")
        print("%c1.用户选择" % (">" if i == 1 else " "))
        print("%c2.新建用户" % (">" if i == 2 else " "))
        print("%c3.管理用户" % (">" if i == 3 else " "))
        print("%c4.退出" % (">" if i == 4 else " "))
        x = msvcrt.getch()

        if x == b"w" and i > 1:
            i -= 1
        elif x == b"s" and i < 4:
            i += 1
        elif x == b"\r":
            if i == 1:
                if choose_user() == 1:
                    return
            elif i == 2:
                if create_user() == 1:
                    return
            elif i == 3:
                manage_user()
            else:
                return


def manage_user():
    i = 1
    global default_user
    while 1:
        cls = os.system("cls")
        print("----ghelper用户管理----")
        sum = len(userlist["users"])
        j = 1
        for u in userlist["users"]:
            print("%c%d.%s" % (">" if i == j else " ", j, u))
            j += 1
        print("%c%d.退出" % (">" if i == 4 else " ", sum + 1))
        x = msvcrt.getch()
        if x == b"w" and i > 1:
            i -= 1
        elif x == b"s" and i < sum + 1:
            i += 1
        elif x == b"\r":
            if i == sum + 1:
                return
            username = userlist["users"][users[i - 1]]["username"]
            password = base64_decry(userlist["users"][users[i - 1]]["password"])
            k = 1
            while 1:
                cls = os.system("cls")
                print("----ghelper用户管理----")
                print("用户：%s" % username)
                print("%c1.修改密码" % (">" if k == 1 else " "))
                print("%c2.修改账号" % (">" if k == 2 else " "))
                print("%c3.删除用户" % (">" if k == 3 else " "))
                print("%c4.退出" % (">" if k == 4 else " "))
                y = msvcrt.getch()
                if y == b"w" and k > 1:
                    k -= 1
                elif y == b"s" and k < 4:
                    k += 1
                elif y == b"\r":
                    if k == 1:
                        cls = os.system("cls")
                        print("----ghelper----")
                        print("请输入密码：", end="")
                        new_password = pwd_input()
                        print("")
                        user = {
                            username: {
                                "username": username,
                                "password": base64_encry(new_password),
                            }
                        }
                        userlist["users"]["users"].update(user)
                        with open("user.json", "w+", encoding="utf-8") as f:
                            json.dump(userlist, f, indent=4, ensure_ascii=False)
                        return
                    elif k == 2:
                        cls = os.system("cls")
                        print("----ghelper----")
                        print("请输入账号：", end="")
                        new_username = pwd_input()
                        print("")
                        user = {
                            username: {
                                "username": new_username,
                                "password": base64_encry(password),
                            }
                        }
                        userlist["users"].update(user)
                        with open("user.json", "w+", encoding="utf-8") as f:
                            json.dump(userlist, f, indent=4, ensure_ascii=False)
                        return
                    elif k == 3:
                        if users[i - 1] == default_user:
                            default_user = ""
                        userlist["users"].pop(users[i - 1])
                        users.pop(i - 1)
                        i = 1
                        with open("user.json", "w+", encoding="utf-8") as f:
                            json.dump(userlist, f, indent=4, ensure_ascii=False)
                        init()
                        return
                    else:
                        return


def choose_user():
    i = 1
    global default_user
    while 1:
        cls = os.system("cls")
        print("----ghelper用户选择（登录）----")
        sum = len(userlist["users"])
        j = 1
        print(sum)
        for u in userlist["users"]:
            print("%c%d.%s" % (">" if i == j else " ", j, u))
            j += 1
        x = msvcrt.getch()
        if x == b"w" and i > 1:
            i -= 1
        elif x == b"s" and i < sum:
            i += 1
        elif x == b"\r":
            username = userlist["users"][users[i - 1]]["username"]
            password = base64_decry(userlist["users"][users[i - 1]]["password"])
            f = 1
            sit = gmoj_login(username, password)
            if sit==1:
                print("成功！")
                default_user = users[i - 1]
                pause = os.system("pause")
            elif sit==0 :
                print("账号和密码不匹配")
                f = 0
                pause = os.system("pause")        
            return f


def create_user():
    global default_user
    cls = os.system("cls")
    print("----ghelper创建用户----")
    username = input("请输入用户名：")
    print("请输入密码：", end="")
    password = pwd_input()
    print("")
    f=1
    sit  = gmoj_login(username, password)
    if sit==1:
        print("成功！")
        default_user = username
        user = {username: {"username": username, "password": base64_encry(password)}}
        userlist["users"].update(user)
        userlist["default_user"].update({"username": username})
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(userlist, f, indent=4, ensure_ascii=False)
        init()
        pause = os.system("pause")
    elif sit==0:
        print("失败！")
        f = 0
        pause = os.system("pause")
    else: f=0
    return f


def html_to_pdf(html, to_file):
    path_wkthmltopdf = r"D:\\LRK\\python\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit.from_file(html, to_file, configuration=config)


def get_html(b, id):
    for i in b.find_all(class_="btn btn-mini btn_copy"):
        i.decompose()
    with open("data\\" + id + ".html", "w+", encoding="utf-8") as f:
        f.write("<head>\n")
        f.write('  <meta charset="utf-8">\n')
        f.write("</head>\n")
        f.write(str(b.find(class_="row-fluid")))
        f.write(str(b.find(id="problem_show_container").find(class_="span9")))
        f.write(str(b.style))
        f.write(str(b.find(type="text/javascript")))
    html_to_pdf("data\\" + id + ".html", id + ".pdf")

def get_match_html(b, id):
    for i in b.find_all(class_="btn btn-mini btn_copy"):
        i.decompose()
    with open("data\\" + id + ".html", "w+", encoding="utf-8") as f:
        f.write("<head>\n")
        f.write('  <meta charset="utf-8">\n')
        f.write("</head>\n")
        f.write(str(b))
    html_to_pdf("data\\" + id + ".html", id + ".pdf")

def get_markdown(b, id):
    cls = os.system("cls")
    print("抱歉，markdown采集正在研发中...")
    pause = os.system("pause")


def get_problem():
    cls = os.system("cls")
    if default_user=="":
        print("你还未登录！")
        pause = os.system("pause")
        return
    id = input("请输入题号：")
    url = "https://gmoj.net/senior/index.php/main/show/" + id
    try:
        r = requests.get(url, cookies=cookies, headers=headers)
    except:
        print("error")
        return
    b = BeautifulSoup(r.text,"html.parser")
    title = b.find("h4").string
    if title!="(Standard IO)":
        title = b.find("h4").find("span").string
        title = title[0:title.find('.')]
    else: title = id
    
    if b.find(style="margin-top: 4px") == None:
        get_html(b, title)
    else:
        get_markdown(b, title)

def get_match_problem(id,problem):
    cls = os.system("cls")
    if default_user=="":
        print("你还未登录！")
        pause = os.system("pause")
        return
    url = "https://gmoj.net/senior/index.php/contest/show/" + id+"/"+problem
    r = requests.get(url, cookies=cookies, headers=headers)
    b = BeautifulSoup(r.text,"html.parser")
    b.find(class_="navbar").extract()
    title = b.find("h4")
    if title!="<h4>(Standard IO)</h4>":
        title = b.find("h4").find("span").string
        title = title[0:title.find('.')]
    else: title = id
    folder = os.path.exists("data\\"+id+"\\"+title)
    if not folder:
        os.makedirs("data\\"+id+"\\"+title)
    folder = os.path.exists(id+"\\"+title)
    if not folder:
        os.makedirs(id+"\\"+title)
    if b.find(style="margin-top: 4px") == None or b.find(style="margin-top: 4px").string=="Submit":
        get_match_html(b, id+"\\"+title+"\\"+title)
    else:
        get_markdown(b, id+"\\"+title+"\\"+title)


def get_match():
    url = "https://gmoj.net/senior/index.php/contest/"
    cls = os.system("cls")
    if default_user=="":
        print("你还未登录！")
        pause = os.system("pause")
        return
    id = input("请输入比赛id：")
    list_url = url + "problems/" + id
    r = requests.get(list_url, headers=headers, cookies=cookies)
    b = BeautifulSoup(r.text,"html.parser")
    folder = os.path.exists(id)
    if not folder:
        os.makedirs(id)
    folder = os.path.exists("data\\"+id)
    if not folder:
        os.makedirs("data\\"+id)
    for i in b.find_all("a"):
        i.extract()
    for i in b.find_all("td"):
        if i.string != None:
            get_match_problem(id,i.string)
    pause = os.system("pause")


def main():
    init()
    cls = os.system("cls")
    i = 1
    while 1:
        print("----ghelper----")
        print("用户：%s" % ("未登录" if (default_user == "") else default_user))
        print("%c1.用户管理（登录）" % (">" if i == 1 else " "))
        print("%c2.题目下载" % (">" if i == 2 else " "))
        print("%c3.比赛爬取" % (">" if i == 3 else " "))
        print("%c4.退出" % (">" if i == 4 else " "))
        x = msvcrt.getch()
        if x == b"w" and i > 1:
            i -= 1
        elif x == b"s" and i < 8:
            i += 1
        elif x == b"\r":
            if i == 1:
                login()
            elif i == 2:
                get_problem()
            elif i == 3:
                get_match()
            else:
                break

        cls = os.system("cls")


main()