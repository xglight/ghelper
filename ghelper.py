import os
import base64
import requests
import json
from bs4 import BeautifulSoup
import pdfkit
import easygui

url = "https://gmoj.net/senior"
js = {}
users = []
default_user = ""
codes = []
default_code = ""
exe_path = ""


def init():  # 预处理json
    global js
    global users
    global default_user
    global default_code
    default_user = ""
    users = []
    if os.path.exists("user.json") == 0:
        js = {
            "default_user": {"username": ""},
            "users": {},
            "default_code": {"codename": ""},
            "codes": {},
        }
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(js, f, indent=4, ensure_ascii=False)
        return
    elif os.path.getsize("user.json") == 0:
        js = {
            "default_user": {"username": ""},
            "users": {},
            "default_code": {"codename": ""},
            "codes": {},
        }
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(js, f, indent=4, ensure_ascii=False)
        return
    # 若无json，创建json
    with open("user.json", "r", encoding="utf-8") as f:
        js = json.load(f)  # 读取json
    default_user = js["default_user"]["username"]
    default_code = js["default_code"]["codename"]
    for i in js["users"]:
        users.append(i)  # 获取json所有用户
    for i in js["codes"]:
        codes.append(i)
    if default_user == "":
        return
    if (
        gmoj_login(default_user, base64_decry(js["users"][default_user]["password"]))
        != 1
    ):
        default_user = ""  # 判断用户能否成功登录


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


def get_user():
    url = "https://gmoj.net/senior/index.php/users/"
    reply = easygui.enterbox("用户名", title="ghelper")
    if reply == None:
        return
    get_url = url + reply
    try:
        r = requests.get(get_url, cookies=cookies, headers=headers, timeout=1)
    except TimeoutError:  # 超时
        easygui.msgbox("timeout", title="ghelper")
        # pause = os.system("pause")
        return -1
    except:  # 其他错误
        easygui.msgbox("login error", title="ghelper")
        # pause = os.system("pause")
        return -1
    b = BeautifulSoup(r.text, "html.parser")
    user = b.find(class_="dl-horizontal")
    project = ["用户名：", "uid:", "排名：", "AC 题目数：", "通过数：", "提交数：", "通过率：", "签名:"]
    information = {
        "用户名：": user.find(class_="label label-info").string,
    }
    j = 1
    for i in user.find_all(class_="badge badge-info"):
        information.update({project[j]: i.string})
        j += 1
    information.update({project[j]: user.find("i").string})
    with open("data\\" + reply + ".txt", "a+", encoding="utf-8") as f:
        f.truncate(0)
    for i in range(0, 8):
        with open("data\\" + reply + ".txt", "a", encoding="utf-8") as f:
            f.write(project[i])
            f.write(information[project[i]])
            f.write("\n")
    text = ""
    with open("data\\" + reply + ".txt", "r", encoding="utf-8") as f:
        text = f.read()
    easygui.textbox("用户：" + reply, title="ghelper", text=text)


def gmoj_login(username, password):  # 发送登录请求
    geturl = "https://gmoj.net/junior/index.php/main/home"  # 主地址（获取秘钥）
    try:  # 尝试请求
        r = requests.get(geturl, headers=headers, timeout=1)
    except TimeoutError:  # 超时
        easygui.msgbox("timeout", title="ghelper")
        # pause = os.system("pause")
        return -1
    except:  # 其他错误
        easygui.msgbox("login error", title="ghelper")
        # pause = os.system("pause")
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
        choices = ["1.用户选择", "2.新建用户", "3.修改密码"]
        reply = easygui.choicebox("ghelper用户管理（登录）", title="ghelper", choices=choices)
        if reply == choices[0]:
            if choose_user() == 1:
                return
        elif reply == choices[1]:
            if create_user() == 1:
                return
        elif reply == choices[2]:
            change_password()
        else:
            return


