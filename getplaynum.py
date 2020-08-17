import requests
import json

#GET_NUM_URL = "https://space.bilibili.com/ajax/member/getSubmitVideos"
GET_NUM_URL = "https://api.bilibili.com/x/space/arc/search"
GET_INFO_URL = "https://api.bilibili.com/x/space/acc/info"
GET_FAN_URL = "https://api.bilibili.com/x/relation/stat"

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

class UP:
    def __makeVideoInfoList(self,uid):
        Sheet = []
        response = requests.get(GET_NUM_URL, { #第一次尝试get，获取页数（每页100个视频）
            "mid": uid,
            'ps': 100,
            #'tid': 0,
            'pn': 1,
            #'keyword': '',
            #'order': 'pubdate',
        }).json()
        #print(response)
        pagenum = response['data']['page']['count']
        #print(pagenum)
        #print(list(range(0,pagenum)))
        for i in range(1,pagenum+1): #根据获取的页数，循环发起get
            response = requests.get(GET_NUM_URL, {
                "mid": uid,
                'ps': 100,
                #'tid': 0,
                'pn': i,
                #'keyword': '',
                #'order': 'pubdate'
            }).json()
            #print(len(response['data']['vlist']))
            for info in response['data']['list']['vlist']:
                video_struct = Video(info['aid'], info['title'], info['play'])
                Sheet.append(video_struct) #一次get获取的100条视频信息封装进Video类对象存入list
        return Sheet
    def __init__(self, mid):
        self.__mid = mid
        response = requests.get(GET_INFO_URL,{
            "mid": mid,
            "jsonp": "jsonp"
        }).json()
        if response['code'] == 0:
            self.__name = response['data']['name']
            self.__level = response['data']['level']
            self.__sign = response['data']['sign']
        response = requests.get(GET_FAN_URL,{
            'vmid': mid
        }).json()
        if response['code'] == 0:
            self.__follower = response['data']['follower']
        self.__videos_list = self.__makeVideoInfoList(mid)
        self.__playsum = 0
        #print(len(videolist))
        for v in self.__videos_list: #循环加和
            #print(type(v.playnum))
            if isinstance(v.playnum,int):
                self.__playsum += v.playnum   
    def show(self):
        print('========UP主信息=======')
        print('ID:\t'+self.__name)
        print('UID:\t'+str(self.__mid))
        print('等级:\tlv.'+str(self.__level))
        print('签名:\t'+self.__sign)
        print('粉丝:\t'+str(self.__follower))
        print("播放量:\t"+str(self.__playsum))

if __name__ == "__main__":
    #mid = 37663924
    mid = int(input("UID:"))
    UP_struct = UP(mid)
    UP_struct.show()
    #videolist = makeVideoInfoList(mid)