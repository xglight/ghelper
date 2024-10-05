from markdown import markdown
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Ui_home import Ui_home
from Ui_user import Ui_user
from Ui_login import Ui_login
from Ui_problem import Ui_problem
import requests
from bs4 import *
import base64
import os
import re
import pdfkit
import shutil
from loguru import *


def base64Encry(plaintext):  # base64加密
    logger.debug("base64 encryption work.")
    base64Encry = str(base64.b64encode(plaintext.encode("utf-8")))
    return base64Encry[base64Encry.find("'") + 1: len(base64Encry) - 1]


def base64Decry(ciphertext):  # base64解密
    logger.debug("base64 decryption work.")
    base64Decry = (base64.b64decode(ciphertext)).decode("utf-8")
    return str(base64Decry)


wkhtmltopdf_installed = False


def load_json():
    logger.debug("json loading.")
    global wkhtmltopdf_installed
    global username
    global password
    global js
    global login_success
    js = {"user": {"username": "", "password": ""}}
    if not os.path.exists("config"):
        os.mkdir("config")
    if os.path.exists(user_path) == 0 or os.path.getsize(user_path) == 0:
        with open(user_path, "w+", encoding="utf-8") as f:
            json.dump(js, f, indent=4, ensure_ascii=False)
        return 0
    with open(user_path, "r", encoding="utf-8") as f:
        js = json.load(f)
    username = base64Decry(js["user"]["username"])
    password = base64Decry(js["user"]["password"])
    if login(username, password) == 0:
        username = password = ""
    else:
        login_success = True

    environment_path = os.environ["PATH"]
    path = ""
    wkhtmltopdf_installed = False
    for i in environment_path:
        if i == ";":
            if os.path.exists(path) == 0:
                continue
            for i in os.listdir(path):
                if i == "wkhtmltopdf.exe":
                    cfg.set(cfg.wkhtmltopdf, path+"/")
                    wkhtmltopdf_installed = True
                    break
            if f == True:
                break
            path = ""
        else:
            path += i
    logger.debug("json loaded.")


def htmlToPdf(html, to_file):  # html转pdf
    logger.info("html to pdf work.")
    path_wkthmltopdf = (
        cfg.wkhtmltopdf.value+"/" + r"wkhtmltopdf.exe"  # 需外挂wkhtmltopdf.exe + "/"
    )
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit.from_file(html, to_file, configuration=pdfkit_config,
                     options={"encoding": "utf-8"})


config_path = "config/config.json"
user_path = "config/user.json"
js = ""
username = ""
password = ""
headers = {  # 请求头
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}
cookies = ""
login_success = False


def login(username, password):  # 发送登录请求
    logger.info("login request sent.")
    global cookies
    geturl = "https://gmoj.net/junior/index.php/main/home"  # 主地址（获取秘钥）
    try:
        r = requests.get(geturl, headers=headers, timeout=1)
    except:
        logger.error("login request failed.")
        return 0
    cookies = r.cookies  # 获取cookies，用于之后登录（cookies可保存登录状态）
    cookies = requests.utils.dict_from_cookiejar(cookies)  # cookies格式化
    b = BeautifulSoup(r.text, "html.parser")  # 用bs4处理get的信息
    if str(b) == "None":
        return 0
    secretkey = b.find("script").text  # 获取秘钥
    prekey = secretkey[secretkey.find("saltl") + 7: secretkey.find(";") - 1]
    lastkey = secretkey[
        secretkey.find("saltr") + 7: secretkey.find(";", secretkey.find("saltr")) - 1
    ]  # 制作密文
    posturl = "https://gmoj.net/senior/index.php/main/login"  # post登录地址
    postdata = {
        "username": username,
        "password": prekey + password + lastkey,
    }  # post数据
    try:
        pr = requests.post(
            posturl, cookies=cookies, headers=headers, data=postdata
        )  # 发送post登录请求
    except:
        logger.error("login request failed.")
        return 0
    if pr.status_code != 200:
        logger.warning("login failed.")
        return 0
    if pr.text != "success":
        logger.warning("login failed.")
        return 0
    logger.info("login success.")
    return pr.text == "success"  # 判断是否成功


class Demo(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.resize(900, 600)
        self.setWindowTitle("ghelper")
        self.setWindowIcon(QIcon("favicon.ico"))

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()
        self.createSubInterface()
        self.splashScreen.finish()
        self.close()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1000, loop.quit)
        loop.exec()


class Home(QMainWindow, Ui_home):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(" ", "-"))


name = ""


