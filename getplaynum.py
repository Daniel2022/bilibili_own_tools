import requests
import json

GET_NUM_URL = "https://space.bilibili.com/ajax/member/getSubmitVideos"

class Video: #定义类
    def __init__(self, aid, title, playnum):
        #self.bvid = bvid
        self.aid = aid
        self.title = title
        self.playnum = playnum
    def show(self):
        print(self.title)
        #print(self.bvid)
        print('av' + str(self.aid))
        print(self.playnum)

def makeVideoInfoList(uid):
    Sheet = []
    response = requests.get(GET_NUM_URL, { #第一次尝试get，获取页数（每页100个视频）
        "mid": uid,
        'pagesize': 100,
        'tid': 0,
        'page': 1,
        'keyword': '',
        'order': 'pubdate',
    }).json()
    pagenum = response['data']['pages']
    #print(pagenum)
    #print(list(range(0,pagenum)))
    for i in range(1,pagenum+1): #根据获取的页数，循环发起get
        response = requests.get(GET_NUM_URL, {
            "mid": uid,
            'pagesize': 100,
            'tid': 0,
            'page': i,
            'keyword': '',
            'order': 'pubdate'
        }).json()
        #print(len(response['data']['vlist']))
        for info in response['data']['vlist']:
            video_struct = Video(info['aid'], info['title'], info['play'])
            Sheet.append(video_struct) #一次get获取的100条视频信息封装进Video类对象存入list
    return Sheet

if __name__ == "__main__":
    #mid = 37663924
    mid = input("UID:")
    videolist = makeVideoInfoList(mid)
    sum = 0
    #print(len(videolist))
    for v in videolist: #循环加和
        #print(type(v.playnum))
        if isinstance(v.playnum,int):
            sum += v.playnum
    print(sum)