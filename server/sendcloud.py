#!/usr/bin/python
#coding:utf-8
import requests, json, sys, time
import logging
logging.basicConfig(level=logging.INFO,format='%(message)s')

url="http://api.sendcloud.net/apiv2/mail/send"

mail_to = sys.argv[1]
nickname = sys.argv[2]
uid = sys.argv[3]
hashmessage = sys.argv[4]

verify_url="https://exp.chasedreams.cn/u/%s/verify/%s"%(uid,hashmessage)

mail_text = '''<p>Hi <b>@%s</b>!</p>
<p>Help us secure your EXP-Weibo account by verifying your email address (<a href="mailto:%s">%s</a>). This lets you access all of EXP-Weibo's features.</p>
<a href="%s">Verify email address</a>
<p>%s</p>
<br>'''%(nickname,mail_to,mail_to,verify_url,time.ctime())


params = {"apiUser": "???", \
  "apiKey" : "???",\
  "from" : "noreply@exp.chasedreams.cn", \
  "fromName" : "EXP-Weibo", \
  "to" : mail_to, \
  "subject" : "[EXP-Weibo] Please verify your email address.", \
  "html": mail_text, \
}

r = requests.post(url, files={}, data=params)
logging.info(r.text)

