#!usr/bin/env python
# coding=utf-8

__author__ = 'yujun huang'

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_mail(subject=None, to_addrs=None, content=""):
    msg = MIMEText(content, 'html', 'utf-8')

    # 输入Email 地址：
    from_addr = 'robot@tigerbrokers.com'
    password = 'Famu8854'

    msg['From'] = _format_addr("老虎 <%s> " % from_addr)
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg['To'] = ""
    for addr in to_addrs:
        msg['To'] += addr

    # SMTP 服务器地址
    smtp_server = 'smtp.office365.com'
    server = smtplib.SMTP(smtp_server, 587)
    server.set_debuglevel(1)  # 用于打印出和SMTP服务器交互的所有信息

    # server.ehlo()
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()

if __name__ == '__main__':
    send_mail(subject='test',to_addrs=['huangyujun@tigerbrokers.com'],content='')
