# -*- coding: utf-8 -*-
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

gmail_user = ''
gmail_app_password = ''
title = '안녕하세요'
text = '내용입니다\n내용입니다'

msg = MIMEMultipart("alternative")
msg["Subject"] = u'{0}'.format(title)
part1 = MIMEText(u'{0}'.format(text),
                 "plain", "utf-8")
msg.attach(part1)
email_text = msg.as_string().encode('ascii')

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, gmail_user, email_text)
    server.close()

    print('이메일 보냄')
except Exception as exception:
    print("오류: %s!\n\n" % exception)
