import requests
import json
import subprocess
import os
#from requests.cookies import RequestsCookieJar

GET_VIDEO_INFO_URL = "https://api.bilibili.com/x/web-interface/view"
GET_VIDEO_DOWNLOAD_URL = "https://api.bilibili.com/x/player/playurl"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cookie": "",#Add Your Cookies here
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.30 Safari/537.36 Edg/84.0.522.11",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": '1'
}

quality_dict = { #这个不知道写来干吗
    "4K": 120,
    "1080p60": 116,
    "720p60": 74,
    "1080p+": 112,
    "1080p": 80,
    "720p": 64,
    "480p":32,
    "360p":16
}

def getVideoInfo(bid): #拉取稿件信息，获取p数和cid
    response = requests.get(GET_VIDEO_INFO_URL, {
        "bvid": bid
    }).json()
    if response['code'] == 0:
        return response['data']

def getPlayUrl(bvid, cid, qn=80): #get链接获取api，返回全部URL数据
    response = requests.get(GET_VIDEO_DOWNLOAD_URL,{
        'bvid': bvid,
        'cid': cid,
        'qn': qn,
        'otype': 'json',
        'fourk': 1,
        'fnever': 0,
        'type': '',
        'fnval': 16
    },headers=headers).json()
    if response['code'] == 0:
        return response['data']

def getVedioAndAudioUrls(data,qn=80): #根据画质解析对应URL，有H265则保存
    Urllist={'Video_avc':'','Video_hev':'','Audio':''}
    AudioUrl = data['dash']['audio'][0]['baseUrl']
    VideoUrls = data['dash']['video']
    print(qn)
    i=0
    for k in range(0,len(VideoUrls)-1):
        #print(k)
        block = VideoUrls[k]
        #print(block['id'])
        if block['id'] == qn:
            #print(block['codecid'])
            if block['codecid'] == 7:
                Urllist['Video_avc'] = block['baseUrl']
            if block['codecid'] == 12:
                Urllist['Video_hev'] = block['baseUrl']
            i+=1
        if i >=2:
            break
    if Urllist['Video_avc'] == '':
        print("无所选画质（或大会员无效）")
        Urllist['Video_avc'] = VideoUrls[0]['baseUrl']
    Urllist['Audio'] = AudioUrl
    return Urllist
        
def WeatherHaveH265(Urllist): #判断是否获取到H265URL
    if Urllist['Video_hev'] == '':
        return False
    else:
        return True

def Download(vurl, aurl, bvid, page, title): #启动下载，使用aria2c，ffmpeg合流
    referer = "https://www.bilibili.com/video/"
    downshell = "aria2c -s 5 -D -o Video.mp4 " + "\"" + vurl + "\" --referer=" + referer + str(bvid) + "?p=" + str(page)
    subprocess.Popen([r'powershell',downshell]).wait()
    downshell = "aria2c -s 5 -D -o Audio.aac " + "\"" + aurl + "\" --referer=" + referer + str(bvid) + "?p=" + str(page)
    subprocess.Popen([r'powershell',downshell]).wait()
    makeshell = "ffmpeg -i Video.mp4 -i Audio.aac -c:v copy -c:a copy -strict experimental " + "\"" + title + "_" + str(page) + ".mp4\""
    print(makeshell)
    subprocess.Popen([r'powershell',makeshell]).wait()
    subprocess.Popen([r'powershell',"del Video.mp4\ndel Audio.aac"]).wait()

if __name__ == "__main__":
    #bvid = "BV17p4y1D7dA"
    #bvid = "BV1LT4y1g7uw"
    bvid = input("请输入BV号：")
    Info = getVideoInfo(bvid)
    title = Info['title'] #这里应该要处理下有些字符不能作为windows文件名的问题？？？
    pages = Info['pages']
    print('This video has',len(pages),'page(s)')
    if len(pages) != 1:
        page = int(input("选择P："))-1
    else:
        page = 0
    print('画质选择 \n4K:120\n1080p60: 116\n720p60: 74\n1080p: 80\n720p: 64\n480p: 32\n360p: 16')
    qn = int(input("选择画质："))
    cid = pages[page]['cid']
    data = getPlayUrl(bvid, cid, qn)
    Urllist = getVedioAndAudioUrls(data, qn)
    #print(Urllist)
    print("Downloading " + bvid + " " + title + " Page " + str(page))
    if(WeatherHaveH265(Urllist)):
        print("This page have HEVC codec.")
        if(input("是否下载HEVC格式？Y/N") == "Y"):
            Download(Urllist['Video_hev'],Urllist['Audio'],bvid,page+1,title)
        else:
            Download(Urllist['Video_avc'],Urllist['Audio'],bvid,page+1,title)
    else:
        Download(Urllist['Video_avc'],Urllist['Audio'],bvid,page+1,title)

    """
    for i in range(0,len(pages)):
        cid = pages[i]['cid']
        print("Page", i+1, "cid:", cid)
        data = getPlayUrl(bvid, cid, qn)
        Urllist = getVedioAndAudioUrls(data, qn)
        if(WeatherHaveH265(Urllist)):
            print("This page have HEVC codec.")
            Download(Urllist['Video_hev'],Urllist['Audio'],bvid,i+1,title)
        else:
            Download(Urllist['Video_avc'],Urllist['Audio'],bvid,i+1,title)
            """
        