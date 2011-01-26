from urllib2 import build_opener
from pid_maker.thirdparty_app import BeautifulSoup
from pid_maker.thirdparty_app.BeautifulSoup import *
import re

opener = build_opener()
url = 'http://uss.intra.umessage.com.cn:8180/UrlChangeService/urlGet.do?lu=http://m.12580.com/wap/index.do?&pid=U01QF311'

page = opener.open(url).read()

soup = BeautifulSoup(page)

a = soup.shorturl.string


http://uss.intra.umessage.com.cn:8180/UrlChangeService/urlGet.do?lu=http://m.12580.com/wap/index.do?&pid=U01QF311

target_url = "http://uss.intra.umessage.com.cn:8180/UrlChangeService/urlGet.do?lu=http://m.12580.com/wap/index.do?&pid=U01QF311"
lu = "douban.com"
pid = "12580a"


whole_url = "http://uss.intra.umessage.com.cn:8180/UrlChangeService/urlGet.do?lu=%s&pid=%s" %(lu,pid)