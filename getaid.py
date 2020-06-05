import requests
import json

GET_VIDEO_INFO_URL = "https://api.bilibili.com/x/web-interface/view"
GET_VIDEO_DOWNLOAD_URL = "https://api.bilibili.com/x/player/playurl"

def getVideoInfo(bid):
    response = requests.get(GET_VIDEO_INFO_URL, {
        "bvid": bid
    }).json()
    if response['code'] == 0:
        return response['data']

if __name__ == "__main__":
    #bvid = "BV17p4y1D7dA"
    #bvid = "BV1LT4y1g7uw"
    bvid = input("请输入BV号：")
    Info = getVideoInfo(bvid)