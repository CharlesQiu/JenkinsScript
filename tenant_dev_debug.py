#!/usr/bin/env python
# encoding: utf-8

# tenant_dev_debug.py
# iOS

# Created by Charles.Qiu on 2016/12/8 上午10:02.
# Copyright © 2016年 Charles.Qiu. All rights reserved.
# HomePage: https://github.com/CharlesQiu
# Email: qhs@outlook.com


import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# 二维码
from PIL import Image
import qrcode

import GlobalDefines
_global_defines = GlobalDefines

# 运行时环境变量字典
environsDict = os.environ
# 此次 jenkins 构建版本号
num_build = environsDict['BUILD_NUMBER']

# git 本地地址 和 git 服务器地址配置
repo_path = '/Users/haogongyu/.jenkins/workspace/tenant_dev/'

app_name = 'app 英文名'
app_ch_name = 'app 中文名字'
app_logo_path = repo_path + 'Config/HGYTenant/HGYTenant.xcassets/AppIcon.appiconset/180@2x.png'

# 此处需要用绝对路径
app_qrcode_path = '/Users/haogongyu/.jenkins/build/tenant_dev/' + app_name + '-' + num_build + '.png'

cmd_git_log = 'git log -' + str(_global_defines.GIT_LOG_NUMBER_DEBUG) + ' --pretty=format:"<font color="green">%cd  %cn %s</font><br/>" --date=iso'

cmd_rm_ipa = 'rm ~/.jenkins/build/ipa/合并端\(开发环境Build*\).ipa'
cmd_mv_ipa = 'mv ~/.jenkins/build/tenant_dev/*.ipa ~/.jenkins/build/ipa/' + app_ch_name + '\(开发环境Build' + num_build +'\)' + '.ipa'
cmd_rm_png = 'rm ~/.jenkins/build/tenant_dev/*.png'

mail_theme = app_ch_name + '开发环境iOS端最新打包文件'
mail_title = app_ch_name + '开发环境（可选开发/测试/灰度/产品环境） - #Bulid:' + num_build

# 获取 最后一次 提交git的信息
def getCommitInfo():
    os.chdir(repo_path);
    lastCommitInfo = runCmd(cmd_git_log)
    return '<font color="orange">最新的' + \
           str(_global_defines.GIT_LOG_NUMBER_DEBUG) + \
           '个提交记录:</font><br/>' + \
           lastCommitInfo
# 生成二维码
def genQrcode(string, path, logo=""):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=1
    )
    qr.add_data(string)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")
    if logo and os.path.exists(logo):
        try:
            icon = Image.open(logo)
            img_w, img_h = img.size
        except Exception as e:
            print(e)
            sys.exit(1)
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        icon = icon.convert("RGBA")
        img.paste(icon, (w, h), icon)
    img.save(path)
    # 调用系统命令打开图片
    os.system('xdg-open %s' % path)

# 发送邮件
def sendEmail():
    # 根据不同邮箱配置 host，user，和pwd
    mail_host = _global_defines.MAIL_HOST
    mail_user = _global_defines.MAIL_SENDER
    mail_pwd = _global_defines.MAIL_PASSWORD
    mail_to = ','.join(_global_defines.MAIL_RECEIVERS)

    msg = MIMEMultipart()

    # 二维码
    genQrcode(_global_defines.APP_SERVER_URL, app_qrcode_path, app_logo_path)

    environsString = '<h3><font color="Purple">' + mail_title + '</font></h3>'
    environsString += _global_defines.EMAIL_BODY

    # 获取git最后一次提交信息
    lastCommitInfo = getCommitInfo()
    environsString += '<p>' + lastCommitInfo + '<p>'

    message = environsString
    body = MIMEText(message, _subtype='html', _charset='utf-8')

    # 添加附件
    with open(app_qrcode_path, 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'png', filename=app_qrcode_path)
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=app_qrcode_path)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        msg.attach(mime)

    msg.attach(body)
    msg['To'] = mail_to
    msg['from'] = mail_user
    msg['subject'] = mail_theme

    try:
        s = smtplib.SMTP()
        # 设置为调试模式，就是在会话过程中会有输出信息
        s.set_debuglevel(1)
        s.connect(mail_host)
        s.starttls()  # 创建 SSL 安全加密 链接

        s.login(mail_user, mail_pwd)

        s.sendmail(mail_user, _global_defines.MAIL_RECEIVERS, msg.as_string())
        s.close()

    except Exception, e:
        print e

# python 执行shell 命令
def runCmd(cmd):
    try:
        import subprocess
    except ImportError:
        _, result_f, error_f = os.popen3(cmd)
    else:
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_f, error_f = process.stdout, process.stderr

    errors = error_f.read()
    if errors:
        print errors
        pass
    result_str = result_f.read().strip()
    if result_f:   result_f.close()
    if error_f:    error_f.close()

    return result_str

def main():
    runCmd(cmd_rm_ipa)
    runCmd(cmd_mv_ipa)
    sendEmail()
    runCmd(cmd_rm_png)
    return

if __name__ == '__main__':
    main()
