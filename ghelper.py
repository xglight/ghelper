from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Ui_home import Ui_home
from Ui_user import Ui_user
from Ui_login import Ui_login
from Ui_problem import Ui_problem
import requests
from bs4 import *
import base64
import os
import pdfkit


def base64Encry(plaintext):  # base64加密
    base64Encry = str(base64.b64encode(plaintext.encode("utf-8")))
    return base64Encry[base64Encry.find("'") + 1: len(base64Encry) - 1]


def base64Decry(ciphertext):  # base64解密
    base64Decry = (base64.b64decode(ciphertext)).decode("utf-8")
    return str(base64Decry)


def load_json():
    global username, password, js, login_success
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
    f = False
    for i in environment_path:
        if i == ";":
            for i in os.listdir(path):
                if i == "wkhtmltopdf.exe":
                    cfg.set(cfg.wkhtmltopdf, path+"/")
                    f = True
                    break
            if f == True:
                break
            path = ""
        else:
            path += i
    if f == False:
        cfg.set(cfg.wkhtmltopdf, "")

def htmlToPdf(html, to_file):  # html转pdf
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
    global cookies
    geturl = "https://gmoj.net/junior/index.php/main/home"  # 主地址（获取秘钥）
    r = requests.get(geturl, headers=headers, timeout=1)
    cookies = r.cookies  # 获取cookies，用于之后登录（cookies可保存登录状态）
    cookies = requests.utils.dict_from_cookiejar(cookies)  # cookies格式化
    b = BeautifulSoup(r.text, "html.parser")  # 用bs4处理get的信息
    if str(b) == "None":
        return -1
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
    # print(postdata)
    pr = requests.post(
        posturl, cookies=cookies, headers=headers, data=postdata
    )  # 发送post登录请求
    return pr.text == "success"  # 判断是否成功


