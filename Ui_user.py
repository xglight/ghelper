# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\LRK\python\ghelper-qt\user.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_user(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.SubtitleLabel = SubtitleLabel(self.centralwidget)
        self.SubtitleLabel.setMaximumSize(QtCore.QSize(100, 30))
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        self.gridLayout.addWidget(self.SubtitleLabel, 1, 1, 1, 1)
        self.Rank = SubtitleLabel(self.centralwidget)
        self.Rank.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Rank.setText("")
        self.Rank.setObjectName("Rank")
        self.gridLayout.addWidget(self.Rank, 3, 2, 1, 1)
        self.SubtitleLabel_2 = SubtitleLabel(self.centralwidget)
        self.SubtitleLabel_2.setMaximumSize(QtCore.QSize(100, 30))
        self.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.gridLayout.addWidget(self.SubtitleLabel_2, 2, 1, 1, 1)
        self.AC_problems = SubtitleLabel(self.centralwidget)
        self.AC_problems.setMaximumSize(QtCore.QSize(16777215, 30))
        self.AC_problems.setText("")
        self.AC_problems.setObjectName("AC_problems")
        self.gridLayout.addWidget(self.AC_problems, 4, 2, 1, 1)
        self.SubtitleLabel_7 = SubtitleLabel(self.centralwidget)
        self.SubtitleLabel_7.setMaximumSize(QtCore.QSize(100, 30))
        self.SubtitleLabel_7.setObjectName("SubtitleLabel_7")
        self.gridLayout.addWidget(self.SubtitleLabel_7, 3, 3, 1, 1)
        self.Description = SubtitleLabel(self.centralwidget)
        self.Description.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Description.setText("")
        self.Description.setObjectName("Description")
        self.gridLayout.addWidget(self.Description, 5, 2, 1, 3)
        self.Solve = SubtitleLabel(self.centralwidget)
        self.Solve.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Solve.setText("")
        self.Solve.setObjectName("Solve")
        self.gridLayout.addWidget(self.Solve, 1, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.SubtitleLabel_5 = SubtitleLabel(self.centralwidget)
        self.SubtitleLabel_5.setMaximumSize(QtCore.QSize(100, 30))
        self.SubtitleLabel_5.setObjectName("SubtitleLabel_5")
        self.gridLayout.addWidget(self.SubtitleLabel_5, 1, 3, 1, 1)
        self.SubtitleLabel_8 = SubtitleLabel(self.centralwidget)
        self.SubtitleLabel_8.setMaximumSize(QtCore.QSize(100, 30))
        self.SubtitleLabel_8.setObjectName("SubtitleLabel_8")
        self.gridLayout.addWidget(self.SubtitleLabel_8, 5, 1, 1, 1)
        self.SubtitleLabel_3 = SubtitleLabel(self.centralwidget)
        self.SubtitleLabel_3.setMaximumSize(QtCore.QSize(100, 30))
        self.SubtitleLabel_3.setObjectName("SubtitleLabel_3")
        self.gridLayout.addWidget(self.SubtitleLabel_3, 3, 1, 1, 1)
        self.Search_user = SearchLineEdit(self.centralwidget)
        self.Search_user.setMaximumSize(QtCore.QSize(225, 33))
        self.Search_user.setObjectName("Search_user")
        self.gridLayout.addWidget(self.Search_user, 0, 0, 1, 1)
        self.Rate = SubtitleLabel(self.centralwidget)
        self.Rate.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Rate.setText("")
        self.Rate.setObjectName("Rate")
        self.gridLayout.addWidget(self.Rate, 3, 4, 1, 1)
        self.Avatar = ImageLabel(self.centralwidget)
        self.Avatar.setMinimumSize(QtCore.QSize(225, 225))
        self.Avatar.setMaximumSize(QtCore.QSize(225, 225))
        self.Avatar.setObjectName("Avatar")
        self.gridLayout.addWidget(self.Avatar, 1, 0, 5, 1)
        self.Submit = SubtitleLabel(self.centralwidget)
        self.Submit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Submit.setText("")
        self.Submit.setObjectName("Submit")
        self.gridLayout.addWidget(self.Submit, 2, 4, 1, 1)
        self.SubtitleLabel_6 = SubtitleLabel(self.centralwidget)
        self.SubtitleLabel_6.setMaximumSize(QtCore.QSize(100, 30))
        self.SubtitleLabel_6.setObjectName("SubtitleLabel_6")
        self.gridLayout.addWidget(self.SubtitleLabel_6, 2, 3, 1, 1)
        self.uid = SubtitleLabel(self.centralwidget)
        self.uid.setMaximumSize(QtCore.QSize(16777215, 30))
        self.uid.setText("")
        self.uid.setObjectName("uid")
        self.gridLayout.addWidget(self.uid, 1, 2, 1, 1)
        self.Username = SubtitleLabel(self.centralwidget)
        self.Username.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Username.setText("")
        self.Username.setObjectName("Username")
        self.gridLayout.addWidget(self.Username, 2, 2, 1, 1)
        self.SubtitleLabel_4 = SubtitleLabel(self.centralwidget)
        self.SubtitleLabel_4.setMaximumSize(QtCore.QSize(100, 30))
        self.SubtitleLabel_4.setObjectName("SubtitleLabel_4")
        self.gridLayout.addWidget(self.SubtitleLabel_4, 4, 1, 1, 1)
        self.Link_blog = HyperlinkLabel(self.centralwidget)
        self.Link_blog.setObjectName("Link_blog")
        self.gridLayout.addWidget(self.Link_blog, 7, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("user", "MainWindow"))
        self.SubtitleLabel.setText(_translate("user", "uid："))
        self.SubtitleLabel_2.setText(_translate("user", "用户名："))
        self.SubtitleLabel_7.setText(_translate("user", "正确率："))
        self.SubtitleLabel_5.setText(_translate("user", "解决："))
        self.SubtitleLabel_8.setText(_translate("user", "签名："))
        self.SubtitleLabel_3.setText(_translate("user", "排名："))
        self.Avatar.setText(_translate("user", "uid"))
        self.SubtitleLabel_6.setText(_translate("user", "提交："))
        self.SubtitleLabel_4.setText(_translate("user", "AC："))
        self.Link_blog.setText(_translate("user", "Hyperlink label"))
from qfluentwidgets import HyperlinkLabel, ImageLabel, SearchLineEdit, SubtitleLabel
