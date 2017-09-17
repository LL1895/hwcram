#!/usr/bin/python3
# coding: utf-8
import os
import logging
from logging.handlers import RotatingFileHandler

if not os.path.exists('/var/log/hwcram'):
    os.makedirs('/var/log/hwcram',0o755)

#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s %(module)s %(funcName)s %(process)d %(thread)d %(levelname)s %(message)s',filename='/var/log/hwcram/hwcram.log',filemode='a')
logging.basicConfig(level=logging.ERROR,format='%(asctime)s %(filename)s %(module)s %(funcName)s %(process)d %(thread)d %(levelname)s %(message)s',filename='/var/log/hwcram/hwcram.log',filemode='a')

#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
Rthandler = RotatingFileHandler('/var/log/hwcram/hwcram.log', maxBytes=10*1024*1024,backupCount=5)
#Rthandler.setLevel(logging.DEBUG)
Rthandler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s %(filename)s %(module)s %(funcName)s %(process)d %(thread)d %(levelname)s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)
