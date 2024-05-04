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


class Config(QConfig):
    # download
    downloadFolder = ConfigItem("Folders", "Download", "download", FolderValidator())
    cacheFolder = ConfigItem("Folders", "Cache", "cache", FolderValidator())


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


class User(QMainWindow, Ui_user):
    username = ""

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.Search_user.setPlaceholderText("输入用户名")
        self.Search_user.searchSignal.connect(self.cSearch_user)
        self.Search_user.returnPressed.connect(self.cSearch_user)
        self.setObjectName(text.replace(" ", "-"))

    def cSearch_user(self):
        if str(self.Search_user.text()) != "":
            global username
            username = str(self.Search_user.text())


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

    def __connectSignalToSlot(self):
        self.download.clicked.connect(self.cdownload)
        self.cache.clicked.connect(self.ccache)


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


class Login(QMainWindow, Ui_login):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(text.replace("", "-"))


class Window(FluentWindow):
    """主界面"""

    def __init__(self):
        super().__init__()
        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Home("主页", self)
        self.userInterface = User("用户", self)
        # self.problemInterface = Home('题目', self)
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

        # self.navigationInterface.addSeparator()

        # self.addSubInterface(self.problemInterface, FIF.LABEL, '题目')
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
    qconfig.load("config/config.json", cfg)
    app = QApplication(sys.argv)
    # w=Demo()
    # w.show()
    # w.close()
    w = Window()
    w.show()
    app.exec()
