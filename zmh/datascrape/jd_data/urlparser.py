#!/usr/bin/python 
# -*- coding:utf-8 -*-
import re

class urlparser():
    def __init__(self):
        self.urls = []
    def feed(self,data):
        url = re.findall(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>''', data, re.S | re.I)
        for u in url:
            self.urls.append(u[6])
    def geturls(self):
        return self.urls
if __name__ == '__main__':
    urls = []
    urlparser = urlparser()
    urlparser.feed('1111111111<a href="http://www.bccn.net">BCCN</a>2222222<a href="http://bbs.bccn.net">BCCN.BBS</a>333333333')
    urls += urlparser.geturls()
    print(urls)