import requests
from bs4 import *
import time
import threading
import os
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
url = "https://gmoj.net/senior/index.php/main/ranklist/"
gmoj_login("2022李睿康","cleGHt13(&")
def get_avator(l,r):
    for i in range(l,r+1):
        get_url = url + str(i)
        r = requests.get(get_url,cookies=cookies, headers=headers).text
        b = BeautifulSoup(r, "html.parser")
        with open("test.html","w+",encoding='utf-8') as f:
                f.write(str(b))
        b=b.table.tbody
        cnt = 0
        for i in b.find_all("tr"):
            with open("test.html","w+",encoding='utf-8') as f:
                f.write(str(i))
            s = str(i)
            name = s[int(int(s.find("span")) + 30):int(s.find("<",int(s.find("span"))+31,int(len(s))))]
            # print(name)
            uurl = "https://gmoj.net/senior/index.php/users/"+name
            try:
                r = requests.get(uurl, headers=headers, cookies=cookies)
            except:
                continue
            b = BeautifulSoup(r.text,'html.parser')
            
            if b.find("p") != None:
                continue
            data = b.find("img")["src"]
            if data != "":
                path = str("D:/LRK/python/ghelper-qt/cache")+'/'+str(name)+"_avatar.png"
                if os.path.exists(path):continue
                r = requests.get(data,headers=headers)
                if r.status_code == 404:
                    continue
                with open(path,"wb") as f:
                    f.write(r.content)

threads = []
start = time.time()
# 创建并启动线程
for i in range(1,11):
    thread = threading.Thread(target=get_avator, args=((i-1)*15+1,i*15))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()
stop = time.time()