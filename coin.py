import requests
import http.cookiejar
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "content-length": "94",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cookie": "",#Add Your Cookies here
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.39",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "referer": "https://www.bilibili.com/video/"
    #"sec-fetch-user": "?1",
    #"upgrade-insecure-requests": '1'
}

csrf = ''

url = "https://api.bilibili.com/x/web-interface/coin/add"

def cookie_loader(cookiefile="cookies.sqlite"):
    #来自soimort/you-get sqlite格式火狐cookies处理
    import sqlite3, shutil, tempfile, os
    temp_dir = tempfile.gettempdir()
    temp_cookiefile = os.path.join(temp_dir, 'temp_cookiefile.sqlite')
    shutil.copy2(cookiefile, temp_cookiefile)
    cookies = http.cookiejar.MozillaCookieJar()
    con = sqlite3.connect(temp_cookiefile)
    cur = con.cursor()
    cur.execute("""SELECT host, path, isSecure, expiry, name, value
    FROM moz_cookies""")
    for item in cur.fetchall():
        c = http.cookiejar.Cookie(
            0, item[4], item[5], None, False, item[0],
            item[0].startswith('.'), item[0].startswith('.'),
            item[1], False, item[2], item[3], item[3] == '', None,
            None, {},
        )
        cookies.set_cookie(c)
    #引自mo-han/mo-han-toolbox
    cookie_dict = requests.utils.dict_from_cookiejar(cookies)
    #print(cookie_dict['bili_jct'])
    cookies_l = ['{}={}'.format(k, v) for k, v in cookie_dict.items()]
    cookie = '; '.join(cookies_l)
    return [cookie,cookie_dict['bili_jct']]

def set_header():
    import os
    global csrf
    if os.path.exists("cookies.sqlite"):
        tmp = cookie_loader()
        headers['cookie'] = tmp[0]
        csrf = tmp[1]
        print('已加载cookies')
    else:
        print('不存在cookies.sqlite')

def addcoin(aid,num,csrf,url,headers):
    print(1)
    res = requests.post(url=url,data={
        'aid': aid,
        'multiply': num,
        'select_like': 0,
        'cross_domain': 'true',
        'csrf': csrf
    },headers=headers).json()
    #print(res)
    return res['code']

if __name__ == '__main__':
    import random, time
    print("你5个币没了！！！！")
    Sucssess = 0
    set_header()
    while(Sucssess < 5):
        aid = random.randint(1,999999999)
        ret = addcoin(aid=aid,num=1,csrf=csrf,url=url,headers=headers)
        if  ret == 0:
            Sucssess += 1
            print("投币至av%d" % aid)
        else:
            pass
        time.sleep(0.5)