class Config(QConfig):
    # download
    downloadFolder = ConfigItem(
        "Folders", "Download", "download", FolderValidator())
    cacheFolder = ConfigItem("Folders", "Cache", "cache", FolderValidator())
    wkhtmltopdf = ConfigItem(
        "Folders", "Wkhtmltopdf", "wkhtmltopdf", FolderValidator())


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
        url = "https://gmoj.net/senior/index.php/users/"+name
        try:
            r = requests.get(url, headers=headers, cookies=cookies)
        except:
            return -1
        b = BeautifulSoup(r.text, 'html.parser')
        if b.find("p") != None:
            self.find_error()
            return -1
        self.find_success()
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
            r = requests.get(data, headers=headers)
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
            elif j == 3:
                self.Rank.setText(i.span.text)
            elif j == 4:
                self.AC_problems.setText(i.a.span.text)
            elif j == 5:
                self.Solve.setText(i.a.span.text)
            elif j == 6:
                self.Submit.setText(i.a.span.text)
            elif j == 7:
                self.Rate.setText(i.span.text)
            else:
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


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
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
        self.__initWidget()

    def __initWidget(self):
        self.resize(900, 600)
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

    def cdownload(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.download.setContent(folder)

    def ccache(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if not folder or cfg.get(cfg.cacheFolder) == folder:
            return

        cfg.set(cfg.cacheFolder, folder)
        self.cache.setContent(folder)

    def cwkhtmltopdf(self):
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
        return -1

    def __connectSignalToSlot(self):
        self.download.clicked.connect(self.cdownload)
        self.cache.clicked.connect(self.ccache)
        self.wkhtmltopdf.clicked.connect(self.cwkhtmltopdf)

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
        # self.setupUi(self)
        self.hBoxLayout = QHBoxLayout(self)
        self.settingIterface = SettingInterface(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.settingIterface)
        self.resize(900, 600)
        self.setObjectName(text.replace(" ", "-"))


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
        self.setObjectName(text.replace(" ", "-"))
        self.Problem.cellDoubleClicked.connect(self.open_problem)

    def search_problem(self):
        global cookies
        global headers
        Problem.search = str(self.Search_problem.text())
        url = "https://gmoj.net/senior/index.php/main/problemset?search=" + Problem.search
        try:
            r = requests.get(url, headers=headers, cookies=cookies)
        except:
            return -1
        b = BeautifulSoup(r.text, "html.parser")
        with open("problem.html", "w", encoding="utf-8") as f:
            f.write(str(b))
        if str(b) == "None":
            return -1
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
            return -1
        Problem.page = 1
        self.View_problem()

    def getPage(self):
        global cookies
        global headers
        Problem.problem_set = []
        url = "https://gmoj.net/senior/index.php/main/problemset/" + \
            str(Problem.page) + "?search=" + Problem.search
        try:
            r = requests.get(url, headers=headers, cookies=cookies)
        except:
            return -1
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
        self.getPage()
        if len(Problem.problem_set) == 0:
            return -1
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
        self.Problem.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        for i in range(len(Problem.problem_set)):
            self.check = QTableWidgetItem()
            self.check.setCheckState(Qt.Unchecked)  # 把checkBox设为未选中状态
            self.Problem.setItem(i, 0, self.check)
        for i in range(len(Problem.problem_set)):
            self.Problem.setItem(i, 1, QTableWidgetItem(
                Problem.problem_set[i]["pid"]))
        for i in range(len(Problem.problem_set)):
            self.Problem.setItem(i, 2, QTableWidgetItem(
                Problem.problem_set[i]["title"]))
        for i in range(len(Problem.problem_set)):
            self.Problem.setItem(i, 3, QTableWidgetItem(
                Problem.problem_set[i]["source"]))
        for i in range(len(Problem.problem_set)):
            self.Problem.setItem(i, 4, QTableWidgetItem(
                Problem.problem_set[i]["solvedCount"]))
        for i in range(len(Problem.problem_set)):
            self.Problem.setItem(i, 5, QTableWidgetItem(
                Problem.problem_set[i]["submitCount"]))
        for i in range(len(Problem.problem_set)):
            self.Problem.setItem(i, 6, QTableWidgetItem(
                Problem.problem_set[i]["avg"]))

    def check_problem(self, item):
        h = item.row()
        if self.Problem.item(h, 0).checkState() == Qt.Checked:
            self.Problem.item(h, 0).setCheckState(Qt.Unchecked)
        else:
            self.Problem.item(h, 0).setCheckState(Qt.Checked)

    def jump_up(self):
        if Problem.page > 1:
            Problem.page -= 1
            self.View_problem()

    def jump_down(self):
        if Problem.page < Problem.lastpage:
            Problem.page += 1
            self.View_problem()

    def check_all(self):
        for i in range(self.Problem.rowCount()):
            self.Problem.item(i, 0).setCheckState(Qt.Checked)

    def check_reverse(self):
        for i in range(self.Problem.rowCount()):
            if self.Problem.item(i, 0).checkState() == Qt.Checked:
                self.Problem.item(i, 0).setCheckState(Qt.Unchecked)
            else:
                self.Problem.item(i, 0).setCheckState(Qt.Checked)

    def open_problem(self, row, column):
        if column == 2:
            pid = self.Problem.item(row, 1).text()
            p = self.get_problem(pid)
            if p != 1:
                self.login_error()
                return -1
            
    
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
        url = "https://gmoj.net/senior/index.php/main/show/" + id
        try:
            r = requests.get(url, headers=headers, cookies=cookies)
        except:
            return -1
        b = BeautifulSoup(r.text, "html.parser")
        if str(b) == "None" or b.find(style="white-space: pre-wrap") != None:
            return -1
        title = str(b.find("h4").string)
        if title != "(Standard IO)":
            title = b.find("h4").find("span").string
            title = title[0: title.find(".")]
        else:
            title = id
        if not os.path.exists(cfg.cacheFolder.value+"\\" + str(id)):
            os.makedirs(cfg.cacheFolder.value + "\\" + str(id))
        title = str(title)
        with open(cfg.cacheFolder.value+"\\" + str(id) + "\\" + "o_" + str(id) + ".html", "w", encoding="utf-8") as f:
            f.write(str(b))
        if b.find(id="problem_description") == None:  # 判断是否为markdown
            if self.problem_html(id)== 1:
                return 1
        else:
            print(-1)
        #     getMarkdown(b, str(title), str(title) + "/")
        # TODO: 增加markdown渲染功能

    def problem_html(self, id):
        b = ""
        if not os.path.exists(cfg.downloadFolder.value+"\\" + str(id)):
            os.makedirs(cfg.downloadFolder.value + "\\" + str(id))
        if not os.path.exists(cfg.cacheFolder.value+"\\" + str(id)+"\\" + str(id) + ".html"):
            return -1
        with open(cfg.cacheFolder.value+"\\" + str(id) + "\\"+"o_" + str(id) + ".html", "r", encoding="utf-8") as f:
            b = f.read()
        b = BeautifulSoup(b, "html.parser")
        for i in b.find_all(class_="btn btn-mini btn_copy"):
            i.decompose()
        with open(cfg.cacheFolder.value+"\\" + str(id) + "\\" + str(id) + ".html", "w+", encoding="utf-8") as f:
            f.write("<head>\n")
            f.write('  <meta charset="utf-8">\n')
            f.write("</head>\n")  # 写入编码
            f.write(str(b.find(class_="row-fluid")))
            f.write(str(b.find(id="problem_show_container").find(class_="span9")))
            f.write(str(b.style))
            f.write(str(b.find(type="text/javascript")))
        print(cfg.cacheFolder.value+"\\" + str(id) + "\\" + str(id) + ".html")
        print(cfg.downloadFolder.value+"\\" + str(id) + "\\" + str(id) + ".pdf")
        htmlToPdf(cfg.cacheFolder.value+"\\" + str(id) + "\\" + str(id) + ".html", cfg.downloadFolder.value+"\\" + str(id) + "\\" + str(id) + ".pdf")
        return 1


class Login(QMainWindow, Ui_login):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.password.returnPressed.connect(self.cPassword)
        self.login.clicked.connect(self.cPassword)
        self.setObjectName(text.replace("", "-"))

    def cPassword(self):
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
    cfg = Config()
    load_json()
    qconfig.load("config/config.json", cfg)
    app = QApplication(sys.argv)
    # w=Demo()
    # w.show()
    # w.close()
    w = Window()
    w.show()
    app.exec()
