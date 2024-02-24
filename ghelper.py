import sys
import os
import json
import base64
import requests
from bs4 import BeautifulSoup
import pdfkit
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_ghelper import Ui_ghelper  # 导入你写的界面类
import shutil
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
json_path = "ghelper.json"
js = {}
default_user = ""
users = []
headers = {  # 请求头
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}
cookies = ""
exePath = ""
dataPath = ""
problem = []
search = ""
savePath = ""


def base64Encry(plaintext):  # base64加密
    base64Encry = str(base64.b64encode(plaintext.encode("utf-8")))
    return base64Encry[base64Encry.find("'") + 1 : len(base64Encry) - 1]


def base64Decry(ciphertext):  # base64解密
    base64Decry = (base64.b64decode(ciphertext)).decode("utf-8")
    return str(base64Decry)


def login(username, password):  # 发送登录请求
    global cookies
    geturl = "https://gmoj.net/junior/index.php/main/home"  # 主地址（获取秘钥）
    r = requests.get(geturl, headers=headers, timeout=1)
    cookies = r.cookies  # 获取cookies，用于之后登录（cookies可保存登录状态）
    cookies = requests.utils.dict_from_cookiejar(cookies)  # cookies格式化
    b = BeautifulSoup(r.text, "html.parser")  # 用bs4处理get的信息
    if str(b) == "None":
        return -1
    secretkey = b.find("script").text  # 获取秘钥
    prekey = secretkey[secretkey.find("saltl") + 7 : secretkey.find(";") - 1]
    lastkey = secretkey[
        secretkey.find("saltr") + 7 : secretkey.find(";", secretkey.find("saltr")) - 1
    ]  # 制作密文
    posturl = "https://gmoj.net/senior/index.php/main/login"  # post登录地址
    postdata = {
        "username": username,
        "password": prekey + password + lastkey,
    }  # post数据
    # print(postdata)
    pr = requests.post(
        posturl, cookies=cookies, headers=headers, data=postdata
    )  # 发送post登录请求
    return pr.text == "success"  # 判断是否成功


def getAnnex(id, path):
    url = "https://gmoj.net/senior/index.php/main/showdownload/" + str(id)
    try:
        r = requests.get(url, headers=headers, cookies=cookies)
    except:
        return -1
    b = BeautifulSoup(r.text, "html.parser").find(id="downloads").tbody
    if str(b) == "None":
        return -1
    for i in b.find_all("tr"):
        filename = i.find("td").find_next("td").a.text
        download_url = "https://gmoj.net/senior/" + str(
            i.find("td").find_next("td").a.get("href")
        )
        r = requests.get(download_url, headers=headers, cookies=cookies)
        with open(savePath + path + filename, "w+", encoding="utf-8") as f:
            f.write(r.text)


def htmlToPdf(html, to_file):  # html转pdf
    path_wkthmltopdf = (
        exePath + r"/wkhtmltopdf/bin/wkhtmltopdf.exe"  # 需外挂wkhtmltopdf.exe + "/"
    )
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit.from_file(html, to_file, configuration=config, options={"encoding": "utf-8"})


def getHtml(b, title, folder):  # 获取题目题面html
    for i in b.find_all(class_="btn btn-mini btn_copy"):
        i.decompose()  # 排除不需要内容
    vis = 0
    x = 1
    for i in b.find_all(class_="sample_pre sample_pre_borderless"):
        if not vis:
            if not os.path.exists(dataPath + folder):
                os.makedirs(dataPath + folder)
            with open(
                dataPath + folder + title + "_" + str(x) + ".in", "w+", encoding="utf-8"
            ) as f:
                f.write(i.text)
            with open(
                dataPath + folder + title + "_" + str(x) + ".in", "r+", encoding="utf-8"
            ) as f:
                with open(
                    savePath + folder + title + "_" + str(x) + ".in",
                    "w+",
                    encoding="utf-8",
                ) as ff:
                    ss = f.readlines()
                    for s in ss:
                        if s == "\n" or s == "" or s == " " or s == " \n":
                            continue
                        else:
                            ff.write(s)

            vis = 1
        else:
            with open(
                dataPath + folder + title + "_" + str(x) + ".ans",
                "w+",
                encoding="utf-8",
            ) as f:
                f.write(i.text)
            with open(
                dataPath + folder + title + "_" + str(x) + ".ans",
                "r+",
                encoding="utf-8",
            ) as f:
                with open(
                    savePath + folder + title + "_" + str(x) + ".ans",
                    "w+",
                    encoding="utf-8",
                ) as ff:
                    ss = f.readlines()
                    for s in ss:
                        if s == "\n" or s == "" or s == " " or s == " \n":
                            continue
                        else:
                            ff.write(s)

            vis = 1
    with open(dataPath + folder + title + ".html", "w+", encoding="utf-8") as f:
        f.write("<head>\n")
        f.write('  <meta charset="utf-8">\n')
        f.write("</head>\n")  # 写入编码
        f.write(str(b.find(class_="row-fluid")))
        f.write(str(b.find(id="problem_show_container").find(class_="span9")))
        f.write(str(b.style))
        f.write(str(b.find(type="text/javascript")))
    htmlToPdf(
        dataPath + folder + title + ".html", savePath + folder + title + ".pdf"
    )  # 转换pdf