def choose_user():  # 选择用户登录
    i = 0
    global default_user
    while 1:
        choices = js["users"]
        reply = ""
        if len(choices) == 0:
            easygui.msgbox("无用户！", title="ghelper")
        elif len(choices) == 1:
            reply = easygui.ynbox(
                msg="选择：(y/n)"
                + str(choices)[
                    str(choices).find("'")
                    + 1 : str(choices).find("'", str(choices).find("'") + 1)
                ],
                title="ghelper",
                choices=("[<Y>]Yes", "[<N>]NO"),
                default_choice="[<Y>]Yes",
                cancel_choice="[<N>]No",
            )
            if reply == 0:
                return
            else:
                i = 0
        else:
            reply = easygui.choicebox("选择用户", title="ghelper", choices=choices)
            for j in choices:
                if reply == j:
                    break
                i += 1
            if i == len(choices):
                return
        username = js["users"][users[i]]["username"]
        password = base64_decry(js["users"][users[i]]["password"])  # 获取用户用户名、密码
        f = 1
        sit = gmoj_login(username, password)
        if sit == 1:
            easygui.msgbox("成功！", title="ghelper")
            default_user = users[i]
            # pause = os.system("pause")
        elif sit == 0:
            easygui.msgbox("该用户账号和密码不匹配！", title="ghelper")
            f = 0
            # pause = os.system("pause")
        return f


def create_user():  # 创建用户
    global default_user
    reply = easygui.multpasswordbox(
        "创建用户", title="ghelper", fields=["用户名：", "密码："], values=["", ""]
    )
    if reply == None or len(reply) < 2:
        return
    username = reply[0]
    password = reply[1]
    if username == "" or password == "":
        return
    f = 1
    sit = gmoj_login(username, password)  # 判断能否登陆成功
    if sit == 1:
        easygui.msgbox("成功！", "ghelper")
        default_user = username
        user = {username: {"username": username, "password": base64_encry(password)}}
        js["users"].update(user)
        js["default_user"].update({"username": username})
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(js, f, indent=4, ensure_ascii=False)
        init()
        # pause = os.system("pause")
    elif sit == 0:
        easygui.msgbox("失败！", "ghelper")
        f = 0
        # pause = os.system("pause")
    else:  # 未知错误
        f = 0
    return f


def change_password():
    i = 0
    global default_user
    while 1:
        choices = js["users"]
        reply = ""
        if len(choices) == 0:
            easygui.msgbox("无用户！", title="ghelper")
        elif len(choices) == 1:
            reply = easygui.ynbox(
                msg="选择：(y/n)"
                + str(choices)[
                    str(choices).find("'")
                    + 1 : str(choices).find("'", str(choices).find("'") + 1)
                ],
                title="ghelper",
                choices=("[<Y>]Yes", "[<N>]NO"),
                default_choice="[<Y>]Yes",
                cancel_choice="[<N>]No",
            )
            if reply == 0:
                return
            else:
                i = 0
        else:
            reply = easygui.choicebox("选择用户", title="ghelper", choices=choices)
            for j in choices:
                if reply == j:
                    break
                i += 1
            if i == len(choices):
                return
        username = js["users"][users[i]]["username"]  # 获取用户用户名
        password = easygui.passwordbox("修改密码", title="ghelper")
        if password == None:
            return
        new_user = {
            username: {
                username: {"username": username, "password": base64_encry(password)}
            }
        }
        js["users"].update(new_user)
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(js, f, indent=4, ensure_ascii=False)
        init()


# TODO:exe
def html_to_pdf(html, to_file):  # html转pdf
    path_wkthmltopdf = (
        exe_path + r"\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"  # 需外挂wkhtmltopdf.exe
    )
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit.from_file(html, to_file, configuration=config)


def get_html(b, id, path):  # 获取题目题面html
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
    html_to_pdf("data\\" + id + ".html", path + id + ".pdf")  # 转换pdf


