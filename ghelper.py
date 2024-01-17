import msvcrt
import os
import base64
import requests
import json
from bs4 import BeautifulSoup
import pdfkit

url = "https://gmoj.net/senior"
userlist = {}
users = []
default_user = ""


def init():  # 预处理json
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
    # 若无json，创建json
    with open("user.json", "r", encoding="utf-8") as f:
        userlist = json.load(f)  # 读取json
    default_user = userlist["default_user"]["username"]
    for i in userlist["users"]:
        users.append(i)  # 获取json所有用户
    if default_user == "":
        return
    if (
        gmoj_login(
            default_user, base64_decry(userlist["users"][default_user]["password"])
        )
        != 1
    ):
        default_user = ""  # 判断用户能否成功登录


def pwd_input():  # 密码输入，无回显
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


headers = {  # 请求头
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}
cookies = 1  # cookies


def base64_encry(plaintext):  # base64加密
    base64_encry = str(base64.b64encode(plaintext.encode("utf-8")))
    return base64_encry[base64_encry.find("'") + 1 : len(base64_encry) - 1]


def base64_decry(ciphertext):  # base64解密
    base64_decry = (base64.b64decode(ciphertext)).decode("utf-8")
    return str(base64_decry)


def gmoj_login(username, password):  # 发送登录请求
    geturl = "https://gmoj.net/junior/index.php/main/home"  # 主地址（获取秘钥）
    try:  # 尝试请求
        r = requests.get(geturl, headers=headers, timeout=1)
    except TimeoutError:  # 超时
        print("timeout")
        pause = os.system("pause")
        return -1
    except:  # 其他错误
        print("login error")
        pause = os.system("pause")
        return -1
    global cookies
    cookies = r.cookies  # 获取cookies，用于之后登录（cookies可保存登录状态）
    cookies = requests.utils.dict_from_cookiejar(cookies)  # cookies格式化
    b = BeautifulSoup(r.text, "html.parser")  # 用bs4处理get的信息
    secretkey = b.find("script").text  # 获取秘钥
    prekey = secretkey[secretkey.find("saltl") + 7 : secretkey.find(";") - 1]
    lastkey = secretkey[
        secretkey.find("saltr") + 7 : secretkey.find(";", secretkey.find("saltr")) - 1
    ]  # 制作密文
    posturl = "https://gmoj.net/senior/index.php/main/login"  # post登录地址
    postdata = {"username": username, "password": prekey + password + lastkey}  # post数据
    # print(postdata)
    pr = requests.post(
        posturl, cookies=cookies, headers=headers, data=postdata
    )  # 发送post登录请求
    return pr.text == "success"  # 判断是否成功


def login():  # 登录
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


def manage_user():  # 用户管理
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
                        }  # 制作json
                        userlist["users"]["users"].update(user)
                        with open("user.json", "w+", encoding="utf-8") as f:
                            json.dump(
                                userlist, f, indent=4, ensure_ascii=False
                            )  # 写入json
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
                        }  # 制作json
                        userlist["users"].update(user)
                        with open("user.json", "w+", encoding="utf-8") as f:
                            json.dump(
                                userlist, f, indent=4, ensure_ascii=False
                            )  # 写入json
                        return
                    elif k == 3:
                        if users[i - 1] == default_user:
                            default_user = ""
                        userlist["users"].pop(users[i - 1])
                        users.pop(i - 1)
                        i = 1
                        with open("user.json", "w+", encoding="utf-8") as f:
                            json.dump(
                                userlist, f, indent=4, ensure_ascii=False
                            )  # 写入json
                        init()
                        return
                    else:
                        return


def choose_user():  # 选择用户登录
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
            password = base64_decry(
                userlist["users"][users[i - 1]]["password"]
            )  # 获取用户用户名、密码
            f = 1
            sit = gmoj_login(username, password)
            if sit == 1:
                print("成功！")
                default_user = users[i - 1]
                pause = os.system("pause")
            elif sit == 0:
                print("账号和密码不匹配")
                f = 0
                pause = os.system("pause")
            return f


def create_user():  # 创建用户
    global default_user
    cls = os.system("cls")
    print("----ghelper创建用户----")
    username = input("请输入用户名：")
    print("请输入密码：", end="")
    password = pwd_input()
    print("")
    f = 1
    sit = gmoj_login(username, password)  # 判断能否登陆成功
    if sit == 1:
        print("成功！")
        default_user = username
        user = {username: {"username": username, "password": base64_encry(password)}}
        userlist["users"].update(user)
        userlist["default_user"].update({"username": username})
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(userlist, f, indent=4, ensure_ascii=False)
        init()
        pause = os.system("pause")
    elif sit == 0:
        print("失败！")
        f = 0
        pause = os.system("pause")
    else:  # 未知错误
        f = 0
    return f


def html_to_pdf(html, to_file):  # html转pdf
    path_wkthmltopdf = (
        r"D:\\LRK\\python\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"  # 需外挂wkhtmltopdf.exe
    )
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit.from_file(html, to_file, configuration=config)


def get_html(b, id):  # 获取题目题面html
    for i in b.find_all(class_="btn btn-mini btn_copy"):
        i.decompose()  # 排除不需要内容
    with open("data\\" + id + ".html", "w+", encoding="utf-8") as f:
        f.write("<head>\n")
        f.write('  <meta charset="utf-8">\n')
        f.write("</head>\n")  # 写入编码
        f.write(str(b.find(class_="row-fluid")))
        f.write(str(b.find(id="problem_show_container").find(class_="span9")))
        f.write(str(b.style))
        f.write(str(b.find(type="text/javascript")))
    html_to_pdf("data\\" + id + ".html", id + ".pdf")  # 转换pdf


