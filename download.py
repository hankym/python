import urllib.request
import re
from bs4 import BeautifulSoup
import warnings
import queue
import threading

#warnings.filterwarnings("ignore")
urlpre = "http://bbs.hupu.com"
gifpx  = ".gif"
urlp = re.compile('<a id="" href="(.*?)">(.*?)</a>')
gifp = re.compile('src="(.{0,100}?).gif"')
maxline = 10

urllist = []
giflist = []
def geturllist(url):
    try:
        p = urllib.request.urlopen(url).read()
        p = p.decode("GBK","ignore")
        urllist.clear()
        for i,j in urlp.findall(p):
            urllist.append(i)
    except Exception as err:
        #pass
        warnings.warn(err)

def IsExitInList(List,element):
    for i in List:
        print(i)
        if i == element:
            print("exit")
            return True
    return False

def getgiflist(url):
    try:
        p = urllib.request.urlopen(url).read()
        #p = p.decode("GBK")
        giflist.clear()
        soup = BeautifulSoup(p)
        for i in soup.find_all("img"):
            svalue = i.get("src")
            if svalue.find(".gif") != -1 and svalue.find("hoopchina") == -1:
                
                #isexit = IsExitInList(giflist,svalue)
                #if isexit == False:
                giflist.append(svalue)
                
        #for i in gifp.findall(p):
         #   if i.find("hoopchina") != -1:
          #      continue
           # print(i)
            #giflist.append(i)
    except Exception as err:
        warnings.warn(err)



class DownLoadThread(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.queue = q

    def run(self):
        while True:
            url = self.queue.get()
            #print ("get url %s" %url[-10:])
            self.downloadgif(url,url[-10:])
            self.queue.task_done()
            print("%s done" % url[-10:])
    def downloadgif(self,url,savename):
        try:
            urllib.request.urlretrieve(url,savename)
            #print("down%s",url[-10:])
        except Exception as err:
            print("download error")

testurl = "http://bbs.hupu.com/bxj"


count = 0
ii = 1



q = queue.Queue()
while(ii < maxline):

    tempurl = testurl + "-%d" % ii
    

    #tempurl = testurl + "-%d"%i

    ii += 1

    print("**********")
    print(tempurl)
        
    geturllist(tempurl)



    for url in urllist:
        url = urlpre + url
        getgiflist(url)
        #print ("url %s %d",url,len(giflist))


        for gif in giflist:
            #gif = gif + gifpx
            print(gif)
            q.put(gif)

        if (len(giflist) > 0):
            for i in  range(5):
                t = DownLoadThread(q)
                t.setDaemon(True)
                t.start()


            #downloadgif(gif,"d:\\gif\\" + gif[-10:])
            q.join()
            print ("join end")
        #print ("end")