def getMarkdown(b, title, folder):  # 获取markdown题面
    cls = os.system("cls")
    head = b.find(style="text-align: center")
    body = b.find(id="problem_show_container")
    problem = body.script.text
    with open(dataPath + folder + title + ".txt", "w+", encoding="utf-8") as f:
        f.write(problem)
    with open(savePath + folder + title + ".md", "w+", encoding="utf-8") as f:
        f.write("# " + head.h2.text + "\n\n")
        f.write(str(head.h4) + "\n\n")
        sampleData = body.find(class_="div_samplecase")
        timeLimits = (
            head.find(id="problem_judge_details")
            .find("span")
            .find(class_="badge badge-info")
        )
        memeryLimits = timeLimits.find_next("span").find(class_="badge badge-info")
        f.write("Time Limits: " + timeLimits.text + "\n\n")
        f.write("Memory Limits: " + memeryLimits.text + "\n\n")
        vis1 = vis2 = 0
        with open(dataPath + folder + title + ".txt", "r", encoding="utf-8") as ff:
            text = ff.readlines()
            for i in text:
                if i.find("problem_description") != -1:
                    f.write("## Problem Description\n\n")
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 3]
                    f.write(s + "\n")
                    continue
                elif i.find("input_description") != -1 and not vis1:
                    f.write("## Input\n\n")
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 3]
                    f.write(s + "\n")
                    vis1 = 1
                    continue
                elif i.find("output_description") != -1 and not vis2:
                    f.write("## Output\n\n")
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 3]
                    f.write(s + "\n")
                    vis2 = 1
                    bb = 1
                    visin = 1
                    f.write("## Sample Data\n\n")
                    for j in sampleData.find_all(class_="div_samplecase_plaintext"):
                        for k in j.find_all("div"):
                            f.write("##### " + k.h5.span.text + "\n```\n")
                            f.write(k.pre.text + "\n```\n")
                            if visin:
                                with open(
                                    savePath + folder + title + "_" + str(bb) + ".in",
                                    "w+",
                                    encoding="utf-8",
                                ) as fff:
                                    fff.write(k.pre.text)
                                visin = 0
                            else:
                                with open(
                                    savePath + folder + title + "_" + str(bb) + ".ans",
                                    "w+",
                                    encoding="utf-8",
                                ) as fff:
                                    fff.write(k.pre.text)
                                bb += 1
                                visin = 1
                    for j in sampleData.find_all(class_="div_samplecase_markdown"):
                        f.write("##### " + j.h5.text + "\n")
                        f.write(j.div.get("data-markdown") + "\n")
                    continue
                elif i.find("data_constraint") != -1:
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 3]
                    if s == "":
                        continue
                    f.write("## Data Constraint\n\n")
                    f.write(s + "\n")
                    continue
                elif i.find("hint") != -1:
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 7]
                    if s == "":
                        continue
                    f.write("## Hint\n\n")
                    f.write(s + "\n")
                    continue


