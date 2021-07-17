'''
@desc:获取手机号码归属地
@author:sinsen
@date:2019年9月4日
'''
from sys import argv
from pyquery import PyQuery
import requests

header = {
    "Accept-Language": "zh-CN,zh;q=0.9",
    #"Cookie": "ASPSESSIONIDQABBQTSS=HHMFIOGCNGNBMIMIJKIFFHIM",
    "Host": "www.ip138.com:8080",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}
def get_addr(phone=None):
    req = requests.get("http://www.ip138.com:8080/search.asp?action=mobile&mobile=%s"%phone, headers=header)
    req.encoding = req.apparent_encoding # 手动更换编码，简直智障
    doc = PyQuery(req.text)
    print(doc('.tdc2:eq(1)').text())

if __name__ == "__main__":
    if len(argv)>1:
        get_addr(argv[1])
    else:
        print("python %s [phone number]" % argv[0])
