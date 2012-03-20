# -*- coding: utf-8 -*-  
'''
Created on 2012-3-19
@author: sanli
'''
import logging
from selenium import webdriver

import os
base_path = os.getcwd()
logging.basicConfig(level=logging.INFO)
logger = logging


class ChromeCtl:
    def startChrome(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument("kiosk")
        
        #判断操作系统
        import platform
        osname = platform.uname()[0] 
        if( osname == "Windows"):  # windows 系统
            self.driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)
        elif( osname == "Darwin"):  # MacOS 系统
            self.driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
        else:
            self.driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)
            
        self.show_content("cover.html")
    
    def stopChrome(self):
        self.driver.close()
        
    """展示指定内容，如果是“http://”开始的资源，就直接访问，否则访问res目录下对应的资源
    """
    def show_content(self, resurl = ""):
    
        if( resurl.find("http://") == 0):
            logger.info("打开远程资源：" + resurl)
            self.driver.get(resurl)
        else:
            local_file = "file://" + base_path + "/res/" + resurl
            logger.info("打开本地文件：" + local_file)
            self.driver.get(local_file)


class Console:
    
    def __init__(self, chrome_ctl):
        self.chrome_ctl = chrome_ctl 
        
    def start(self):

        PORT = 8000
        
        ConsoleHandler.chrome_ctl = self.chrome_ctl 
        
        import SocketServer        
        httpd = SocketServer.TCPServer(("", PORT), ConsoleHandler)
        
        print "serving at port", PORT
        httpd.serve_forever()
        
        

import SimpleHTTPServer
class ConsoleHandler (SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    """处理控制命令"""
    def do_GET(self):
        logger.info("REQUEST:" + self.path);
        if(self.path.find("/res/") == 0):
            ConsoleHandler.chrome_ctl.show_content(self.path[5:])
            
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    
    
if __name__ == '__main__':

    logger.info("启动Chrome...")
    ctl = ChromeCtl()
    ctl.startChrome()
    
    logger.info("启动控制端口...")
    console = Console(ctl)
    console.start()
    
    
    import time
    time.sleep(100);
    
    ctl.stopChrome()
    
    
    
    