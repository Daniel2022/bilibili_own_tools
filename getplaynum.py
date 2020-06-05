import requests
import json

GET_NUM_URL = "https://space.bilibili.com/ajax/member/getSubmitVideos"

class Video:
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
    response = requests.get(GET_NUM_URL, {
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
    for i in range(1,pagenum+1):
        response = requests.get(GET_NUM_URL, {
            "mid": uid,
            'pagesize': 100,
            'tid': 0,
            'page': i,
            'keyword': '',
            'order': 'pubdate',
        }).json()
        #print(len(response['data']['vlist']))
        for info in response['data']['vlist']:
            video_struct = Video(info['aid'], info['title'], info['play'])
            Sheet.append(video_struct)
    return Sheet

if __name__ == "__main__":
    mid = 37663924
    videolist = makeVideoInfoList(mid)
    sum = 0
    #print(len(videolist))
    for v in videolist:
        #print(type(v.playnum))
        if isinstance(v.playnum,int):
            sum += v.playnum
    print(sum)