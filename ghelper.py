from qfluentwidgets import FluentWindow, NavigationItemPosition, SubtitleLabel, setFont, SplashScreen
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow,StandardTitleBar
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Ui_home import Ui_home
from Ui_user import Ui_user

class Demo(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.resize(900, 600)
        self.setWindowTitle('ghelper')
        self.setWindowIcon(QIcon('favicon.ico'))

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

class Home(QMainWindow,Ui_home):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))

class User(QMainWindow,Ui_user):
    def __init__(self,text:str,parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Home('主页',self)
        self.userInterface = User('用户', self)
        # self.problemInterface = Home('题目', self)
        # self.settingInterface = Home('设置', self)
        # self.contestInterface = Home('比赛', self)
        # self.submitInterface = Home('提交', self)
        # self.rankInterface = Home('榜单', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.userInterface, FIF.ROBOT, '用户')

        # self.navigationInterface.addSeparator()

        # self.addSubInterface(self.problemInterface, FIF.LABEL, '题目')
        # self.addSubInterface(self.contestInterface, FIF.CALENDAR, '比赛')
        # self.addSubInterface(self.submitInterface, FIF.SEND, '提交')
        # self.addSubInterface(self.rankInterface, FIF.BOOK_SHELF, '榜单')

        # self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 600)
        self.setWindowIcon(QIcon('favicon.ico'))
        self.setWindowTitle('ghelper')


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    # w=Demo()
    # w.show()
    # w.close()
    w = Window()
    w.show()
    app.exec()
