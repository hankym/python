__author__ = 'Administrator'
import re

from urllib.request import urlopen,urlretrieve

from bs4 import BeautifulSoup

import requests

import time

BXJ_URL = "http://bbs.hupu.com/bxj"
BXJ_TITLE = "http://bbs.hupu.com"

FOLDER  = "./gif/"

LIMIT_PAGE = 10
START_PAGE = 10
END_PAGE = START_PAGE + LIMIT_PAGE
def getLinks(inculeurl):

    print("*****" + inculeurl)
    html = urlopen(inculeurl)

    bs = BeautifulSoup(html,"lxml")

    linkList = []
    for link in bs.find_all("a", href=re.compile("^/(\d+)\.html$")):
        if link.attrs["href"] is not None:
           linkList.append(link.attrs["href"])

    return linkList

def get_gif_link(url):

    print(url)
    html = urlopen(url)
    bs   = BeautifulSoup(html,"lxml")

    linklist = []

    for link in bs.find_all("img",src=re.compile("^http://.+\.gif$")):

        if link.attrs["src"] not in linklist:
             if link.attrs["src"].find("icon") == -1 and link.attrs["src"].find("b1.hoopchina.com.cn") == -1:
                 linklist.append(link.attrs["src"])

    return linklist


def download_git(link):

    try:
        name = str(int(time.time() * 1000)) + ".gif"

        data = requests.get(link, timeout=5)
        with open(FOLDER + name,"wb") as f:
            f.write(data.content)

    except Exception as e:
        print(e)



def bxj_gif_download():

    for i in range(START_PAGE,END_PAGE):
        ex = ""

        if i is not 0:
            ex = "-" + str(2+i)

        pagelist = getLinks(BXJ_URL+ex)

        for pagelink in pagelist:
            giflink = get_gif_link(BXJ_TITLE+pagelink)

            for gif in  giflink:

                print(gif)
                download_git(gif)



if __name__ == "__main__":

   bxj_gif_download()


