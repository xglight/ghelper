import requests
from bs4 import BeautifulSoup
import os
import string

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}
cookies = ""
def gmoj_login(username, password):  # 发送登录请求
    geturl = "https://gmoj.net/junior/index.php/main/home"  # 主地址（获取秘钥）
    r = requests.get(geturl, headers=headers, timeout=1)
    global cookies
    cookies = r.cookies  # 获取cookies,用于之后登录（cookies可保存登录状态）
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
with open("ranklist.csv","a",encoding='utf-8') as f:
    f.write("排名,用户名,签名,通过题目数,提交通过数,提交数,AC率\n")
gmoj_login('2022李睿康','cleGHt13(&')
url = "https://gmoj.net/senior/index.php/main/ranklist/"
for i in range(1,150+1):
    get_url = url + str(i)
    r = requests.get(get_url,cookies=cookies, headers=headers).text
    b = BeautifulSoup(r, "html.parser")
    b=b.table.tbody
    cnt = 0
    for i in b.find_all("td"):
        if i.string==None:
            with open("ranklist.csv","a",encoding='utf-8') as f:
                if i.find(class_="label label-info") != None:
                    f.write('"'+i.find(class_="label label-info").text+'"')
                    f.write(',')
                else:
                    f.write('""')
                    f.write(',')
        else:
            if cnt==7:
                with open("ranklist.csv","a",encoding='utf-8') as f:
                    f.write('\n')
                cnt=0
            with open("ranklist.csv","a",encoding='utf-8') as f:
                f.write('"'+i.string+'"')
                f.write(',')
        cnt+=1
    with open("ranklist.csv","a",encoding='utf-8') as f:
        f.write('\n')
