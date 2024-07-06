# ghelper 使用说明

## 1. 下载安装

可以选择 release 版本下载，下载后解压到任意目录，然后双击运行 ghelper.exe 即可。

或者 fork 项目到本地，然后在本地编译运行。

## 2. 功能介绍

本项目致力于为 gmoj 打造一个易用、高效的辅助工具，毕竟 gmoj，~~大家都知道~~。

目前 ghelper 主要有以下功能：

1. 登录 gmoj
2. 获取 gmoj 用户的个人信息
3. 查看和下载 gmoj 题目信息与比赛

未来将会支持以下功能：

1. 查看 gmoj 排行榜
2. 提交题目和查看评测状态
3. 一个本地的对拍辅助

## 3.软件说明

软件基于 Python 3.9 开发，使用 PyQt5 作为 GUI 框架。

采用 MIT 协议开源。

使用了以下的第三方库：

1. requests
2. beautifulsoup4
3. qfluentwidgets
4. pdfkit
   
以及一个第三方的 html 转 pdf 工具 pdfkit:

官网:<https://pdfkit.org/>

下载:<https://wkhtmltopdf.org/downloads.html>