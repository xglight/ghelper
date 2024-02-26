# ghelper 说明文档

> 版本 v1.0.0

## 使用

打开 `ghelper.exe` 即可使用。

## 功能

目前有三大功能。

### 用户

用于登录。

### 题目下载

用于下载题目，兼有搜索题目的功能。

### 比赛下载

用于下载比赛，目前只支持比赛id。

## 说明

用户数据保存在 `ghelper.json` 下，没有加密，用 `base64` 进行储存。

下载数据保存在 `data` 文件夹下，可清空。

本程序采用 `python` 编写。

利用 `wkhtmltopdf` 进行 `html` 转 `pdf` 