def downloadProblem(id):
    global cookies
    url = "https://gmoj.net/senior/index.php/main/show/" + str(id)  #
    try:  # 尝试爬取
        r = requests.get(url, cookies=cookies, headers=headers)
    except:  # 错误
        return -1
    b = BeautifulSoup(r.text, "html.parser")
    if str(b) == "None" or b.find(style="white-space: pre-wrap") != None:
        return -1
    title = str(b.find("h4").string)
    if title != "(Standard IO)":
        title = b.find("h4").find("span").string
        title = title[0 : title.find(".")]
    else:
        title = id
    if not os.path.exists(savePath + str(title)):
        os.makedirs(savePath + str(title))
    if not os.path.exists(dataPath + str(title)):
        os.makedirs(dataPath + str(title))
    title = str(title)
    getAnnex(id, str(title) + "/")
    # with open(title + "/" + id + ".cpp", "w+", encoding="utf-8") as f:
    #     if default_code != "":
    #         f.write(base64Decry(js["codes"][default_code]["code"]))
    # 分析需不需freopen，若需，获取文件名
    if b.find(id="problem_description") == None:  # 判断是否为markdown
        getHtml(b, str(title), str(title) + "/")
    else:
        getMarkdown(b, str(title), str(title) + "/")


lastpage = 1
page = 1


def searchProblem(search):
    global cookies
    global problem
    global lastpage
    global page
    lastpage = page = 1
    problem = []
    url = "https://gmoj.net/senior/index.php/main/problemset?search=" + search
    try:
        r = requests.get(url, cookies=cookies, headers=headers)
    except:
        return -1
    b = BeautifulSoup(r.text, "html.parser")
    if str(b) == "None":
        return -1
    t = str(b.find(class_="pagination pagination-small pagination-centered"))
    mi = 1
    vis = 0
    for i in t[::-1]:
        if "0" <= i and i <= "9":
            lastpage += (ord(i) - ord("0")) * mi
            mi *= 10
            vis = 1
        elif vis:
            if i == '"':
                break
            else:
                vis = 0
                lastpage = 0
                mi = 1


def getPage(search):
    global problem
    global cookies
    global lastpage
    global page
    problem = []
    url = (
        "https://gmoj.net/senior/index.php/main/problemset/"
        + str(page)
        + "?search="
        + search
    )
    try:
        r = requests.get(url, cookies=cookies, headers=headers)
    except:
        return -1
    b = BeautifulSoup(r.text, "html.parser").find(class_="problemset_table").table.tbody
    if str(b) == "None":
        return -1
    for i in b.find_all(style="height:0px"):
        j = 0
        problem.append(
            {
                "pid": i.find(class_="pid").a.text,
                "title": i.find(class_="title").a.text,
                "source": i.find(class_="source").text,
                "solvedCount": i.find(class_="solvedCount").a.span.text,
                "submitCount": i.find(class_="submitCount").a.span.text,
                "avg": i.find(class_="avg").a.span.text,
            }
        )


def downloadMatch(id):
    global cookies
    url = "https://gmoj.net/senior/index.php/contest/problems/" + str(id)
    try:
        r = requests.get(url, headers=headers, cookies=cookies)
    except:
        -1
    b = BeautifulSoup(r.text, "html.parser")
    if b.find(style="white-space: pre-wrap") != None:
        return -1
    b = b.find(id="contest_problems").tbody
    j = 0
    if not os.path.exists(savePath + "M" + str(id)):
        os.makedirs(savePath + "M" + str(id))
    if not os.path.exists(dataPath + "M" + str(id)):
        os.makedirs(dataPath + "M" + str(id))
    for i in b.find_all("tr"):
        uurl = (
            "https://gmoj.net/senior/index.php/contest/show/" + str(id) + "/" + str(j)
        )
        rr = requests.get(uurl, headers=headers, cookies=cookies)
        bb = BeautifulSoup(rr.text, "html.parser")
        title = str(bb.find("h4").string)
        if title != "(Standard IO)":
            title = bb.find("h4").find("span").string
            title = title[0 : title.find(".")]
        else:
            title = j
        if not os.path.exists(savePath + "M" + str(id) + "/" + str(title)):
            os.makedirs(savePath + "M" + str(id) + "/" + str(title))
        if not os.path.exists(dataPath + "M" + str(id) + "/" + str(title)):
            os.makedirs(dataPath + "M" + str(id) + "/" + str(title))
        # getMAnnex(id, "M" + str(id) + "/" + str(title))
        if bb.find(id="problem_description") == None:
            getMHtml(bb, str(title), "M" + str(id) + "/" + str(title) + "/")
        else:
            getMMarkdown(bb, str(title), "M" + str(id) + "/" + str(title) + "/")
        j += 1