class User(QMainWindow, Ui_user):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        if login_success == False:
            self.login_error()
        self.Search_user.setPlaceholderText("输入用户名")
        self.Search_user.searchSignal.connect(self.cSearch_user)
        self.Search_user.returnPressed.connect(self.cSearch_user)
        self.setObjectName(text.replace(" ", "-"))
        global name
        if name == "":
            name = username
        self.work()

    def cSearch_user(self):
        global name
        name = str(self.Search_user.text())
        self.work()

    def work(self):
        global name
        logger.info("user search request sent. username: " + name)
        if login_success == False:
            self.login_error()
            return 0
        url = "https://gmoj.net/senior/index.php/users/"+name
        try:
            r = requests.get(url, headers=headers, cookies=cookies)
        except:
            logger.error("user search request failed. username: "+name)
            return 0
        b = BeautifulSoup(r.text, 'html.parser')
        if b.find("p") != None:
            self.find_error()
            logger.warning("user not found. username: "+name)
            return 0
        self.find_success()
        logger.info("user found. username: "+name)
        # init
        self.Description.setText("")
        # Blog
        if b.find(class_="btn btn-small btn-info") != None:
            self.Link_blog.show()
            self.Link_blog.setText("Blog")
            self.Link_blog.setUrl(
                b.find(class_="btn btn-small btn-info")["href"])
        else:
            self.Link_blog.hide()
        # Avatar
        data = b.find("img")["src"]
        if data == "":
            self.Avatar.setImage("default_avatar.png")
        else:
            try:
                r = requests.get(data, headers=headers)
            except:
                logger.error("avatar request failed. username: "+name)
            if r.status_code != 200:
                self.Avatar.setImage("default_avatar.png")
            else:
                with open(str(cfg.get(cfg.cacheFolder))+'/'+str(name)+"_avator.png", "wb") as f:
                    f.write(r.content)
                self.Avatar.setImage(
                    cfg.get(cfg.cacheFolder)+'/'+name+"_avator.png")
        self.Avatar.setBorderRadius(8, 8, 8, 8)
        self.Avatar.scaledToHeight(255)
        # info
        data = b.find_all("dd")
        j = 1
        for i in data:
            if j == 1:
                self.uid.setText(i.span.text)
            elif j == 2:
                self.Username.setText(i.span.text)
            elif j == 4:
                self.Rank.setText(i.span.text)
            elif j == 5:
                self.AC_problems.setText(i.a.span.text)
            elif j == 6:
                self.Solve.setText(i.a.span.text)
            elif j == 7:
                self.Submit.setText(i.a.span.text)
            elif j == 8:
                self.Rate.setText(i.span.text)
            elif j == 9:
                self.Description.setText(i.text)
            j += 1

    def find_error(self):
        InfoBar.error(
            title="失败",
            content=f"未找到用户",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )

    def find_success(self):
        InfoBar.success(
            title="成功",
            content=f"用户 {name} 已找到！",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self,
        )

    def login_error(self):
        InfoBar.error(
            title="错误",
            content=f"请先登录！",
            orient=Qt.Horizontal,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self,
        )


class Config(QConfig):
    # download
    downloadFolder = ConfigItem(
        "Folders", "Download", "download", FolderValidator())
    cacheFolder = ConfigItem("Folders", "Cache", "cache", FolderValidator())
    wkhtmltopdf = ConfigItem(
        "Folders", "Wkhtmltopdf", "Wkhtmltopdf", FolderValidator())

    # log
    loglevel = OptionsConfigItem(
        "Log", "Loglevel", 20, OptionsValidator([10, 20, 30, 40, 50]))


class SettingInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = TitleLabel("设置", self)
        self.Download = SettingCardGroup("下载", self.scrollWidget)
        self.download = PushSettingCard(
            "选择文件夹",
            FIF.DOWNLOAD,
            "下载目录",
            cfg.get(cfg.downloadFolder),
            self.Download,
        )
        self.cache = PushSettingCard(
            "选择文件夹",
            FIF.DOWNLOAD,
            "缓存目录",
            cfg.get(cfg.cacheFolder),
            self.Download,
        )
        self.wkhtmltopdf = PushSettingCard(
            "选择文件夹",
            FIF.DOWNLOAD,
            "Wkhtmltopdf",
            cfg.get(cfg.wkhtmltopdf),
            self.Download,
        )

        self.storage = SettingCardGroup("存储", self.scrollWidget)
        self.clearcache = PrimaryPushSettingCard(
            text="清空",
            icon=FIF.DELETE,
            title="清空缓存",
            content="清理程序的缓存文件 (cache)"
        )
        self.cleardownload = PrimaryPushSettingCard(
            text="清空",
            icon=FIF.DELETE,
            title="清空下载",
            content="清理程序的下载文件 (download)"
        )

        self.log = SettingCardGroup("日志", self.scrollWidget)
        self.clearlog = PrimaryPushSettingCard(
            text="清空",
            icon=FIF.DELETE,
            title="清空日志",
            content="清理程序的日志文件 (log)"
        )
        self.loglevel = ComboBoxSettingCard(
            configItem=cfg.loglevel,
            icon=FIF.SETTING,
            title="日志等级",
            content="日志记录等级",
            texts=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(900, 550)
        self.scrollWidget.setLayout(self.expandLayout)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 35, 0, 0)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(10, 0)

        self.Download.addSettingCard(self.download)
        self.Download.addSettingCard(self.cache)
        self.Download.addSettingCard(self.wkhtmltopdf)

        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(30, 10, 60, 0)
        self.expandLayout.addWidget(self.Download)

        self.storage.addSettingCard(self.clearcache)
        self.storage.addSettingCard(self.cleardownload)

        self.expandLayout.addWidget(self.storage)

        self.log.addSettingCard(self.clearlog)
        self.log.addSettingCard(self.loglevel)

        self.expandLayout.addWidget(self.log)

    def cdownload(self):
        logger.debug("download folder selected.")
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.download.setContent(folder)

    def ccache(self):
        logger.debug("cache folder selected.")
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if not folder or cfg.get(cfg.cacheFolder) == folder:
            return

        cfg.set(cfg.cacheFolder, folder)
        self.cache.setContent(folder)

    def cwkhtmltopdf(self):
        logger.debug("wkhtmltopdf folder selected.")
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if not folder or cfg.get(cfg.wkhtmltopdf) == folder:
            return
        for i in os.listdir(folder):
            if i.find("wkhtmltopdf.exe") != -1:
                self.find_success()
                cfg.set(cfg.wkhtmltopdf, folder)
                self.wkhtmltopdf.setContent(folder)
                return 1
        self.find_error()
        return 0

    def clear_cache(self):
        logger.debug("clear cache.")
        if QMessageBox.question(self, "警告", "确定要清空缓存吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            for i in os.listdir(cfg.get(cfg.cacheFolder)):
                if os.path.isfile(cfg.get(cfg.cacheFolder) + "/" + i):
                    os.remove(cfg.get(cfg.cacheFolder) + "/" + i)
                else:
                    shutil.rmtree(cfg.get(cfg.cacheFolder) + "/" + i)
            InfoBar.success(
                title="成功",
                content=f"缓存已清空！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )

    def clear_download(self):
        logger.debug("clear download.")
        if QMessageBox.question(self, "警告", "确定要清空下载吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            for i in os.listdir(cfg.get(cfg.downloadFolder)):
                if os.path.isfile(cfg.get(cfg.downloadFolder) + "/" + i):
                    os.remove(cfg.get(cfg.downloadFolder) + "/" + i)
                else:
                    shutil.rmtree(cfg.get(cfg.downloadFolder) + "/" + i)
            InfoBar.success(
                title="成功",
                content=f"下载已清空！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )

    def clear_log(self):
        logger.debug("clear log.")
        if QMessageBox.question(self, "警告", "确定要清空日志吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            for i in os.listdir("logs"):
                try:
                    os.remove("logs" + "/" + i)
                except:
                    pass
            InfoBar.success(
                title="成功",
                content=f"日志已清空！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )

    def __connectSignalToSlot(self):
        self.download.clicked.connect(self.cdownload)
        self.cache.clicked.connect(self.ccache)
        self.wkhtmltopdf.clicked.connect(self.cwkhtmltopdf)
        self.clearcache.clicked.connect(self.clear_cache)
        self.cleardownload.clicked.connect(self.clear_download)
        self.clearlog.clicked.connect(self.clear_log)

    def find_error(self):
        InfoBar.error(
            title="失败",
            content=f"未找到可用的 wkhtmltopdf.exe",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )

    def find_success(self):
        InfoBar.success(
            title="成功",
            content=f"wkhtmltopdf.exe 已就绪",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )


class Setting(QMainWindow):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.settingIterface = SettingInterface(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.settingIterface)
        self.setLayout(self.hBoxLayout)
        self.resize(900, 600)
        self.setObjectName(text.replace(" ", "-"))


class HTMLView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("HTML Viewer")
        self.resize(1000, 800)
        self.broswer = QWebEngineView()
        self.broswer.load(QUrl.fromLocalFile("problem.html"))
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.broswer)
        self.setLayout(self.hBoxLayout)


class Problem(QMainWindow, Ui_problem):
    lastpage = 0
    page = 0
    search = ""
    Problem = []

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        if login_success == False:
            self.login_error()
        self.Problem.itemClicked.connect(self.check_problem)
        self.Search_problem.setPlaceholderText("搜索")
        self.Search_problem.searchSignal.connect(self.search_problem)
        self.Search_problem.returnPressed.connect(self.search_problem)
        self.Choose_all.clicked.connect(self.check_all)
        self.Choose_reverse.clicked.connect(self.check_reverse)
        self.Jump_up.clicked.connect(self.jump_up)
        self.Jump_down.clicked.connect(self.jump_down)
        self.Jump.clicked.connect(self.jump_page)
        self.Problem_download.clicked.connect(self.download_problem)
        self.setObjectName(text.replace(" ", "-"))
        self.Problem.cellDoubleClicked.connect(self.open_problem)
        self.search_problem()

    def download_problem(self):
        global cookies
        global headers
        global wkhtmltopdf_installed
        if wkhtmltopdf_installed == False:
            self.find_error()
            return 0
        if len(Problem.problem_set) == 0:
            return 0
        pid_list = []
        for i in range(len(Problem.problem_set)):
            if self.Problem.item(i, 0).checkState() == Qt.Checked:
                pid = Problem.problem_set[i]["pid"]
                pid_list.append(pid)
        if len(pid_list) == 0:
            return 0
        self.ProgressBar.setRange(0, 100)
        self.ProgressBar.setValue(0)
        cnt = 0
        success = 0
        jump = 0
        error = 0
        for i in pid_list:
            if os.path.exists(self.cache_problem_path(i)) == False:
                if self.get_problem(i) == 1:
                    success += 1
                else:
                    error += 1
            else:
                jump += 1
            cnt += 1
            self.ProgressBar.setValue((int((1.0*cnt)/(1.0*len(pid_list))*100)))
        self.ProgressBar.setValue(100)
        self.download_success(success, jump, error)

    def find_error(self):
        InfoBar.error(
            title="失败",
            content=f"未找到可用的 wkhtmltopdf.exe",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )

    def download_success(self, success, jump, error):
        InfoBar.success(
            title="下载成功",
            content=f"成功：{success} 跳过：{jump} 失败：{error}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=4000,
            parent=self,
        )

    def search_problem(self):
        logger.info("problem search request sent. search: " + Problem.search)
        global cookies
        global headers
        Problem.search = str(self.Search_problem.text())
        url = "https://gmoj.net/senior/index.php/main/problemset?search=" + Problem.search
        try:
            r = requests.get(url, headers=headers, cookies=cookies)
        except:
            logger.error("problem search request failed.")
            return 0
        b = BeautifulSoup(r.text, "html.parser")
        with open("problem.html", "w", encoding="utf-8") as f:
            f.write(str(b))
        if str(b) == "None":
            return 0
        bb = str(b.find(class_="pagination pagination-small pagination-centered"))
        if b.find("em"):
            Problem.lastpage = 1
        mi = 1
        vis = 0
        for i in bb[::-1]:
            if "0" <= i and i <= "9":
                Problem.lastpage += int(ord(i) - ord("0")) * mi
                mi *= 10
                vis = 1
            elif vis:
                if i == '"':
                    break
                else:
                    vis = 0
                    Problem.lastpage = 0
                    mi = 1
        if Problem.lastpage == 0:
            return 0
        Problem.page = 1
        self.View_problem()

    def cache_problem_path(self, id):
        return cfg.cacheFolder.value+"\\" + str(id) + "\\"+"o_" + str(id) + ".html"

    def getPage(self):
        logger.info("get page work. page: " + str(Problem.page))
        global cookies
        global headers
        Problem.problem_set = []
        url = "https://gmoj.net/senior/index.php/main/problemset/" + \
            str(Problem.page) + "?search=" + Problem.search
        try:
            r = requests.get(url, headers=headers, cookies=cookies)
        except:
            logger.error("get page request failed.")
            return 0
        b = BeautifulSoup(r.text, "html.parser").find(
            class_="problemset_table").table.tbody
        for i in b.find_all(style="height:0px"):
            Problem.problem_set.append(
                {
                    "pid": i.find(class_="pid").a.text,
                    "title": i.find(class_="title").a.text,
                    "source": i.find(class_="source").text,
                    "solvedCount": i.find(class_="solvedCount").a.span.text,
                    "submitCount": i.find(class_="submitCount").a.span.text,
                    "avg": i.find(class_="avg").a.span.text,
                }
            )

    def View_problem(self):
        logger.debug("problem view work. page: " + str(Problem.page))
        self.getPage()
        if len(Problem.problem_set) == 0:
            return 0
        self.Problem.setRowCount(0)
        self.Problem.setColumnCount(0)
        self.Problem.setRowCount(len(Problem.problem_set))
        self.Problem.setColumnCount(7)
        self.Problem.setHorizontalHeaderLabels(
            ["选择", "pid", "题目名", "来源", "AC", "提交", "平均分"]
        )
        self.Problem.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Problem.setSelectionMode(QAbstractItemView.NoSelection)
        self.Problem.verticalHeader().setVisible(False)
        self.Problem.setColumnWidth(0, 35)
        self.Problem.setColumnWidth(1, 50)
        self.Problem.setColumnWidth(2, 260)
        self.Problem.setColumnWidth(3, 289)
        self.Problem.setColumnWidth(4, 60)
        self.Problem.setColumnWidth(5, 60)
        self.Problem.setColumnWidth(6, 60)
        Labels = ["pid", "title", "source",
                  "solvedCount", "submitCount", "avg"]
        for i in range(len(Problem.problem_set)):
            self.check = QTableWidgetItem()
            self.check.setCheckState(Qt.Unchecked)  # 把checkBox设为未选中状态
            self.Problem.setItem(i, 0, self.check)
            self.Problem.item(i, 0).setTextAlignment(Qt.AlignCenter)
            for j in range(1, 6+1):
                self.Problem.setItem(i, j, QTableWidgetItem(
                    Problem.problem_set[i][Labels[j-1]]))
                self.Problem.item(i, j).setTextAlignment(Qt.AlignCenter)

    def check_problem(self, item):
        logger.debug("problem check clicked. row: " + str(item.row()))
        h = item.row()
        if self.Problem.item(h, 0).checkState() == Qt.Checked:
            self.Problem.item(h, 0).setCheckState(Qt.Unchecked)
        else:
            self.Problem.item(h, 0).setCheckState(Qt.Checked)

    def jump_up(self):
        logger.debug("problem jump up clicked. page: " + str(Problem.page))
        if Problem.page > 1:
            Problem.page -= 1
            self.View_problem()

    def jump_down(self):
        logger.debug("problem jump down clicked. page: " + str(Problem.page))
        if Problem.page < Problem.lastpage:
            Problem.page += 1
            self.View_problem()

    def jump_page(self):
        logger.debug("problem jump page clicked. page: " + str(Problem.page))
        try:
            page = int(self.Jump_page.text())
            if page > 0 and page <= Problem.lastpage:
                Problem.page = page
                self.View_problem()
        except:
            pass

    def check_all(self):
        logger.debug("problem check all clicked.")
        for i in range(self.Problem.rowCount()):
            self.Problem.item(i, 0).setCheckState(Qt.Checked)

    def check_reverse(self):
        logger.debug("problem check reverse clicked.")
        for i in range(self.Problem.rowCount()):
            if self.Problem.item(i, 0).checkState() == Qt.Checked:
                self.Problem.item(i, 0).setCheckState(Qt.Unchecked)
            else:
                self.Problem.item(i, 0).setCheckState(Qt.Checked)

    def open_problem(self, row, column):
        logger.debug("problem open clicked. row: " +
                     str(row) + " column: " + str(column))
        if column == 2:
            pid = self.Problem.item(row, 1).text()
            self.get_problem(pid)
            win = HTMLView()
            win.broswer.load(QUrl.fromLocalFile(
                cfg.cacheFolder.value+"\\" + str(pid) + "\\" + str(pid) + ".html"))
            win.broswer.setWindowTitle(pid)
            win.show()
            win.exec_()

    def login_error(self):
        InfoBar.error(
            title="错误",
            content=f"找不到题目！",
            orient=Qt.Horizontal,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )

    def login_error(self):
        InfoBar.error(
            title="错误",
            content=f"请先登录！",
            orient=Qt.Horizontal,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self,
        )

    def get_problem(self, id):
        logger.info("problem get request sent. id: " + str(id))
        url = "https://gmoj.net/senior/index.php/main/show/" + id
        try:
            r = requests.get(url, headers=headers, cookies=cookies)
        except:
            logger.error("problem get request failed.")
            return 0
        b = BeautifulSoup(r.text, "html.parser")
        if str(b) == "None" or b.find(style="white-space: pre-wrap") != None:
            return 0
        title = str(b.find("h4").string)
        if title != "(Standard IO)":
            title = b.find("h4").find("span").string
            title = title[0: title.find(".")]
        else:
            title = id
        if not os.path.exists(cfg.cacheFolder.value+"\\" + str(id)):
            os.makedirs(cfg.cacheFolder.value + "\\" + str(id))
        title = str(title)
        with open(self.cache_problem_path(id), "w", encoding="utf-8") as f:
            f.write(str(b))
        if b.find(id="problem_description") == None:  # 判断是否为markdown
            if self.problem_html(id) == 1:
                return 1
        else:
            if self.problem_markdown(id) == 1:
                return 1
        logger.warning("problem get failed. id: " + str(id))
        return 0
        #     getMarkdown(b, str(title), str(title) + "/")
        # TODO: 增加markdown渲染功能

    example_in = []
    example_out = []
    example_explain = []

    def update_example(self, id, end, tt):
        if tt == "":
            return
        if end == 1:
            if id != 0:
                while len(example_explain) < id:
                    example_explain.append("")
                example_explain[id-1] = tt
            else:
                example_explain.append(tt)
        elif end == 2:
            if id != 0:
                while len(example_in) < id:
                    example_in.append("")
                example_in[id-1] = tt
            else:
                example_in.append(tt)
        elif end == 3:
            if id != 0:
                while len(example_out) < id:
                    example_out.append("")
                example_out[id-1] = tt
            else:
                example_out.append(tt)
        end = 0
        tt = ""

    def get_html_example(self, id):
        logger.debug("problem html example work. id: " + str(id))
        global example_in
        global example_out
        global example_explain
        example_in = []
        example_out = []
        example_explain = []
        b = ""
        with open(self.cache_problem_path(id), "r", encoding="utf-8") as f:
            b = f.read()
        b = BeautifulSoup(b, "html.parser")
        for i in b.find_all(class_="btn btn-mini btn_copy"):
            i.decompose()
        body = b.find(id="problem_show_container").find(
            id="mainbar").find(id="problem_main_content")
        cnt = 1
        end = 0  # 1:样例 2:输入 3:输出
        id = 0
        for i in body.find_all(class_="well"):
            if cnt == 4 or cnt == 5:
                text = i.fieldset.pre.text
                file = ""
                id = 0
                end = -1
                for line in text.splitlines():
                    if line == "" or line == " ":
                        continue
                    if (((line.find("Sample") != -1) or (line.find("样例") != -1) or (line.find("说明") != -1) or (line.find("输入") != -1) or (line.find("输出") != -1)) and (len(line) <= 7)):
                        self.update_example(id, end, file)
                        file = ""
                        end = -1
                        id = 0
                        if (line.find("Explanation") != -1 or line.find("说明") != -1 or line.find("解释") != -1):
                            end = 1
                        elif (line.find("Input") != -1 or line.find("输入") != -1):
                            end = 2
                        elif line.find("Output") != -1 or line.find("输出") != -1:
                            end = 3
                    else:
                        file = file + line + "\n"
                if end == -1:
                    end = 2 + (cnt == 5)
                self.update_example(id, end, file)
                end = 0
            cnt += 1
        return

    def get_markdown_example(self, id):
        logger.debug("problem markdown example work. id: " + str(id))
        global example_in
        global example_out
        global example_explain
        example_in = []
        example_out = []
        example_explain = []
        b = ""
        with open(self.cache_problem_path(id), "r", encoding="utf-8") as f:
            b = f.read()
        b = BeautifulSoup(b, "html.parser")
        for i in b.find_all(class_="btn btn-mini btn_copy"):
            i.decompose()
        body = b.find(id="problem_show_container").find(
            id="mainbar").find(id="problem_main_content")
        cnt = 1
        end = 0  # 1:样例 2:输入 3:输出
        id = 0
        for i in body.find(class_="div_samplecase_plaintext").find_all("div"):
            text = i.pre.text
            file = ""
            id = 0
            t = i.h5.span.text
            if (t.find("Explanation") != -1 or t.find("说明") != -1 or t.find("解释") != -1):
                end = 1
            elif (t.find("Input") != -1 or t.find("输入") != -1):
                end = 2
            elif t.find("Output") != -1 or t.find("输出") != -1:
                end = 3

            for line in text.splitlines():
                if line == "" or line == " ":
                    continue
                if (((line.find("Sample") != -1) or (line.find("样例") != -1) or (line.find("说明") != -1) or (line.find("输入") != -1) or (line.find("输出") != -1)) and (len(line) <= 7)):
                    self.update_example(id, end, file)
                    file = ""
                    end = -1
                    id = 0
                    cost = re.findall(r'[1-9]+\.?[0-9]*', line)
                    if len(cost) > 0:
                        id = int(cost[0])
                    if (line.find("Explanation") != -1 or line.find("说明") != -1 or line.find("解释") != -1):
                        end = 1
                    elif (line.find("Input") != -1 or line.find("输入") != -1):
                        end = 2
                    elif line.find("Output") != -1 or line.find("输出") != -1:
                        end = 3
                else:
                    file = file + line + "\n"
            self.update_example(id, end, file)
            end = 0
        return

    def problem_html(self, id):
        logger.info("problem html work. id: " + str(id))
        b = ""
        if not os.path.exists(cfg.downloadFolder.value+"\\" + str(id)):
            os.makedirs(cfg.downloadFolder.value + "\\" + str(id))
        if not os.path.exists(self.cache_problem_path(id)):
            return 0
        self.get_html_example(id)
        with open(self.cache_problem_path(id), "r", encoding="utf-8") as f:
            b = f.read()
        b = BeautifulSoup(b, "html.parser")
        for i in b.find_all(class_="btn btn-mini btn_copy"):
            i.decompose()
        all = b.find(class_="row-fluid")
        body = b.find(id="problem_show_container").find(
            id="mainbar").find(id="problem_main_content")
        head = all.find(style="text-align: center")
        title = head.find("h2").text
        with open(cfg.cacheFolder.value+"\\" + str(id) + "\\" + str(id) + ".html", "w+", encoding="utf-8") as f:
            f.write("<head>\n")
            f.write('  <meta charset="utf-8">\n')
            f.write('  <title>{0}</title>\n'.format(title))
            f.write("</head>\n")
            f.write("<body style=\"margin-left: 20%; margin-right: 20%;\">\n")
            f.write("<h2 style=\"text-align: center;\">{0}</h2>".format(title))
            if head.find("h4").find("span") != None:
                in_name = ""
                out_name = ""
                for i in head.find("h4").find_all("span"):
                    if in_name == "":
                        in_name = i.text
                    else:
                        out_name = i.text
                f.write("  <h4 style=\"text-align: center\">Input:<span style=\"color: red; font-weight: bold;\">{0}</span>,Output:<span style=\"color: red; font-weight: bold;\">{1}</span></h4>\n".format(
                    in_name, out_name))
            else:
                f.write("  <h4 style=\"text-align: center\">File IO</h4>\n")
            time_limit = 0
            memory_limit = 0
            for i in head.find(id="problem_judge_details").find_all("span"):
                if time_limit == 0:
                    company = ''.join(re.findall(r'[A-Za-z]', i.text))
                    number = re.sub('\D', '', i.text)
                    if company == 's' or company == 'S':
                        time_limit = int(number)*1000
                    else:
                        time_limit = int(number)
                else:
                    company = ''.join(re.findall(r'[A-Za-z]', i.text))
                    number = re.sub('\D', '', i.text)
                    if company == 'kb' or company == 'KB':
                        memory_limit = int(number)
                    else:
                        memory_limit = int(number)*1024
            f.write(
                "  <h4 style=\"text-align: center\">Time Limit: {0} ms, Memory Limit: {1} KB</h4>\n".format(time_limit, memory_limit))
            cnt = 1
            for i in body.find_all(class_="well"):
                if cnt == 1:
                    f.write("  <h4>题目描述</h4>\n")
                    f.write("  <p>\n")
                    f.write(str(i.fieldset.div))
                    f.write("  </p>\n")
                elif cnt == 2:
                    f.write("  <h4>输入格式</h4>\n")
                    f.write("  <p>\n")
                    f.write(str(i.fieldset.div))
                    f.write("  </p>\n")
                elif cnt == 3:
                    f.write("  <h4>输出格式</h4>\n")
                    f.write("  <p>\n")
                    f.write(str(i.fieldset.div))
                    f.write("  </p>\n")
                elif cnt == 4:
                    for j in range(len(example_in)):
                        f.write("  <h4>样例输入{0}</h4>\n".format(j+1))
                        f.write("  <pre>\n")
                        f.write(example_in[j])
                        f.write("  </pre>\n")
                        f.write("  <h4>样例输出{0}</h4>\n".format(j+1))
                        f.write("  <pre>\n")
                        if j < len(example_out):
                            f.write(example_out[j])
                        else:
                            f.write("---None---")
                        f.write("  </pre>\n")
                        if ((len(example_explain) > 0) and (int(len(example_explain)) > j)):
                            f.write("  <h4>样例解释{0}</h4>\n".format(j+1))
                            f.write(
                                "  <div class=\"test_div\" style=\"word-wrap:break-word;\">\n")
                            f.write(example_explain[j])
                            f.write("  </div>\n")
                elif cnt > 5:
                    f.write("  <h4>{0}</h4>\n".format(i.legend.h4.text))
                    f.write("  <p>\n")
                    f.write(str(i.fieldset.div))
                    f.write("  </p>\n")
                cnt += 1
        htmlToPdf(cfg.cacheFolder.value+"\\" + str(id) + "\\" + str(id) + ".html",
                  cfg.downloadFolder.value+"\\" + str(id) + "\\" + str(id) + ".pdf")
        return 1

    def problem_markdown(self, id):
        logger.info("problem markdown work. id: " + str(id))
        b = ""
        if not os.path.exists(cfg.downloadFolder.value+"\\" + str(id)):
            os.makedirs(cfg.downloadFolder.value + "\\" + str(id))
        if not os.path.exists(self.cache_problem_path(id)):
            return 0
        self.get_markdown_example(id)
        with open(self.cache_problem_path(id), "r", encoding="utf-8") as f:
            b = f.read()
        b = BeautifulSoup(b, "html.parser")
        for i in b.find_all(class_="btn btn-mini btn_copy"):
            i.decompose()
        all = b.find(class_="row-fluid")
        body = b.find(id="problem_show_container").find(
            id="mainbar").find(id="problem_main_content")
        head = all.find(style="text-align: center")
        title = head.find("h2").text
        script_tag = b.find('script', text=re.compile(r'const rawMarkdown'))
        script_content = script_tag.string
        raw_markdown_match = str(re.search(
            r"const rawMarkdown\s*=\s*(\{.*?\})", script_content, re.DOTALL).group(1))
        raw_markdown_var = re.findall(r".*:", raw_markdown_match)
        for i in raw_markdown_var:
            with open(cfg.cacheFolder.value+"/" + str(id) + "/" + "test" + ".md", "w+", encoding="utf-8") as f:
                f.write(str(i))
            i = i.replace(" ", "")
            raw_markdown_match = raw_markdown_match.replace(
                i, "\""+(i.replace(":", ""))+"\":")
        raw_markdown = json.loads(raw_markdown_match)
        title_var = ["problem_description", "input_description",
                     "output_description", "data", "hint"]
        title_name = ["题目描述", "输入格式", "输出格式", "数据范围", "提示"]
        with open(cfg.cacheFolder.value+"/" + str(id) + "/" + str(id) + ".html", "w+", encoding="utf-8") as f:
            f.write("<head>\n")
            f.write('  <meta charset="utf-8">\n')
            f.write('  <title>{0}</title>\n'.format(title))
            f.write("  <script>\n")
            f.write("    MathJax = {\n")
            f.write(
                "        tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]}\n")
            f.write("    };\n")
            f.write("  </script>\n")
            f.write("  <script id=\"MathJax-script\" async src=\"https://cdn.bootcdn.net/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js\">\n")
            f.write("  </script>\n")
            f.write("</head>\n")
            f.write("<body style=\"margin-left: 20%; margin-right: 20%;\">\n")
            f.write("<h2 style=\"text-align: center;\">{0}</h2>".format(title))
            if head.find("h4").find("span") != None:
                in_name = ""
                out_name = ""
                for i in head.find("h4").find_all("span"):
                    if in_name == "":
                        in_name = i.text
                    else:
                        out_name = i.text
                f.write("  <h4 style=\"text-align: center\">Input:<span style=\"color: red; font-weight: bold;\">{0}</span>,Output:<span style=\"color: red; font-weight: bold;\">{1}</span></h4>\n".format(
                    in_name, out_name))
            else:
                f.write("  <h4 style=\"text-align: center\">File IO</h4>\n")
            time_limit = 0
            memory_limit = 0
            for i in head.find(id="problem_judge_details").find_all("span"):
                if time_limit == 0:
                    company = ''.join(re.findall(r'[A-Za-z]', i.text))
                    number = re.sub('\D', '', i.text)
                    if company == 's' or company == 'S':
                        time_limit = int(number)*1000
                    else:
                        time_limit = int(number)
                else:
                    company = ''.join(re.findall(r'[A-Za-z]', i.text))
                    number = re.sub('\D', '', i.text)
                    if company == 'kb' or company == 'KB':
                        memory_limit = int(number)
                    else:
                        memory_limit = int(number)*1024
            f.write(
                "  <h4 style=\"text-align: center\">Time Limit: {0} ms, Memory Limit: {1} KB</h4>\n".format(time_limit, memory_limit))
            for i in title_var:
                if i in raw_markdown:
                    f.write(
                        "  <h4>{0}</h4>\n".format(title_name[title_var.index(i)]))
                    f.write("  <p>\n")
                    html = markdown(raw_markdown[i])
                    f.write(html)
                    f.write("  </p>\n")
                    if i == "output_description":
                        for j in range(len(example_in)):
                            f.write("  <h4>样例输入{0}</h4>\n".format(j+1))
                            f.write("  <pre>\n")
                            f.write(example_in[j])
                            f.write("  </pre>\n")
                            f.write("  <h4>样例输出{0}</h4>\n".format(j+1))
                            f.write("  <pre>\n")
                            f.write(example_out[j])
                            f.write("  </pre>\n")
                            if ((len(example_explain) > 0) and (int(len(example_explain)) > j)):
                                f.write("  <h4>样例解释{0}</h4>\n".format(j+1))
                                f.write(
                                    "  <div class=\"test_div\" style=\"word-wrap:break-word;\">\n")
                                f.write(example_explain[j])
                                f.write("  </div>\n")
            f.write("</body>\n")

        htmlToPdf(cfg.cacheFolder.value+"\\" + str(id) + "\\" + str(id) + ".html",
                  cfg.downloadFolder.value+"\\" + str(id) + "\\" + str(id) + ".pdf")
        return 1


class Login(QMainWindow, Ui_login):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.password.returnPressed.connect(self.cPassword)
        self.login.clicked.connect(self.cPassword)
        self.setObjectName(text.replace("", "-"))

    def cPassword(self):
        logger.info("login work.")
        global username, password, login_success
        name = str(self.username.text())
        _password = str(self.password.text())
        if login(name, _password):
            username = name
            password = _password
            js["user"]["username"] = base64Encry(username)
            js["user"]["password"] = base64Encry(password)
            with open(user_path, "w+", encoding="utf-8") as f:
                json.dump(js, f, indent=4, ensure_ascii=False)
            self.username.setText("")
            self.password.setText("")
            self.login_success(username)
            login_success = True
        else:
            self.login_error()

    def login_success(self, username):
        InfoBar.success(
            title="成功",
            content=f"用户 {username} 已登录！",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )

    def login_error(self):
        InfoBar.error(
            title="失败",
            content=f"用户名与密码不匹配！",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )


class Window(FluentWindow):
    """主界面"""

    def __init__(self):
        super().__init__()
        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Home("主页", self)
        self.userInterface = User("用户", self)
        self.problemInterface = Problem('题目', self)
        self.settingInterface = Setting("设置", self)
        self.loginInterface = Login("登录", self)
        # self.contestInterface = Home('比赛', self)
        # self.submitInterface = Home('提交', self)
        # self.rankInterface = Home('榜单', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.loginInterface, FIF.VPN, "登录")
        self.addSubInterface(self.userInterface, FIF.ROBOT, "用户")

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.problemInterface, FIF.LABEL, '题目')
        # self.addSubInterface(self.contestInterface, FIF.CALENDAR, '比赛')
        # self.addSubInterface(self.submitInterface, FIF.SEND, '提交')
        # self.addSubInterface(self.rankInterface, FIF.BOOK_SHELF, '榜单')
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM
        )

    def initWindow(self):
        self.resize(900, 600)
        self.setWindowIcon(QIcon("favicon.ico"))
        self.setWindowTitle("ghelper")


if __name__ == "__main__":
    # logger.remove(handler_id=None)
    cfg = Config()
    qconfig.load("config/config.json", cfg)
    logger.add("logs/{time}.log", rotation="10 MB",
               encoding="utf-8", level=cfg.loglevel.value)
    logger.info("ghelper.exe start.")
    load_json()
    if cfg.wkhtmltopdf.value == "":
        wkhtmltopdf_installed = False
    else:
        for i in os.listdir(cfg.wkhtmltopdf.value):
            if i == "wkhtmltopdf.exe":
                wkhtmltopdf_installed = True
                logger.debug("wkhtmltopdf installed.")
                break
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