def get_match_html(b, id):  # 获取比赛题目题面
    for i in b.find_all(class_="btn btn-mini btn_copy"):
        i.decompose()
    with open("data\\" + id + ".html", "w+", encoding="utf-8") as f:
        f.write("<head>\n")
        f.write('  <meta charset="utf-8">\n')
        f.write("</head>\n")
        f.write(str(b))
    html_to_pdf("data\\" + id + ".html", id + ".pdf")


# TODO:get_markdown
def get_markdown(b, id):  # 获取markdown题面
    cls = os.system("cls")
    print("抱歉，markdown采集正在研发中...")
    # pause = os.system("pause")


def get_problem():  # 获取题目
    cls = os.system("cls")
    if default_user == "":
        easygui.msgbox("你还未登录！", title="ghelper")
        # pause = os.system("pause")
        return
    id = easygui.enterbox(
        "题目id：",
        title="ghelper",
    )
    if id == None:
        return
    url = "https://gmoj.net/senior/index.php/main/show/" + id  #
    try:  # 尝试爬取
        r = requests.get(url, cookies=cookies, headers=headers)
    except:  # 错误
        easygui.msgbox("error", title="ghelper")
        return
    b = BeautifulSoup(r.text, "html.parser")
    title = b.find("h4").string
    if title != "(Standard IO)":
        title = b.find("h4").find("span").string
        title = title[0 : title.find(".")]
    else:
        title = id
    folder = os.path.exists(title)
    if not folder:
        os.makedirs(title)
    with open(title + "\\" + id + ".cpp", "w+", encoding="utf-8") as f:
        if default_code != "":
            f.write(base64_decry(js["codes"][default_code]["code"]))
    # 分析需不需freopen，若需，获取文件名
    if b.find(style="margin-top: 4px") == None:  # 判断是否为markdown
        get_html(b, title, title + "\\")
    else:
        get_markdown(b, title)


def get_match_problem(id, problem):  # 获取比赛题面
    cls = os.system("cls")
    if default_user == "":
        easygui.msgbox("你还未登录！", title="ghelper")
        return
    url = "https://gmoj.net/senior/index.php/contest/show/" + id + "/" + problem
    r = requests.get(url, cookies=cookies, headers=headers)
    b = BeautifulSoup(r.text, "html.parser")
    b.find(class_="navbar").extract()
    title = b.find("h4")
    if str(title) != "<h4>(Standard IO)</h4>":
        title = b.find("h4").find("span").string
        title = title[0 : title.find(".")]
    else:
        title = id
    folder = os.path.exists("data\\" + id + "\\" + title)
    if not folder:
        os.makedirs("data\\" + id + "\\" + title)
    folder = os.path.exists(id + "\\" + title)
    if not folder:
        os.makedirs(id + "\\" + title)
    with open(id + "\\" + title + "\\" + title + ".cpp", "w+", encoding="utf-8") as f:
        if default_code != "":
            f.write(base64_decry(js["codes"][default_code]["code"]))
    if (
        b.find(style="margin-top: 4px") == None
        or b.find(style="margin-top: 4px").string == "Submit"
    ):
        get_match_html(b, id + "\\" + title + "\\" + title)
    else:
        get_markdown(b, id + "\\" + title + "\\" + title)


def get_match():  # 获取比赛
    url = "https://gmoj.net/senior/index.php/contest/"
    if default_user == "":
        easygui.msgbox("你还未登录！", title="ghelper")
        return
    id = easygui.enterbox(
        "比赛id：",
        title="ghelper",
    )
    if id == None:
        return
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


def submit_problem():  # 题目提交
    url = "https://gmoj.net/senior/index.php/main/submit/"
    if default_user == "":
        easygui.msgbox("你还未登录！", title="ghelper")
        return
    reply = easygui.multenterbox(
        "输入题目信息：", title="ghelper", fields=["题目id：", "提交文件名"], values=["", ""]
    )
    if reply == None or reply.count() < 2:
        return
    id = reply[0]
    problem = reply[1]
    if id == "" or problem == "":
        return
    problem_url = url + id
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
    # pause = os.system("pause")


