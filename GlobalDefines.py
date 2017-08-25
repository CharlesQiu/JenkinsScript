#!/usr/bin/env python
# encoding: utf-8

# GlobalDefines.py
# iOS

# Created by Charles.Qiu on 2017/2/28 下午12:47.
# Copyright © 2017年 Charles.Qiu. All rights reserved.
# HomePage: https://github.com/CharlesQiu
# Email: qhs@outlook.com

import re
import os

MAIL_SENDER = '你的邮箱'
MAIL_HOST = '你的邮箱服务器'
MAIL_PASSWORD = '你的邮箱密码'

MAIL_RECEIVERS = ['测试人员1邮箱', '测试人员1邮箱']
# 测试时不影响太多人
# MAIL_RECEIVERS = ['邮箱']

print MAIL_RECEIVERS

MAIL_RECEIVERS_FAILED = ['邮箱']

# debug 版本 git 记录展示条数
GIT_LOG_NUMBER_DEBUG = 10
# release 版本 git 记录展示条数
GIT_LOG_NUMBER_RELEASE = 20


ifconfig = os.popen('ifconfig en0 inet')
response = ifconfig.read()
reg = '.*?inet (.*?) netmask.*?'
pattern = re.compile(reg, re.S)
ip = re.findall(pattern, response)

APP_SERVER_URL = 'https://' + ip[0] + ':1234/download'
print '$' * 100 + '\niOS-ipa-server: ' + APP_SERVER_URL + '\n' + '¥' * 100

EMAIL_BODY = '<p><font color="red">安装方法: ' \
                        '<br/>方法一: 使用浏览器直接访问 ' + APP_SERVER_URL + \
                        '<br/>方法二: 连上 "haogongyu204 5G" Wi-Fi, 扫描二维码，如果用微信扫描二维码，请点击右上角使用safari打开</font><br/><img src="cid:0" alt="" /></p>'

print EMAIL_BODY
