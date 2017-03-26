# -*- coding: utf-8 -*-
import sys
import smtplib
import time
from email.mime.text import MIMEText


mailto=[]
mailto.append(sys.argv[1])
nickname = sys.argv[2]
uid = sys.argv[3]
hashmessage = sys.argv[4]

verify_url="http://192.168.1.143:8000/u/%s/verify/%s"%(uid,hashmessage)

mail_text = '''Hi <b>@%s</b>!<br><br>Help us secure your EXP-Weibo account by verifying your email address (<a href="mailto:%s">%s</a>). This lets you access all of EXP-Weibo's features.<br><br><a href="%s">Verify email address</a><br><br>%s'''%(nickname,mailto[0],mailto[0],verify_url,time.ctime())


mail_host="???"  #设置服务器
mail_user="???"    #用户名
mail_pass="???"   #授权码 
mail_postfix="???.com"  #发件箱的后缀
  
def send_mail(to_list,sub,content):  
    me="EXP-Weibo"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='html',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
if send_mail(mailto,"[EXP-Weibo] Please verify your email address.",mail_text):  
    print "success"  
else:  
    print "failed"