def code():
    choices = ["1.新建代码模版", "2.选择默认代码模版", "3.查看（更改）代码模版", "4.删除代码模版"]
    reply = easygui.choicebox(
        "当前代码模版：%s" % (("无") if (default_code == "") else default_code),
        title="ghelper",
        choices=choices,
    )
    if reply == choices[0]:
        create_code()
    elif reply == choices[1]:
        choose_code()
    elif reply == choices[2]:
        watch_code()
    elif reply == choices[3]:
        delete_code()
    else:
        return


def code_choose():
    i = 0
    choices = js["codes"]
    reply = ""
    if len(choices) == 0:
        easygui.msgbox("无代码模版！", title="ghelper")
        return -1
    elif len(choices) == 1:
        reply = easygui.ynbox(
            msg="选择：(y/n)"
            + str(choices)[
                str(choices).find("'")
                + 1 : str(choices).find("'", str(choices).find("'") + 1)
            ],
            title="ghelper",
            choices=("[<y>]Yes", "[<n>]NO"),
            default_choice="[<y>]Yes",
            cancel_choice="[<n>]No",
        )
        if reply == 0:
            return -1
        else:
            i = 0
    else:
        reply = easygui.choicebox("选择代码模版", title="ghelper", choices=choices)
        for j in choices:
            if reply == j:
                break
            i += 1
        if i == len(choices):
            return -1
    return i


def create_code():
    choices = ["通过文件", "通过编辑框", "Cancle"]
    codename = easygui.enterbox("代码模版名：", title="ghelper")
    code = ""
    if codename == None:
        return
    reply = easygui.buttonbox("选择写入方式：", title="ghelper", choices=choices)
    if reply == choices[0]:
        path = easygui.fileopenbox("选择文件", title="ghelper", default="D:\\")
        if path != None:
            with open(path, "r", encoding="utf-8") as f:
                t = f.read()
            f = easygui.codebox("确认文件：", title="ghelper", text=t)
            if f != None:
                code = f
    elif reply == choices[1]:
        f = easygui.codebox("编写文件", title="ghelper", text="")
        if f != None:
            code = f
    else:
        return
    if code == "":
        return
    new_code = {codename: {"codename": codename, "code": base64_encry(code)}}
    js["codes"].update(new_code)
    js["default_code"] = {"codename": codename}
    with open("user.json", "w+", encoding="utf-8") as f:
        json.dump(js, f, indent=4, ensure_ascii=False)
    init()


def choose_code():
    i = 0
    global default_code
    while 1:
        i = code_choose()
        if i == -1:
            return
        default_code = codes[i]
        return


def watch_code():
    i = 0
    while 1:
        i = code_choose()
        if i == -1:
            return
        code = base64_decry(js["codes"][codes[i]]["code"])
        reply = easygui.codebox("代码模版：" + codes[i], title="ghelper", text=code)
        new_code = {
            "codes": {
                codes[i]: {
                    "codename": codes[i],
                    "code": base64_encry(reply),
                }
            }
        }
        js.update(new_code)
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(js, f, indent=4, ensure_ascii=False)
        return


def delete_code():
    i = 0
    while 1:
        i = code_choose()
        if i == -1:
            return
        js["codes"].pop(codes[i])
        with open("user.json", "w+", encoding="utf-8") as f:
            json.dump(js, f, indent=4, ensure_ascii=False)
        return


def main():
    global exe_path
    exe_path = os.path.dirname(os.path.abspath(__file__))
    init()
    while 1:
        choices = ["1.用户管理（登录）", "2.题目下载", "3.比赛获取", "4.用户信息获取", "5.代码模版管理"]
        reply = easygui.choicebox(
            "用户：%s" % (("未登录") if (default_user == "") else default_user),
            title="ghelper",
            choices=choices,
        )
        if reply == choices[0]:
            login()
        elif reply == choices[1]:
            get_problem()
        elif reply == choices[2]:
            get_match()
        elif reply == choices[3]:
            get_user()
        elif reply == choices[4]:
            code()
        else:
            return


main()