def get_match_html(b, id):  # 获取比赛题目题面
    for i in b.find_all(class_="btn btn-mini btn_copy"):
        i.decompose()
    with open("data\\" + id + ".html", "w+", encoding="utf-8") as f:
        f.write("<head>\n")
        f.write('  <meta charset="utf-8">\n')
        f.write("</head>\n")
        f.write(str(b))
    html_to_pdf("data\\" + id + ".html", id + ".pdf")


def get_markdown(b, id):  # 获取markdown题面
    cls = os.system("cls")
    print("抱歉，markdown采集正在研发中...")
    pause = os.system("pause")


def get_problem():  # 爬取题目
    cls = os.system("cls")
    if default_user == "":
        print("你还未登录！")
        pause = os.system("pause")
        return
    id = input("请输入题号：")
    url = "https://gmoj.net/senior/index.php/main/show/" + id  #
    try:  # 尝试爬取
        r = requests.get(url, cookies=cookies, headers=headers)
    except:  # 错误
        print("error")
        return
    b = BeautifulSoup(r.text, "html.parser")
    title = b.find("h4").string
    if title != "(Standard IO)":
        title = b.find("h4").find("span").string
        title = title[0 : title.find(".")]
    else:
        title = id
    # 分析需不需freopen，若需，获取文件名
    if b.find(style="margin-top: 4px") == None:  # 判断是否为markdown
        get_html(b, title)
    else:
        get_markdown(b, title)


i = 0


def get_match_problem(id, problem):  # 获取比赛题面
    cls = os.system("cls")
    if default_user == "":
        print("你还未登录！")
        pause = os.system("pause")
        return
    url = "https://gmoj.net/senior/index.php/contest/show/" + id + "/" + problem
    r = requests.get(url, cookies=cookies, headers=headers)
    b = BeautifulSoup(r.text, "html.parser")
    b.find(class_="navbar").extract()
    title = b.find("h4")
    # if title != "<h4>(Standard IO)</h4>":
    #     title = b.find("h4").find("span").string
    #     title = title[0 : title.find(".")]
    # else:
    global i
    title = str(i)
    i += 1
    folder = os.path.exists("data\\" + id + "\\" + title)
    if not folder:
        os.makedirs("data\\" + id + "\\" + title)
    folder = os.path.exists(id + "\\" + title)
    if not folder:
        os.makedirs(id + "\\" + title)
    if (
        b.find(style="margin-top: 4px") == None
        or b.find(style="margin-top: 4px").string == "Submit"
    ):
        get_match_html(b, id + "\\" + title + "\\" + title)
    else:
        get_markdown(b, id + "\\" + title + "\\" + title)


def get_match():  # 获取比赛
    url = "https://gmoj.net/senior/index.php/contest/"
    cls = os.system("cls")
    if default_user == "":
        print("你还未登录！")
        pause = os.system("pause")
        return
    id = input("请输入比赛id：")
    list_url = url + "problems/" + id  # 比赛地址
    r = requests.get(list_url, headers=headers, cookies=cookies)
    b = BeautifulSoup(r.text, "html.parser")
    folder = os.path.exists(id)
    if not folder:
        os.makedirs(id)
    folder = os.path.exists("data\\" + id)
    if not folder:
        os.makedirs("data\\" + id)
    for i in b.find_all("a"):
        i.extract()
    for i in b.find_all("td"):
        if i.string != None:
            get_match_problem(id, i.string)
    pause = os.system("pause")


def submit_problem():  # 题目提交
    url = "https://gmoj.net/senior/index.php/main/submit/"
    cls = os.system("cls")
    if default_user == "":
        print("你还未登录！")
        pause = os.system("pause")
        return
    id = input("请输入题目id：")
    problem_url = url + id
    problem = input("请输入提交文件名：")
    submit = ""
    with open(problem, "r", encoding="utf-8") as f:
        submit = base64_encry(f.read())
    postdata = {
        "pid": id,
        "tid": "",
        "cid": "",
        "gid": "",
        "cookie-language": "c++14",
        "language": {"SRC": "c++14"},
        "texteditor": {"SRC": submit},
    }  # 制作post数据包
    print(problem_url)
    # r = requests.post(problem_url, headers=headers, cookies=cookies, data=postdata)
    pause = os.system("pause")


def test():  # 测试
    url = "https://gmoj.net/senior/index.php/customtest/run"
    problem = input("请输入提交文件名：")
    submit = ""
    with open(problem, "r", encoding="utf-8") as f:
        submit = base64_encry(f.read())
    data = {
        "texteditor": submit,
        "toggle_editor": "on",
        "language": "C++14",
        "input_method": "use_text",
        "input_text": "3\n\
1 2 3\n\
3\n\
1 1 1\n\
2 2\n\
3 2 1 2\n\
2\n\
2 3",
    }
    r = requests.post(url, headers=headers, cookies=cookies, data=data)
    with open("test.txt", "w+", encoding="utf-8") as f:
        f.write(r.text)
    print(r.text)
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
        print("%c4.题目提交" % (">" if i == 4 else " "))
        print("%c5.test" % (">" if i == 5 else " "))
        print("%c5.退出" % (">" if i == 6 else " "))
        x = msvcrt.getch()
        if x == b"w" and i > 1:
            i -= 1
        elif x == b"s" and i < 5:
            i += 1
        elif x == b"\r":
            if i == 1:
                login()
            elif i == 2:
                get_problem()
            elif i == 3:
                get_match()
            elif i == 4:
                submit_problem()
            elif i == 5:
                test()
            else:
                break

        cls = os.system("cls")


main()