def getMAnnex(id, path):
    url = "https://gmoj.net/senior/index.php/main/showdownload/" + str(id)
    try:
        r = requests.get(url, headers=headers, cookies=cookies)
    except:
        return -1
    b = BeautifulSoup(r.text, "html.parser").find(id="downloads").tbody
    if str(b) == "None":
        return -1
    for i in b.find_all("tr"):
        filename = i.find("td").find_next("td").a.text
        download_url = "https://gmoj.net/senior/" + str(
            i.find("td").find_next("td").a.get("href")
        )
        r = requests.get(download_url, headers=headers, cookies=cookies)
        with open(savePath + path + filename, "w+", encoding="utf-8") as f:
            f.write(r.text)


def getMHtml(b, title, folder):  # 获取比赛题目题面
    for i in b.find_all(class_="btn btn-mini btn_copy"):
        i.decompose()  # 排除不需要内容
    b.find(class_="navbar").decompose()
    vis = 0
    x = 1
    for i in b.find_all(class_="sample_pre sample_pre_borderless"):
        if not vis:
            if not os.path.exists(dataPath + folder):
                os.makedirs(dataPath + folder)
            with open(
                dataPath + folder + title + "_" + str(x) + ".in", "w+", encoding="utf-8"
            ) as f:
                f.write(i.text)
            with open(
                dataPath + folder + title + "_" + str(x) + ".in", "r+", encoding="utf-8"
            ) as f:
                with open(
                    savePath + folder + title + "_" + str(x) + ".in",
                    "w+",
                    encoding="utf-8",
                ) as ff:
                    ss = f.readlines()
                    for s in ss:
                        if s == "\n" or s == "" or s == " " or s == " \n":
                            continue
                        else:
                            ff.write(s)

            vis = 1
        else:
            with open(
                dataPath + folder + title + "_" + str(x) + ".ans",
                "w+",
                encoding="utf-8",
            ) as f:
                f.write(i.text)
            with open(
                dataPath + folder + title + "_" + str(x) + ".ans",
                "r+",
                encoding="utf-8",
            ) as f:
                with open(
                    savePath + folder + title + "_" + str(x) + ".ans",
                    "w+",
                    encoding="utf-8",
                ) as ff:
                    ss = f.readlines()
                    for s in ss:
                        if s == "\n" or s == "" or s == " " or s == " \n":
                            continue
                        else:
                            ff.write(s)

            vis = 1
    with open(dataPath + folder + title + ".html", "w+", encoding="utf-8") as f:
        f.write("<head>\n")
        f.write('  <meta charset="utf-8">\n')
        f.write("</head>\n")  # 写入编码
        f.write(str(b))
    htmlToPdf(
        dataPath + folder + title + ".html", savePath + folder + title + ".pdf"
    )  # 转换pdf


def getMMarkdown(b, title, folder):  # 获取markdown题面
    cls = os.system("cls")
    head = b.find(style="text-align: center")
    body = b.find(id="problem_show_container")
    problem = body.script.text
    with open(dataPath + folder + title + ".txt", "w+", encoding="utf-8") as f:
        f.write(problem)
    with open(savePath + folder + title + ".md", "w+", encoding="utf-8") as f:
        f.write("# " + head.h2.text + "\n\n")
        f.write(str(head.h4) + "\n\n")
        sampleData = body.find(class_="div_samplecase")
        timeLimits = (
            head.find(id="problem_judge_details")
            .find("span")
            .find(class_="badge badge-info")
        )
        memeryLimits = timeLimits.find_next("span").find(class_="badge badge-info")
        f.write("Time Limits: " + timeLimits.text + "\n\n")
        f.write("Memory Limits: " + memeryLimits.text + "\n\n")
        vis1 = vis2 = 0
        with open(dataPath + folder + title + ".txt", "r", encoding="utf-8") as ff:
            text = ff.readlines()
            for i in text:
                if i.find("problem_description") != -1:
                    f.write("## Problem Description\n\n")
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 3]
                    f.write(s + "\n")
                    continue
                elif i.find("input_description") != -1 and not vis1:
                    f.write("## Input\n\n")
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 3]
                    f.write(s + "\n")
                    vis1 = 1
                    continue
                elif i.find("output_description") != -1 and not vis2:
                    f.write("## Output\n\n")
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 3]
                    f.write(s + "\n")
                    vis2 = 1
                    f.write("## Sample Data\n\n")
                    bb = 1
                    visin = 1
                    for j in sampleData.find_all(class_="div_samplecase_plaintext"):
                        for k in j.find_all("div"):
                            f.write("##### " + k.h5.span.text + "\n```\n")
                            f.write(k.pre.text + "\n```\n")
                            if visin:
                                with open(
                                    savePath + folder + title + "_" + str(bb) + ".in",
                                    "w+",
                                    encoding="utf-8",
                                ) as fff:
                                    fff.write(k.pre.text)
                                visin = 0
                            else:
                                with open(
                                    savePath + folder + title + "_" + str(bb) + ".ans",
                                    "w+",
                                    encoding="utf-8",
                                ) as fff:
                                    fff.write(k.pre.text)
                                bb += 1
                                visin = 1
                    for j in sampleData.find_all(class_="div_samplecase_markdown"):
                        f.write("##### " + j.h5.text + "\n")
                        f.write(j.div.get("data-markdown") + "\n")
                    continue
                elif i.find("data_constraint") != -1:
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 3]
                    if s == "":
                        continue
                    f.write("## Data Constraint\n\n")
                    f.write(s + "\n")
                    continue
                elif i.find("hint") != -1:
                    s = str(i.encode("utf-8").decode("unicode-escape"))
                    s = s.replace("\/", "/")
                    s = s[s.find('"') + 1 : len(s) - 7]
                    if s == "":
                        continue
                    f.write("## Hint\n\n")
                    f.write(s + "\n")
                    continue


