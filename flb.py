__author__ = 'Administrator'

import re

from urllib.request import urlopen,urlretrieve

from bs4 import BeautifulSoup

import requests

import time


FOLDER  = "./gif/"

LIMIT_PAGE = 10
START_PAGE = 0
END_PAGE = START_PAGE + LIMIT_PAGE

FLB_URL = "http://fuliba.net"

EXCLUDE_URL = ["http://ww1.sinaimg.cn/mw1024/006a0xdJgw1f6ozk2ag33g307e02a3yn.gif","http://ww1.sinaimg.cn/mw690/006a0xdJgw1f8zxcjq344g30h801y0sx.gif"]

def getLinks(includeurl):

    html = urlopen(includeurl)

    bs = BeautifulSoup(html,"lxml")

    linkList = []

    for link in bs.find_all("a", rel="external"):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in linkList and len(link.attrs["href"]) > 0:
                linkList.append(link.attrs["href"])

    return linkList

def get_gif_link(url):

    html = urlopen(url)

    bs   = BeautifulSoup(html,"lxml")

    linkList = []
    for link in bs.find_all("img", src=re.compile("^http://.+\.gif$")):

        if link.attrs["src"] is not None:
            if link.attrs["src"].find("icon") == -1 and link.attrs["src"] not in EXCLUDE_URL:
                linkList.append(link.attrs["src"])
    return linkList

def download_git(link):

    try:
        name = str(int(time.time() * 1000)) + ".gif"

        data = requests.get(link, timeout=5)
        with open(FOLDER + name,"wb") as f:
            f.write(data.content)

    except Exception as e:
        print(e)


def flb_gif_download():

    for i in range(START_PAGE,END_PAGE):

        ex = ""

        if i is not 0:
            ex = "/page/"+str(i+1)

        linkList = getLinks(FLB_URL + ex)

        for link in linkList:

            giflink = get_gif_link(link)

            for gif in giflink:
                print(gif)
                download_git(gif)



if __name__ == "__main__":

   flb_gif_download()
   print("end")