def load_json():
    global json_path
    global js
    global default_user
    global users
    js = {"default_user": "", "users": []}
    if os.path.exists(json_path) == 0 or os.path.getsize(json_path) == 0:
        with open(json_path, "w+", encoding="utf-8") as f:
            json.dump(js, f, indent=4, ensure_ascii=False)
        return 0
    with open(json_path, "r", encoding="utf8") as f:
        js = json.load(f)
    default_user = js["default_user"]
    users = js["users"]
    for i in users:
        if i["username"] == default_user:
            if not login(default_user, base64Decry(i["password"])):
                default_user = ""
            break


class MyMainWindow(QMainWindow, Ui_ghelper):  # 这里也要记得
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.acSavePath.triggered.connect(self.ac_SavePath)
        self.acClear.triggered.connect(self.ac_Clear)
        # self.laUser = QLabel(self)
        self.laUser.setText(
            "用户：" + ("未登录" if default_user == "" else default_user)
        )  # 当前用户
        self.pubUser.clicked.connect(self.pub_User)  # 用户
        self.pubManegerUser.clicked.connect(self.pub_ManegerUser)  # 用户_用户管理
        self.tw_MangerUser()  # 用户_用户管理
        self.pubCreateUser.clicked.connect(self.pub_CreateUser)  # 用户_新建用户
        self.pubCreate.clicked.connect(self.pub_Create)  # 用户_新建用户_新建
        self.lePassword.returnPressed.connect(self.le_Password)  # 用户_新建用户_密码
        self.pubDownloadProblem.clicked.connect(self.pub_DownloadProblem)  # 题目下载
        self.lePId.returnPressed.connect(self.le_PId)  # 题目下载_题目id
        self.pubPSearch.clicked.connect(self.pub_PSearch)  # 题目下载_搜索
        self.lePSearch.returnPressed.connect(self.le_PSearch)  # 题目下载_搜索
        self.lePSearch.setPlaceholderText("用'|'分割关键字")
        self.lePPage.setPlaceholderText("输入页码")
        self.pubPCheckAll.clicked.connect(self.pub_PCheckAll)  # 题目下载_全选
        self.pubPCheckReverse.clicked.connect(self.pub_PCheckReverse)  # 题目下载_反选
        self.pubPUpPage.clicked.connect(self.pub_PUpPage)  # 题目下载_上一页
        self.pubPDownPage.clicked.connect(self.pub_PDownPage)  # 题目下载_下一页
        self.pubPJump.clicked.connect(self.pub_PJump)  # 题目下载_跳转
        self.lePPage.returnPressed.connect(self.le_PPage)  # 题目下载_页码
        self.pubPDownload.clicked.connect(self.pub_PDownload)  # 题目下载_下载
        self.pubDownloadMatch.clicked.connect(self.pub_DownloadMatch)  # 比赛下载
        self.leMId.returnPressed.connect(self.le_MId)  # 题目下载_题目id
        self.pubMDownload.clicked.connect(self.pub_MDownload)  # 题目下载_下载

    def ac_SavePath(self):
        global savePath
        newSavePath = ""
        newSavePath = QFileDialog.getExistingDirectory(
            self, "选择下载数据保存目录", newSavePath
        )
        if newSavePath != "":
            savePath = newSavePath + "/"

    def ac_Clear(self):
        shutil.rmtree(dataPath)
        os.makedirs(dataPath)

    def pub_User(self):
        self.main.setCurrentIndex(0)

    def pub_ManegerUser(self):
        self.swUser.setCurrentIndex(0)

    def tw_MangerUser(self):
        self.twMangerUser.setRowCount(len(users))
        self.twMangerUser.setColumnCount(2)
        self.twMangerUser.setHorizontalHeaderLabels(["用户名", "操作"])
        self.twMangerUser.setColumnWidth(0, 200)
        self.twMangerUser.setColumnWidth(1, 260)
        self.twMangerUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.twMangerUser.setSelectionMode(QAbstractItemView.NoSelection)
        self.twMangerUser.verticalHeader().setVisible(False)
        for i in range(len(users)):
            self.twMangerUser.setItem(i, 0, QTableWidgetItem(users[i]["username"]))
        for i in range(len(users)):
            self.twMangerUser.setCellWidget(i, 1, self.user_button(i))

    def user_button(self, row):
        widget = QWidget()
        self.pubChoose = QPushButton("选择")
        self.pubChoose.setStyleSheet(
            """ text-align : center;
                                    background-color :  DarkSeaGreen;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; """
        )
        self.pubChoose.setProperty("row", row)
        self.pubChoose.clicked.connect(self.pub_Choose)
        self.pubUpdate = QPushButton("修改")
        self.pubUpdate.setStyleSheet(
            """ text-align : center;
                                          background-color : NavajoWhite;
                                          height : 30px;
                                          border-style: outset;
                                          font : 13px  """
        )
        self.pubUpdate.setProperty("row", row)
        self.pubUpdate.clicked.connect(self.pub_UpdateUser)
        self.pubDelete = QPushButton("删除")
        self.pubDelete.setStyleSheet(
            """ text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; """
        )
        self.pubDelete.setProperty("row", row)
        self.pubDelete.clicked.connect(self.pub_Delete)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.pubChoose)
        hLayout.addWidget(self.pubUpdate)
        hLayout.addWidget(self.pubDelete)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def pub_Choose(self):
        global js
        global default_user
        global users
        sender = self.sender()
        row = sender.property("row")
        username = users[row]["username"]
        password = base64Decry(users[row]["password"])
        if login(username, password):
            default_user = username
            js["default_user"] = username
            self.laUser.setText("用户：" + default_user)
            with open(json_path, "w+", encoding="utf-8") as f:
                json.dump(js, f, indent=4, ensure_ascii=False)
            QMessageBox.information(
                self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes
            )
        else:
            QMessageBox.information(
                self,
                "提示",
                "失败，用户名和密码不匹配",
                QMessageBox.Yes | QMessageBox.Yes,
            )

    def pub_UpdateUser(self):
        global js
        global default_user
        global users
        sender = self.sender()
        row = sender.property("row")
        username = users[row]["username"]
        value, ok = QInputDialog.getText(
            self, "请输入新密码", "请输入密码:", QLineEdit.Password, ""
        )
        if ok:
            new_password = value
            if login(username, new_password):
                users[row]["password"] = base64Encry(new_password)
                js["users"] = users
                with open(json_path, "w+", encoding="utf-8") as f:
                    json.dump(js, f, indent=4, ensure_ascii=False)
                QMessageBox.information(
                    self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes
                )
            else:
                QMessageBox.information(
                    self,
                    "提示",
                    "失败，用户名和密码不匹配",
                    QMessageBox.Yes | QMessageBox.Yes,
                )

    def pub_Delete(self):
        global js
        global default_user
        global users
        sender = self.sender()
        row = sender.property("row")
        ok = QMessageBox.information(
            self,
            "提示",
            "确认要删除吗？",
            QMessageBox.Yes | QMessageBox.Yes,
            QMessageBox.No,
        )
        if ok == QMessageBox.Yes:
            if default_user == users[row]["username"]:
                default_user = ""
                self.laUser.setText("用户：未登录！")
            del users[row]
            js["users"] = users
            js["default_user"] = default_user
            with open(json_path, "w+", encoding="utf-8") as f:
                json.dump(js, f, indent=4, ensure_ascii=False)
            self.laUser.setText("用户：" + default_user)
            QMessageBox.information(
                self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes
            )
            self.tw_MangerUser()

    def pub_CreateUser(self):
        self.swUser.setCurrentIndex(1)

    def pub_Create(self):
        global default_user
        global users
        username = str(self.leUsername.text())
        password = str(self.lePassword.text())
        for user in users:
            if user["username"] == username:
                QMessageBox.information(
                    self, "提示", "用户名已存在", QMessageBox.Yes | QMessageBox.Yes
                )
                return 0
        if login(username, password):
            default_user = username
            users.append({"username": username, "password": base64Encry(password)})
            js["default_user"] = username
            js["users"] = users
            self.laUser.setText("用户：" + default_user)
            with open(json_path, "w+", encoding="utf-8") as f:
                json.dump(js, f, indent=4, ensure_ascii=False)
            self.leUsername.setText("")
            self.lePassword.setText("")
            QMessageBox.information(
                self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes
            )
            self.tw_MangerUser()
        else:
            QMessageBox.information(
                self,
                "提示",
                "失败，用户名和密码不匹配",
                QMessageBox.Yes | QMessageBox.Yes,
            )

    def le_Password(self):
        global default_user
        global users
        username = str(self.leUsername.text())
        password = str(self.lePassword.text())
        for user in users:
            if user["username"] == username:
                QMessageBox.information(
                    self, "提示", "用户名已存在", QMessageBox.Yes | QMessageBox.Yes
                )
                return 0
        if login(username, password):
            default_user = username
            users.append({"username": username, "password": base64Encry(password)})
            js["default_user"] = username
            js["users"] = users
            self.laUser.setText("用户：" + default_user)
            with open(json_path, "w+", encoding="utf-8") as f:
                json.dump(js, f, indent=4, ensure_ascii=False)
            self.leUsername.setText("")
            self.lePassword.setText("")
            QMessageBox.information(
                self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes
            )
            self.tw_MangerUser()
        else:
            QMessageBox.information(
                self,
                "提示",
                "失败，用户名和密码不匹配",
                QMessageBox.Yes | QMessageBox.Yes,
            )

    def pub_DownloadProblem(self):
        self.main.setCurrentIndex(1)

    def le_PId(self):
        try:
            problemId = int(self.lePId.text())
        except:
            self.lePId.setText("")
            return -1
        if downloadProblem(problemId) == -1 or problemId == None:
            self.lePId.setText("")
            return -1
        QMessageBox.information(self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes)
        self.lePId.setText("")
        return 0

    def pub_PSearch(self):
        global search
        global lastpage
        global page
        search = str(self.lePSearch.text())
        searchProblem(search)
        getPage(search)
        self.laPPage.setText("第" + str(page) + "页,共" + str(lastpage) + "页")
        self.slePSearch()

    def le_PSearch(self):
        global search
        global page
        search = str(self.lePSearch.text())
        searchProblem(search)
        getPage(search)
        self.laPPage.setText("第" + str(page) + "页,共" + str(lastpage) + "页")
        self.slePSearch()

    def slePSearch(self):
        self.twP.setRowCount(0)
        self.twP.setColumnCount(0)
        self.twP.setRowCount(len(problem))
        self.twP.setColumnCount(7)
        self.twP.setHorizontalHeaderLabels(
            ["选择", "pid", "题目名", "来源", "AC", "提交", "平均分"]
        )
        self.twP.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.twP.setSelectionMode(QAbstractItemView.NoSelection)
        self.twP.verticalHeader().setVisible(False)
        self.twP.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        for i in range(len(problem)):
            self.check = QTableWidgetItem()
            self.check.setCheckState(Qt.Unchecked)  # 把checkBox设为未选中状态
            self.twP.setItem(i, 0, self.check)
        for i in range(len(problem)):
            self.twP.setItem(i, 1, QTableWidgetItem(problem[i]["pid"]))
        for i in range(len(problem)):
            self.twP.setItem(i, 2, QTableWidgetItem(problem[i]["title"]))
        for i in range(len(problem)):
            self.twP.setItem(i, 3, QTableWidgetItem(problem[i]["source"]))
        for i in range(len(problem)):
            self.twP.setItem(i, 4, QTableWidgetItem(problem[i]["solvedCount"]))
        for i in range(len(problem)):
            self.twP.setItem(i, 5, QTableWidgetItem(problem[i]["submitCount"]))
        for i in range(len(problem)):
            self.twP.setItem(i, 6, QTableWidgetItem(problem[i]["avg"]))

    def pub_PCheckAll(self):
        for i in range(len(problem)):
            self.twP.item(i, 0).setCheckState(Qt.Checked)

    def pub_PCheckReverse(self):
        for i in range(len(problem)):
            if self.twP.item(i, 0).checkState() == Qt.Checked:
                self.twP.item(i, 0).setCheckState(Qt.Unchecked)
            else:
                self.twP.item(i, 0).setCheckState(Qt.Checked)

    def pub_PUpPage(self):
        global page
        global search
        if page > 1:
            page -= 1
        getPage(search)
        self.laPPage.setText("第" + str(page) + "页,共" + str(lastpage) + "页")
        self.slePSearch()

    def pub_PDownPage(self):
        global page
        global lastpage
        global search
        if page < lastpage:
            page += 1
        getPage(search)
        self.laPPage.setText("第" + str(page) + "页,共" + str(lastpage) + "页")
        self.slePSearch()

    def pub_PJump(self):
        global page
        global lastpage
        global search
        newPage = 0
        try:
            newPage = int(self.lePPage.text())
        except:
            self.lePPage.setText("")
            return -1
        if 0 < newPage and newPage <= lastpage:
            page = newPage
        self.lePPage.setPlaceholderText("输入页码")
        self.laPPage.setText("第" + str(page) + "页,共" + str(lastpage) + "页")
        getPage(search)
        self.slePSearch()

    def le_PPage(self):
        global page
        global lastpage
        global search
        newPage = 0
        try:
            newPage = int(self.lePPage.text())
        except:
            self.lePPage.setText("")
            return -1
        if 0 < newPage and newPage <= lastpage:
            page = newPage
        self.lePPage.setPlaceholderText("输入页码")
        self.laPPage.setText("第" + str(page) + "页,共" + str(lastpage) + "页")
        getPage(search)
        self.slePSearch()

    def pub_PDownload(self):
        if str(self.lePId.text()) != "":
            try:
                problemId = int(self.lePId.text())
            except:
                self.lePId.setText("")
                return -1
            if downloadProblem(problemId) == -1 or problemId == None:
                self.lePId.setText("")
                return -1
            QMessageBox.information(
                self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes
            )
            self.lePId.setText("")
            return 0
        if len(problem) == 0:
            return -1
        self.prbPDownload.setRange(0, 100)
        sum = 0
        for i in range(len(problem)):
            if self.twP.item(i, 0).checkState() == Qt.Checked:
                sum += 1
        for i in range(len(problem)):
            if self.twP.item(i, 0).checkState() == Qt.Checked:
                problemId = self.twP.item(i, 1).text()
                downloadProblem(problemId)
                self.prbPDownload.setValue(int(100 / sum * (i + 1)))
        QMessageBox.information(self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes)
        self.prbPDownload.reset()

    def pub_DownloadMatch(self):
        self.main.setCurrentIndex(2)

    def le_MId(self):
        matchId = 0
        try:
            matchId = int(self.leMId.text())
        except:
            self.leMId.setText("")
            return -1
        if downloadMatch(matchId) == -1:
            self.leMId.setText("")
            return -1
        QMessageBox.information(self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes)
        self.leMId.setText("")

    def pub_MDownload(self):
        matchId = 0
        try:
            matchId = int(self.leMId.text())
        except:
            self.leMId.setText("")
            return -1
        if downloadMatch(matchId) == -1:
            self.leMId.setText("")
            return -1
        QMessageBox.information(self, "提示", "成功", QMessageBox.Yes | QMessageBox.Yes)
        self.leMId.setText("")


if __name__ == "__main__":
    load_json()
    exePath = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"
    dataPath = exePath + "data/"
    savePath = os.getcwd() + "/"
    os.chdir(exePath)
    if not os.path.exists("data"):
        os.makedirs("data")
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
