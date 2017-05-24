import asyncio
import aiomysql
import time
import datetime
import random
import base64
import os
import shutil
# import ssl
import re
import hashlib
import pymysql
import json
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from PIL import Image

import logging
logging.basicConfig(level=logging.INFO,format='%(message)s')

import pagelayout

statusconvert = ["notyet","already"]

def statusformat(praises_count,comments_count,reposts_count): #done
    formatstatus = ""
    if reposts_count!=0:
        formatstatus = formatstatus + "转发" + str(reposts_count)
    if comments_count!=0:
        formatstatus = formatstatus + "&nbsp;&nbsp;&nbsp;&nbsp;评论" + str(comments_count)
    if praises_count!=0:
        formatstatus = formatstatus + "&nbsp;&nbsp;&nbsp;&nbsp;赞" + str(praises_count)
    return formatstatus

def existcheck(number): #done
    if number!=0:
        return ""
    else:
        return "empty"

def zerohidden(number): #done
    if number==0:
        return ""
    else:
        return number

def gallerygenerate(jsondata): #done
    imageset = json.loads(jsondata)
    gallery = ""
    for image in imageset:
        gallery = gallery + pagelayout.div_thumb.format(size=image["size"],original=image["original"],thumbnail=image["thumbnail"])

    numberconvert = ["zero","one","two","three","four","five","six","seven","eight","nine"]

    back = '<div class="gallery with%s">%s\n\t\t\t\t\t</div>'%(numberconvert[len(imageset)],gallery)

    return back


def active_at(text): #done
    text = re.sub(r'@([^:|\s]+)(:|\s|$)','<a class="user" href="/u/\g<1>">@\g<1></a>\g<2>',text)
    return text

def timefriendly(timedata): #done

    nowtime = datetime.datetime.now()

    if timedata.date()==nowtime.date():

        subtime=(nowtime - timedata).seconds

        if subtime//60==0:
            return "刚刚"
            
        elif subtime//60<=59:
            return "%s 分钟前"%(subtime//60)

        elif subtime//3600<=12:
            return "%s 小时前"%(subtime//3600)
        else:
           return timedata.strftime('今天 %H:%M')

    elif timedata.date()==(nowtime-datetime.timedelta(days=1)).date():
        return timedata.strftime("昨天 %H:%M")
    else:
        return str(timedata.month) + "-" + str(timedata.day) + timedata.strftime(' %H:%M')



def numberfriendly(number):
    return number

def pickthumb(entrylist):
    thumbset = []
    for entry in entrylist:
        if entry[0]!="":
            imageset = json.loads(entry[0])
            for image in imageset:
                thumbset.append(image["thumbnail"])
                if len(thumbset) == 5:
                    return thumbset

    if len(thumbset)<5:
        for i in range(0,5 - len(thumbset)):
            thumbset.append("")

    return thumbset


def checkpicformat(jsondata):
    try:
        imageset = json.loads(jsondata)
    except:
        return 0

    if len(imageset)>9:
        return 0

    for image in imageset:
        if "size" in image:
            if re.search(r"^\d+x\d+$",image["size"])==None:
                return 0
        else:
            return 0

        if "thumbnail" in image:
            if re.search(r"^/photo/\d{10}/thumbnail/\d{10}\.(jpg|png|gif)$",image["thumbnail"])==None:
                return 0
        else:
            return 0

        if "original" in image:
            if re.search(r"^/photo/\d{10}/original/\d{10}\.(jpg|png|gif)$",image["original"])==None:
                return 0
        else:
            return 0

    return 1

def shielding(content):
    shielding_list = ["我也不知道有什么敏感词"]
    for words in shielding_list:
        if content.find(words)!=-1:
            return 1
    return 0


def getdevice(user_agnet):
    device_dict = {"iPhone":"iPhone","Windows":"Windows","iPad":"iPad","HUAWEI":"华为","ONEPLUS":"一加","MI ":"小米","vivo ":"vivo","OPPO":"OPPO","Letv":"乐视","Nexus":"Nexus","HTC_":"HTC","Macintosh":"macOS","LG-":"LG","SM-":"三星"}
    for keyword in device_dict:
        if re.search(keyword,user_agnet)!=None:
            return device_dict[keyword]
    return "网页版"


@asyncio.coroutine
def create_pool():
    global pool
    pool = yield from aiomysql.create_pool(host='localhost', port=3306,
                                           user='root', password='???',
                                           db='???', loop=loop,
                                           charset='utf8')


@asyncio.coroutine
def signin(request):

    if request.content_type!="application/x-www-form-urlencoded":
        return web.HTTPBadRequest(reason="error content type")

    session = yield from get_session(request)

    if request.content_type!="application/x-www-form-urlencoded":
        session.clear()
        return web.HTTPBadRequest(reason="unsupported content-type")

    data = yield from request.post()

    logging.info(str(data))
    
    if len(data)>2:
        session.clear()
        return web.HTTPBadRequest(reason="unneeded value")

    email = data['email'] if 'email' in data else None
    password = data['password'] if 'password' in data else None
    if email==None or password==None:
        session.clear()
        return web.HTTPBadRequest(reason="null value")

    password_sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest()

    # password = re.sub("\'","\\'",password)
    # password = re.sub('\"','\\"',password)

    user_check='''SELECT uid,active FROM user WHERE email ="%s" and password ="%s" and active = 1;'''%(email,password_sha1)

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT uid,active FROM user WHERE email =%s and password =%s',(email,password_sha1))
        if exist == 0:
            yield from cur.close()
            conn.close()
            session.clear()
            return web.HTTPForbidden(reason="login failed")

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

    if out[0][1] != 1:
        return web.HTTPForbidden(reason="not verfiy yet")
    
    session["uid"] = out[0][0]
    session["logintime"] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    return web.Response(text="login success")
  
@asyncio.coroutine
def signup(request):

    if request.content_type!="application/x-www-form-urlencoded":
        return web.HTTPBadRequest(reason="error content type")

    data = yield from request.post()
    if len(data)>3:
        return web.HTTPBadRequest()
    email = data['email'] if 'email' in data else None
    password = data['password'] if 'password' in data else None
    nickname = data['nickname'] if 'nickname' in data else None
    if email==None or password==None or nickname==None:
        return web.HTTPBadRequest()
    if email=='' or password=='' or nickname=='':
        return web.HTTPBadRequest()
    if re.search(r"^[\d|a-z|_]+?@[\d|a-z|_]+?\.[\d|a-z|_|.]+?$",email)==None:
        return web.HTTPBadRequest()

    regdate = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    password_sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest()

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        while True:

            uid = str(random.randint(0000000000,9999999999)).zfill(10)

            try:
                yield from cur.execute('INSERT INTO user (uid,email,password,nickname,introduction,posts_count,follows_count,fans_count,regdate,active)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(uid,email,password_sha1,nickname,"a freshman",0,0,0,regdate,0))
            except pymysql.err.IntegrityError as e:
                logging.info(e)
                if re.search(r"key 'PRIMARY'",e.args[1])!=None:
                    continue
                elif re.search(r"key 'email'",e.args[1])!=None:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPNotAcceptable(reason="email address already registered")
                elif re.search(r"key 'nickname'",e.args[1])!=None:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPNotAcceptable(reason="nickname has been used")
            else:
                break

        yield from conn.commit()
        yield from cur.close()
        conn.close()

    verify = uid + "+" + email + "+" + regdate
    verify_sha1 = hashlib.sha1(verify.encode('utf-8')).hexdigest()

    os.system("python sendcloud.py "+email+" "+nickname+" "+uid+" "+verify_sha1+"&")

    return web.Response(text="success")


@asyncio.coroutine
def verify(request):

    uid=request.match_info["uid"]
    hashmessage=request.match_info["hashmessage"]

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute("SELECT uid,email,regdate,active FROM user WHERE uid = '%s'"%uid)
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPBadRequest()

        out = yield from cur.fetchall()
        if out[0][3]==1:
            yield from cur.close()
            conn.close()
            return web.Response(text="already verified")

        verify = out[0][0] + "+" + out[0][1] + "+" + out[0][2].strftime('%Y/%m/%d %H:%M:%S')
        verify_sha1 = hashlib.sha1(verify.encode('utf-8')).hexdigest()

        if hashmessage!=verify_sha1:
            yield from cur.close()
            conn.close()
            return web.HTTPBadRequest()

        yield from cur.execute("UPDATE user SET active=1 WHERE uid = '%s';"%uid)
        yield from conn.commit()
        yield from cur.close()
        conn.close()

    try:
        shutil.copytree( "/home/oop2/weibo/userfile/sample", "/home/oop2/weibo/userfile/" + uid)
    except BaseException as e:
        logging.info(e)

    return web.Response(text="verify success")


@asyncio.coroutine
def signout(request):

    session = yield from get_session(request)
    session.clear()  
    return web.HTTPFound("/login.html")



@asyncio.coroutine
def indexpage(request):

    session = yield from get_session(request)
    if 'uid' not in session:
        return web.HTTPFound("/login.html")
        # uid = '0000000000'
    else:
        uid = session['uid']

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT user.uid,user.nickname FROM user WHERE user.uid= "%s";'%(uid))
        if exist == 0:
            yield from cur.close()
            conn.close()
            nickname = "微博用户"
        else:
            out = yield from cur.fetchall()
            yield from cur.close()
            conn.close()
            nickname = out[0][1]

    composepage = pagelayout.composepage.format(userid=uid)

    indexpage = pagelayout.indexpage.format(nickname=nickname,userid=uid,composepage=composepage,photoswipe_viewer=pagelayout.photoswipe_viewer)

    return web.Response(text=indexpage,content_type='text/html',charset='utf-8')


@asyncio.coroutine
def detailpage(request):

    pid = request.match_info["pid"]

    session = yield from get_session(request)
    if 'uid' not in session:
        uid = '0000000000'
    else:
        uid = session['uid']

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT post.pid,post.uid,user.nickname,post.posttime,post.device,post.posttext,post.rid,post.withpic,post.praises_count,post.comments_count,post.reposts_count FROM post,user WHERE post.pid = "%s" AND post.uid = user.uid'%(pid))
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound(text=pagelayout.emptypage,content_type='text/html')

        post = yield from cur.fetchall()
        praisecheck = yield from cur.execute('SELECT * FROM praise WHERE praise.pid = "%s" AND praise.uid = "%s";'%(uid,pid))

        if post[0][6]!="":
            rid = post[0][6]
            exist = yield from cur.execute('SELECT post.pid,post.uid,user.nickname,post.posttext,post.withpic,post.praises_count,post.comments_count,post.reposts_count FROM post,user WHERE post.pid = "%s" AND post.uid = user.uid'%(rid))
            if exist == 0:
                yield from cur.close()
                conn.close()
                repostbody = '<div class="repostbody"><p class="reposttext">抱歉，这条微博已经被作者删除</p><div class="repoststatus">None</div></div>'

            else:
                repost = yield from cur.fetchall()
                # yield from cur.close()
                # conn.close()

                if repost[0][4]!="":
                    gallery = gallerygenerate(repost[0][4])
                else:
                    gallery = '<div class="gallery withzero"></div>'


                repoststatus = statusformat(repost[0][5],repost[0][6],repost[0][7])
                repostbody = pagelayout.repostbody.format(rid=rid,uid=repost[0][1],nickname=repost[0][2],reposttext=active_at(repost[0][3]),repoststatus=repoststatus,gallery=gallery)

        else:
            repostbody = ""

        if uid!=post[0][1]:
            followcheck = yield from cur.execute('SELECT * FROM follow WHERE follow.uid = "%s" AND follow.fid = "%s";'%(uid,post[0][1]))
            yield from cur.close()
            conn.close()

            if followcheck==0:
                options = pagelayout.oneoption.format(optiontype="follow",optionvalue='uid="%s"'%post[0][1],optiontext="关注")
            else:
                options = pagelayout.oneoption.format(optiontype="following",optionvalue='uid="%s"'%post[0][1],optiontext="取消关注")
        else:
            options = pagelayout.oneoption.format(optiontype="delete",optionvalue='pid="%s"'%post[0][0],optiontext="删除")

        composepage = pagelayout.composepage.format(userid=uid)

        if post[0][7]!="":
            gallery = gallerygenerate(post[0][7])
        else:
            gallery = '<div class="gallery withzero"></div>'

        detailpage = pagelayout.detailpage.format(uid=post[0][1],nickname=post[0][2],pid=post[0][0],posttime=timefriendly(post[0][3]),device=post[0][4],posttext=active_at(post[0][5]),gallery=gallery,repostbody=repostbody,praisestatus=statusconvert[praisecheck],praises_count=post[0][8],comments_count=post[0][9],reposts_count=post[0][10],userid=uid)

        viewpage = pagelayout.viewpage.format(detailpage=detailpage,commentpage=pagelayout.commentpage,composepage=composepage,options=options,photoswipe_viewer=pagelayout.photoswipe_viewer)

    return web.Response(text=viewpage,content_type='text/html',charset='utf-8')


@asyncio.coroutine
def usersearch(request):

    nickname = request.match_info["nickname"]
    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT user.uid FROM user WHERE user.nickname = %s',(nickname))
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound(text=pagelayout.emptypage,content_type='text/html')
        uid = yield from cur.fetchall()
        yield from cur.close()
        conn.close()
    return web.HTTPFound("/u/"+uid[0][0])


@asyncio.coroutine
def listpage(request):
    pagetype = request.match_info["type"]
    # uid = request.match_info["uid"]
    if pagetype == "follow":
        listpage = pagelayout.listpage.format(title="关注")
    elif pagetype == "fan":
        listpage = pagelayout.listpage.format(title="粉丝")

    return web.Response(text=listpage,content_type='text/html',charset='utf-8')


@asyncio.coroutine
def albumpage(request):

    albumpage = pagelayout.albumpage.format(photoswipe_viewer=pagelayout.photoswipe_viewer)
    return web.Response(text=albumpage,content_type='text/html',charset='utf-8')


@asyncio.coroutine
def userpage(request):

    uid = request.match_info["uid"]

    session = yield from get_session(request)
    if 'uid' not in session:
        userid = '0000000000'
    else:
        userid = session['uid']

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT uid,nickname,introduction,posts_count,follows_count,fans_count FROM user WHERE uid = "%s"'%(uid))
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotFound(text=pagelayout.emptypage,content_type='text/html')

        userdetail = yield from cur.fetchall()

        if userid != uid:
            ufollow_check = yield from cur.execute('SELECT follow.fid FROM follow WHERE follow.uid = "%s" AND follow.fid = "%s";'%(userid,uid))
            followu_check = yield from cur.execute('SELECT follow.uid FROM follow WHERE follow.fid = "%s" AND follow.uid = "%s";'%(userid,uid))

            if ufollow_check == 0 and followu_check == 0:
                actiontype = "follow"
                followu = "false"
            elif ufollow_check == 0 and followu_check == 1:
                actiontype = "follow"
                followu = "true"
            elif ufollow_check == 1 and followu_check == 0:
                actiontype = "following"
                followu = "false"
            elif ufollow_check == 1 and followu_check == 1:
                actiontype = "mutual"
                followu = "true"

        else:
            actiontype = "edit"
            followu = "false"

        exist = yield from cur.execute('SELECT post.withpic FROM post WHERE post.uid = "%s" AND post.withpic != "" LIMIT 5;'%(uid))
        if exist == 0:
            album = pagelayout.album%("","","","","")
        else:
            picset = yield from cur.fetchall()
            album = pagelayout.album%tuple(pickthumb(picset))

        composepage = pagelayout.composepage.format(userid=uid)
        userpage = pagelayout.userpage.format(uid=userdetail[0][0],nickname=userdetail[0][1],actiontype=actiontype,followu=followu,introduction=userdetail[0][2],album=album,posts_count=numberfriendly(userdetail[0][3]),follows_count=numberfriendly(userdetail[0][4]),fans_count=numberfriendly(userdetail[0][5]),composepage=composepage,photoswipe_viewer=pagelayout.photoswipe_viewer)

        yield from cur.close()
        conn.close()

    return web.Response(text=userpage,content_type='text/html',charset='utf-8')


@asyncio.coroutine
def editpage(request):

    session = yield from get_session(request)
    if 'uid' not in session:
        return web.HTTPFound("/login.html")
    else:
        userid = session['uid']

    uid = request.match_info["uid"]

    if uid != userid:
        return web.HTTPForbidden(reason="no right to enter")

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute('SELECT user.uid,user.nickname,user.introduction FROM user WHERE user.uid = %s',(uid))
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPFound("/login.html")
        userinfo = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

    editpage = pagelayout.editpage.format(uid=userinfo[0][0],nickname=userinfo[0][1],introduction=userinfo[0][2])

    return web.Response(text=editpage,content_type='text/html',charset='utf-8')


@asyncio.coroutine
def infoset(request):

    session = yield from get_session(request)

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    if request.content_type!="multipart/form-data":
        return web.HTTPBadRequest(reason="error content type")

    try:
        data = yield from request.post()
    except:
        return web.HTTPBadRequest(reason="abnormal request")


    if 'nickname' in data:
        nickname = data['nickname']
    else:
        nickname = None

    if 'introduction' in data:
        introduction = data['introduction']
    else:
        introduction = None

    if nickname == None and introduction == None:
        return web.HTTPBadRequest(reason="required parameter missing")

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        try:
            if nickname != None and introduction == None:
                exist = yield from cur.execute('UPDATE user SET nickname = %s WHERE uid = %s',(nickname,uid))
            elif nickname == None and introduction != None:
                exist = yield from cur.execute('UPDATE user SET introduction = %s WHERE uid = %s',(introduction,uid))
            elif nickname != None and introduction != None:
                exist = yield from cur.execute('UPDATE user SET nickname = %s , introduction = %s WHERE uid = %s',(nickname,introduction,uid))
        except BaseException as e:
            logging.info(e)
            if e.args[1].find("key 'nickname'")!=-1:
                yield from cur.close()
                conn.close()
                return web.HTTPNotAcceptable(reason="nickname has been used")
        else:
            yield from conn.commit()
            yield from cur.close()
            conn.close()
            if exist == 0:
                return web.HTTPNotAcceptable(reason="no change") # default all user exist
            else:
                return web.HTTPNoContent()

@asyncio.coroutine
def pagingquery(request):

    choose = request.match_info['classify']

    query_parameter=request.rel_url.query

    if "id" in query_parameter:
        if re.search(r'^\d{16}$',query_parameter["id"])!=None:
            pid = query_parameter["id"]
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    if "page" in query_parameter:
        if re.search(r'^\d+$',query_parameter["page"])!=None:
            page = int(query_parameter["page"])
            if page == 0:
                return web.HTTPBadRequest(reason="page start at 1")
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")


    sql_repostquery = '''SELECT repost.rid,post.uid,user.nickname,repost.reposttime,post.posttext
                         FROM repost,post,user
                         WHERE repost.pid = "%s" AND repost.rid = post.pid AND user.uid = post.uid
                         ORDER BY repost.reposttime DESC
                         LIMIT %s,11;
                         '''%(pid,(page-1)*10)

                        # comment.cid,comment.pid,
    sql_commentquery = '''SELECT comment.uid,user.nickname,comment.commenttime,comment.commenttext
                          FROM comment,user 
                          WHERE comment.pid = "%s" AND comment.uid = user.uid
                          ORDER BY comment.commenttime DESC
                          LIMIT %s,11;
                          '''%(pid,(page-1)*10)

                        # ,praise.praisetime
    sql_praisequery = '''SELECT praise.uid,user.nickname
                         FROM praise,user
                         WHERE praise.pid = "%s" and praise.uid = user.uid
                         ORDER BY praise.praisetime DESC
                         LIMIT %s,11;
                         '''%(pid,(page-1)*10)

    if choose == "comments":
        sql_execute = sql_commentquery
    elif choose == "reposts":
        sql_execute = sql_repostquery
    elif choose == "praises":
        sql_execute = sql_praisequery

    # print(sql_execute)

    
    jsonback = {}

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute(sql_execute)
        if exist == 0:
            yield from cur.close()
            conn.close()

            jsonback["goon"] = 0
            jsonback["html"] = ""
            # return web.HTTPNotFound(reason="empty page")
            return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

    if len(out)<11:
        jsonback["goon"] = 0
        repeattime = len(out)
    else:
        jsonback["goon"] = 1
        repeattime = 10

    htmlback = ""

    if choose == "comments":
        for i in range(0,repeattime):
            htmlback = htmlback + pagelayout.onecomment.format(uid=out[i][0],nickname=out[i][1],commenttime=timefriendly(out[i][2]),commenttext=active_at(out[i][3]))

    elif choose == "reposts":
        for i in range(0,repeattime):
            htmlback = htmlback + pagelayout.onerepost.format(pid=out[i][0],uid=out[i][1],nickname=out[i][2],reposttime=timefriendly(out[i][3]),reposttext=active_at(out[i][4]))

    elif choose == "praises":
        for i in range(0,repeattime):
            htmlback = htmlback + pagelayout.onepraise.format(uid=out[i][0],nickname=out[i][1])

    jsonback["html"] = htmlback


    return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


asyncio.coroutine
def uploadimage(request):

    session = yield from get_session(request)
    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    if request.content_type!="multipart/form-data":
        return web.HTTPBadRequest(reason="error content type")

    query_parameter=request.rel_url.query

    if "type" in query_parameter:
        if query_parameter["type"] in {"compose":"","avatar":"","userbg":""}:
            imagetype = query_parameter["type"]
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    try:
        reader = yield from request.multipart()
    except BaseException as e:
        logging.info(e)
        return web.HTTPBadRequest(reason="abnormal request")

    get = yield from reader.next()

    userfilepath = '/home/oop2/weibo/userfile/'

    if os.path.exists(userfilepath + uid)==0:
        return web.HTTPInternalServerError()

    if os.path.exists(userfilepath + uid + "/thumbnail")==0:
        os.mkdir(userfilepath + uid + "/thumbnail")

    if os.path.exists(userfilepath + uid + "/original")==0:
        os.mkdir(userfilepath + uid + "/original")

    size = 0
    suffix = ''
    # hashcal = hashlib.md5()
  
    while True:
        try:
            chunk = yield from get.read_chunk()  # 8192 bytes by default
        except BaseException:
            return web.HTTPBadRequest()

        if not chunk:
            break

        if size == 0 : 

            if len(chunk)<4:
                return web.HTTPBadRequest(reason="unsupported file type")
 
            # top8=chunk[0:4].hex().upper()
            top8=''.join('{:02x}'.format(x) for x in chunk[0:4]).upper()

            if top8[0:6] == 'FFD8FF':
                suffix = ".jpg"
            elif top8[0:8] == '89504E47':
                suffix = ".png"
            elif top8[0:8] == '47494638':
                suffix = ".gif"
            else:
                return web.HTTPUnsupportedMediaType(reason="unsupported file type")

            while True:
                filename = str(int(time.time()))
                if os.path.exists(userfilepath + uid+"/original/" + filename + suffix)==0:
                    f = open(userfilepath + uid + "/original/" + filename + suffix,'wb')
                    break

        size = size + len(chunk)
        f.write(chunk)
        # hashcal.update(chunk)

        if size/1048576 > 2: #2MB is maxsize
            f.close()
            os.remove(userfilepath + uid + "/original/" + filename + suffix)
            return web.HTTPRequestEntityTooLarge(reason="file size overflow")
    
    # hashval = hashcal.hexdigest()
    f.close()

    try:
        img = Image.open(userfilepath + uid + "/original/" + filename + suffix)
        imgsize = img.size
        # print(img.mode)

        if imagetype=="avatar":
            if imgsize[0]!=imgsize[1]:
                os.remove(userfilepath + uid + "/original/" + filename + suffix)
                return web.HTTPBadRequest(reason="unqualified avatar image")
            else:
                img.resize((180,180))
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(userfilepath + uid + "/avatar.jpg", "JPEG")
                os.remove(userfilepath + uid + "/original/" + filename + suffix)
                return web.HTTPNoContent()# success

        elif imagetype=="userbg":
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(userfilepath + uid + "/userbg.jpg", "JPEG")
            os.remove(userfilepath + uid + "/original/" + filename + suffix)
            return web.HTTPNoContent()# success

        elif imagetype=="compose":
            img.thumbnail((240,240))
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(userfilepath + uid + "/thumbnail/" + filename + ".jpg", "JPEG")
            jsonback = {}
            jsonback["size"] = str(imgsize[0]) + "x" + str(imgsize[1])
            jsonback["original"] = "/photo/" + uid + "/original/"+ filename + suffix
            jsonback["thumbnail"] = "/photo/" + uid + "/thumbnail/"+ filename + ".jpg"

            return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

    except BaseException as e:
        logging.info(e)
        return web.HTTPInternalServerError()



@asyncio.coroutine
def createpost(request):

    session = yield from get_session(request)

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    if request.content_type!="multipart/form-data":
        return web.HTTPBadRequest(reason="error content type")

    try:
        data = yield from request.post()
    except:
        return web.HTTPBadRequest(reason="abnormal request")


    if 'content' in data:
        posttext = data['content']
    else:
        return web.HTTPBadRequest(reason="required value missing")

    if len(posttext)>140:
        return web.HTTPBadRequest(reason="text length over limit")

    if shielding(posttext)==1:
        return web.HTTPBadRequest(reason="contain sensitive words")


    if 'rid' in data:
        if re.search(r'^\d{16}$',data['rid'])!=None:
            rid = data['rid']
        else:
            return web.HTTPBadRequest(reason="parameter illegal")

        if 'withpic' in data:
            return web.HTTPBadRequest(reason="cannot repost with pic")
        else:
            withpic = None
    else:
        rid = None
        if 'withpic' in data:
            withpic = data['withpic']
            if checkpicformat(withpic)==0:
                return web.HTTPBadRequest(reason="parameter illegal")
        else:
            withpic = ""

    user_agent = request.headers["User-Agent"]
    device = getdevice(user_agent)

    if "Referer" in request.headers:
        referer = request.headers["Referer"]
        if referer.find("/status/")!=-1:
            contentback = "noneed"
        elif referer.find("/u/")!=-1:
            if referer.find(uid)!=-1:
                contentback = "need"
            else:
                contentback = "noneed"
        else:
            contentback = "need"
    else:
        contentback = "noneed"

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()

        if rid != None:# is a forward post

            exist = yield from cur.execute('SELECT post.pid,post.rid FROM post WHERE post.pid = "%s";'%(rid))
            if exist == 0:
                yield from cur.close()
                conn.close()
                return web.HTTPNotAcceptable(reason="nonexistent repost origin")

            out = yield from cur.fetchall()


            if out[0][1] != "":#origin's rid
                source_rid = out[0][1]
            else:
                source_rid = rid

            while True:


                st_split = list(('%.6f'%(time.time())).replace(".","")) #16 bit
                uid_split = list(uid) #10 bit

                st_choose = "".join(random.sample(st_split, 12)).replace(" ","")
                uid_choose = "".join(random.sample(uid_split, 4)).replace(" ","")

                pid = st_choose + uid_choose

                posttime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                try:
                    yield from cur.execute('INSERT INTO post (pid,uid,posttime,device,posttext,rid,withpic,praises_count,comments_count,reposts_count,hits) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(pid,uid,posttime,device,posttext,source_rid,"",0,0,0,0))
                except BaseException as e:

                    logging.info(e)
                    if e.args[1].find("key 'PRIMARY'")!=-1:
                        continue
                    elif e.args[1].find("FOREIGN KEY (`uid`)")!=-1:
                        yield from cur.close()
                        conn.close()
                        return web.HTTPUnauthorized()

                else:
                    yield from conn.commit()
                    break

            result = yield from cur.execute('SELECT repost.pid FROM repost WHERE repost.rid = "%s";'%(rid))


            insert_data = [(pid,rid,posttime)] # at least one

            out = yield from cur.fetchall()

            for line in out: #if result == 0 don't execute this
                oneentry = []
                oneentry.append(pid)
                oneentry.append(line[0])
                oneentry.append(posttime)
                insert_data.append(tuple(oneentry))

            try:
                yield from cur.executemany('INSERT INTO repost (rid,pid,reposttime) VALUES (%s,%s,%s)',insert_data)
            except BaseException as e:

                logging.info(e)
                if e.args[1].find("key 'PRIMARY'")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPInternalServerError()
                elif e.args[1].find("FOREIGN KEY (`pid`)")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPInternalServerError()

            else:
                yield from conn.commit()

        else: # is an original post

            while True:

                st_split = list(('%.6f'%(time.time())).replace(".","")) #16 bit
                uid_split = list(uid) #10 bit


                st_choose = "".join(random.sample(st_split, 12)).replace(" ","")
                uid_choose = "".join(random.sample(uid_split, 4)).replace(" ","")

                pid = st_choose + uid_choose

                posttime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                try:
                    yield from cur.execute('INSERT INTO post (pid,uid,posttime,device,posttext,rid,withpic,praises_count,comments_count,reposts_count,hits) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(pid,uid,posttime,device,posttext,"",withpic,0,0,0,0))
                except BaseException as e:

                    logging.info(e)
                    if e.args[1].find("key 'PRIMARY'")!=-1:
                        continue
                    elif e.args[1].find("FOREIGN KEY (`uid`)")!=-1:
                        yield from cur.close()
                        conn.close()
                        return web.HTTPUnauthorized()

                else:
                    yield from conn.commit()
                    break

        if contentback=="noneed":
            yield from cur.close()
            conn.close()
            return web.HTTPNoContent()

        elif contentback=="need":

            exist = yield from cur.execute('SELECT post.pid,post.uid,user.nickname,post.posttime,post.device,post.posttext,post.rid,post.withpic,post.praises_count,post.comments_count,post.reposts_count FROM post,user WHERE post.pid = "%s" AND post.uid = user.uid'%(pid))
            if exist == 0:
                yield from cur.close()
                conn.close()
                return web.HTTPInternalServerError()

            post = yield from cur.fetchall()
            praisecheck = yield from cur.execute('SELECT * FROM praise WHERE praise.pid = "%s" AND praise.uid = "%s";'%(uid,pid))

            if post[0][6]!="":
                origin_pid = post[0][6]
                exist = yield from cur.execute('SELECT post.pid,post.uid,user.nickname,post.posttext,post.withpic,post.praises_count,post.comments_count,post.reposts_count FROM post,user WHERE post.pid = "%s" AND post.uid = user.uid'%(origin_pid))
                if exist == 0:
                    yield from cur.close()
                    conn.close()
                    repostbody = '<div class="repostbody"><p class="reposttext">抱歉，这条微博已经被作者删除</p><div class="repoststatus">None</div></div>'
                else:
                    repost = yield from cur.fetchall()
                    yield from cur.close()
                    conn.close()

                    if repost[0][4]!="":
                        gallery = gallerygenerate(repost[0][4])
                    else:
                        gallery = gallery = '<div class="gallery withzero"></div>'

                    repoststatus = statusformat(repost[0][5],repost[0][6],repost[0][7])
                    repostbody = pagelayout.repostbody.format(rid=origin_pid,uid=repost[0][1],nickname=repost[0][2],reposttext=active_at(repost[0][3]),repoststatus=repoststatus,gallery=gallery)

            else:
                yield from cur.close()
                conn.close()
                repostbody = ""

            if post[0][7]!="":
                gallery = gallerygenerate(post[0][7])
            else:
                gallery = '<div class="gallery withzero"></div>'

            onepost = pagelayout.onepost.format(uid=post[0][1],nickname=post[0][2],pid=post[0][0],posttime=timefriendly(post[0][3]),device=post[0][4],posttext=active_at(post[0][5]),gallery=gallery,repostbody=repostbody,praisestatus=statusconvert[praisecheck],praises_exist=existcheck(post[0][8]),praises_count=zerohidden(post[0][8]),comments_exist=existcheck(post[0][9]),comments_count=zerohidden(post[0][9]),reposts_exist=existcheck(post[0][10]),reposts_count=zerohidden(post[0][10]))

            return web.Response(text=onepost,content_type='text/html',charset='utf-8')


@asyncio.coroutine
def destroypost(request):

    session = yield from get_session(request)

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    query_parameter=request.rel_url.query

    if "id" in query_parameter:
        if re.search(r'^\d{16}$',query_parameter["id"])!=None:
            pid = query_parameter["id"]
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()

        exist = yield from cur.execute('SELECT post.pid,post.uid,post.rid FROM post WHERE post.pid = "%s";'%(pid))
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPNotAcceptable(reason="nonexistent weibo")

        out = yield from cur.fetchall()
        if out[0][1]!=uid:
            return web.HTTPUnauthorized()

        yield from cur.execute('DELETE FROM repost WHERE repost.rid = "%s" OR repost.pid = "%s";'%(pid,pid))
        # if result == 0:
        #     yield from cur.close()
        #     conn.close()
        #     return web.HTTPInternalServerError()

        result = yield from cur.execute('DELETE FROM post WHERE post.pid = "%s";'%(pid))
        if result == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPInternalServerError()


        yield from conn.commit()
        yield from cur.close()
        conn.close()

    # return web.Response(text="success")
    return web.HTTPNoContent()


@asyncio.coroutine
def createcomment(request):

    session = yield from get_session(request)

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    if request.content_type!="multipart/form-data":
        return web.HTTPBadRequest(reason="error content type")

    try:
        data = yield from request.post()
    except:
        return web.HTTPBadRequest(reason="abnormal request")

    # logging.info(data)

    if 'content' in data:
        commenttext = data['content']
    else:
        return web.HTTPBadRequest(reason="required value missing")

    if len(commenttext)>140:
        return web.HTTPBadRequest(reason="text length over limit")

    if shielding(commenttext)==1:
        return web.HTTPBadRequest(reason="contain sensitive words")


    if 'pid' in data:
        if re.search(r'^\d{16}$',data['pid'])!=None:
            pid = data['pid']
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required value missing")


    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()

        while True:

            st_split = list(('%.6f'%(time.time())).replace(".","")) #16 bit
            uid_split = list(uid) #10 bit

            st_choose = "".join(random.sample(st_split, 12)).replace(" ","")
            uid_choose = "".join(random.sample(uid_split, 4)).replace(" ","")

            cid = st_choose + uid_choose

            commenttime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            try:
                yield from cur.execute('INSERT INTO comment (cid,pid,uid,commenttime,commenttext) VALUES(%s,%s,%s,%s,%s)',(cid,pid,uid,commenttime,commenttext))
            except BaseException as e:

                logging.info(e)
                if e.args[1].find("key 'PRIMARY'")!=-1:
                    continue
                elif e.args[1].find("FOREIGN KEY (`pid`)")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPNotAcceptable(reason="nonexistent weibo")
                elif e.args[1].find("FOREIGN KEY (`uid`)")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPUnauthorized()
            else:
                yield from conn.commit()
                break

        yield from cur.close()
        conn.close()

    return web.HTTPNoContent()

@asyncio.coroutine
def praiseoperation(request):

    operation = request.match_info["operation"]

    session = yield from get_session(request)

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        uid = session['uid']

    query_parameter=request.rel_url.query

    if "id" in query_parameter:
        if re.search(r'^\d{16}$',query_parameter["id"])!=None:
            pid = query_parameter["id"]
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        if operation == "create":
            try:
                yield from cur.execute('INSERT INTO praise (pid,uid,praisetime) VALUES(%s,%s,%s);',(pid,uid,datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
            except BaseException as e:
                # logging.info(e)
                if e.args[1].find("key 'PRIMARY'")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPNotAcceptable(reason="already praise")
                elif e.args[1].find("FOREIGN KEY (`pid`)")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPNotAcceptable(reason="nonexistent weibo")
                elif e.args[1].find("FOREIGN KEY (`uid`)")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPUnauthorized()

        elif operation == "destroy":
            result = yield from cur.execute('DELETE FROM praise WHERE praise.pid = "%s" AND praise.uid = "%s";'%(pid,uid))
            if result == 0:
                yield from cur.close()
                conn.close()
                return web.HTTPNotAcceptable(reason="not praise yet")

        yield from conn.commit()
        yield from cur.close()
        conn.close()

    return web.HTTPNoContent()
    # return web.Response(text="success")


@asyncio.coroutine
def followoperation(request):

    operation = request.match_info["operation"]

    session = yield from get_session(request)

    if 'uid' not in session:
        return web.HTTPUnauthorized()
    else:
        userid = session['uid']

    query_parameter=request.rel_url.query

    if "id" in query_parameter:
        if re.search(r'^\d{10}$',query_parameter["id"])!=None:
            uid = query_parameter["id"]
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        if operation == "add":
            try:
                yield from cur.execute('INSERT INTO follow (uid,fid,followtime) VALUES(%s,%s,%s);',(userid,uid,datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
            except BaseException as e:
                # logging.info(e)
                if e.args[1].find("key 'PRIMARY'")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPNotAcceptable(reason="already follow")
                elif e.args[1].find("FOREIGN KEY (`fid`)")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPNotAcceptable(reason="nonexistent user")
                elif e.args[1].find("FOREIGN KEY (`uid`)")!=-1:
                    yield from cur.close()
                    conn.close()
                    return web.HTTPUnauthorized()

        elif operation == "remove":
            result = yield from cur.execute('DELETE FROM follow WHERE follow.uid = "%s" AND follow.fid = "%s";'%(userid,uid))
            if result == 0:
                yield from cur.close()
                conn.close()
                return web.HTTPNotAcceptable(reason="not follow yet")

        yield from conn.commit()
        yield from cur.close()
        conn.close()

    return web.HTTPNoContent()
    # return web.Response(text="success")



@asyncio.coroutine
def feedquery(request):

    session = yield from get_session(request)

    if 'uid' not in session:
        userid = "0000000000"
        # return web.HTTPUnauthorized()
    else:
        userid = session['uid']

    querytype = request.match_info["type"]

    query_parameter=request.rel_url.query


    offset = 0

    if "page" in query_parameter:
        if re.search(r'^\d+$',query_parameter["page"])!=None:
            page = int(query_parameter["page"])
            offset = (page - 1) * 10
            if page == 0:
                return web.HTTPBadRequest(reason="page start from 1")
        else:
            return web.HTTPBadRequest(reason="parameter illegal")

    if querytype == "personal":
        if "id" in query_parameter:
            if re.search(r'^\d{10}$',query_parameter["id"])!=None:
                uid = query_parameter["id"]
            else:
                return web.HTTPBadRequest(reason="parameter illegal")
        else:
            return web.HTTPBadRequest(reason="required parameter missing")

    if querytype == "index" and "id" in query_parameter:
        return web.HTTPBadRequest(reason="parameter illegal")

    jsonback = {}

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()

        if querytype=="index":
            follows_count = yield from cur.execute('SELECT follow.fid FROM follow WHERE follow.uid = "%s";'%(userid))
            if follows_count !=0:
                followset = yield from cur.fetchall()
                where_part = ""
                for follow_uid in followset:
                    where_part = where_part + 'post.uid = "' + follow_uid[0] + '" OR '
                where_part = where_part + 'post.uid = "' + userid + '"'
                sql_execute = 'SELECT postcut.pid,postcut.uid,user.nickname,postcut.posttime,postcut.device,postcut.posttext,postcut.rid,postcut.withpic,postcut.praises_count,postcut.comments_count,postcut.reposts_count FROM (SELECT post.pid,post.uid,post.posttime,post.device,post.posttext,post.rid,post.withpic,post.praises_count,post.comments_count,post.reposts_count FROM post WHERE %s ORDER BY post.posttime DESC LIMIT %s,10) postcut,user WHERE postcut.uid = user.uid ORDER BY postcut.posttime DESC;'%(where_part,offset)
            else:
                sql_execute = 'SELECT post.pid,post.uid,user.nickname,post.posttime,post.device,post.posttext,post.rid,post.withpic,post.praises_count,post.comments_count,post.reposts_count FROM post,user WHERE post.uid = user.uid ORDER BY post.posttime DESC LIMIT %s,10'%(offset)

        elif querytype=="personal":
                sql_execute = 'SELECT post.pid,post.uid,user.nickname,post.posttime,post.device,post.posttext,post.rid,post.withpic,post.praises_count,post.comments_count,post.reposts_count FROM post,user WHERE post.uid = user.uid and post.uid = "%s" ORDER BY post.posttime DESC LIMIT %s,10'%(uid,offset)

        # print(sql_execute)

        exist = yield from cur.execute(sql_execute)
        if exist == 0:
            yield from cur.close()
            conn.close()
            jsonback["html"] = ""
            jsonback["goon"] = 0
            # return web.HTTPNotFound(reason="empty page")
            return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

        postfeed = yield from cur.fetchall()

        repost_body_set = {}
        praise_status_set = {}

        for post in postfeed:
            if post[6]!="":
                repost_body_set[post[6]] = '<div class="repostbody"><p class="reposttext">抱歉，这条微博已经被作者删除</p><div class="repoststatus">None</div></div>'
            praise_status_set[post[0]] = 0

        if len(praise_status_set)>0:
            where_part = ""
            for praise_pid in praise_status_set:
                where_part = where_part + 'praisecut.pid = "' + praise_pid + '" OR '
            where_part = where_part[0:-3]

            exist = yield from cur.execute('SELECT praisecut.pid FROM (SELECT praise.pid FROM praise WHERE praise.uid = "%s") praisecut WHERE %s;'%(userid,where_part))
            if exist != 0:
                praisedset = yield from cur.fetchall()
                for line in praisedset:
                    praise_status_set[line[0]] = 1


        if len(repost_body_set)>0:
            where_part = ""
            for repost_pid in repost_body_set:
                where_part = where_part + 'post.pid = "' + repost_pid + '" OR '
            where_part = where_part[0:-3]

            exist = yield from cur.execute('SELECT postcut.pid,postcut.uid,user.nickname,postcut.posttext,postcut.withpic,postcut.praises_count,postcut.comments_count,postcut.reposts_count FROM user,(SELECT post.pid,post.uid,post.posttext,post.withpic,post.praises_count,post.comments_count,post.reposts_count FROM post WHERE %s) postcut WHERE postcut.uid = user.uid;'%(where_part))
            if exist != 0:
                repostset = yield from cur.fetchall()
                for line in repostset:
                    repoststatus = statusformat(line[5],line[6],line[7])
                    if line[4]!="":
                        gallery = gallerygenerate(line[4])
                    else:
                        gallery = '<div class="gallery withzero"></div>'
                    onerepost = pagelayout.repostbody.format(rid=line[0],uid=line[1],nickname=line[2],reposttext=active_at(line[3]),repoststatus=repoststatus,gallery=gallery)
                    repost_body_set[line[0]] = onerepost


        yield from cur.close()
        conn.close()

    
    if len(postfeed)<10:
        jsonback["goon"] = 0
    else:
        jsonback["goon"] = 1

    htmlback = ""

    for post in postfeed:

        if post[7]!="":
            gallery = gallerygenerate(post[7])
        else:
            gallery = '<div class="gallery withzero"></div>'


        if post[6]!="":
            repostbody = repost_body_set[post[6]]
        else:
            repostbody = ""

        onepost = pagelayout.onepost.format(
            pid=post[0],
            uid=post[1],
            nickname=post[2],
            posttime=timefriendly(post[3]),
            device=post[4],
            posttext=active_at(post[5]),
            gallery=gallery,
            repostbody=repostbody,
            praisestatus=statusconvert[praise_status_set[post[0]]],
            praises_exist=existcheck(post[8]),
            praises_count=zerohidden(post[8]),
            comments_exist=existcheck(post[9]),
            comments_count=zerohidden(post[9]),
            reposts_exist=existcheck(post[10]),
            reposts_count=zerohidden(post[10])
            )

        htmlback = htmlback + onepost

    jsonback["html"] = htmlback

    return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


# code by LKH
@asyncio.coroutine
def albumquery(request):

    query_parameter=request.rel_url.query

    if "page" in query_parameter:
        if re.search(r'^\d+$',query_parameter["page"])!=None:
            page = int(query_parameter["page"])
            if page == 0:
                return web.HTTPBadRequest(reason="page start at 1")
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    if "id" in query_parameter:
        if re.search(r'^\d{10}$',query_parameter["id"])!=None:
            uid = query_parameter["id"]
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    jsonback = {}
    htmlback = ''

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        
        result = yield from cur.execute("SELECT withpic FROM post WHERE uid = '%s' AND withpic != '' ORDER BY posttime DESC LIMIT %s, 6 " % (uid, 5*(page-1) ) )
        if result == 0:
            yield from cur.close()
            conn.close()
            jsonback['html'] = ''
            jsonback['goon'] = 0
            return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

        photoset = yield from cur.fetchall()
        yield from cur.close()
        conn.close()

        if len(photoset) < 6:
            jsonback['goon'] = 0
            repeattime = len(photoset)
        else:
            jsonback['goon'] = 1
            repeattime = 5
            
        for i in range(0,repeattime):
            withpic_jsons = json.loads(photoset[i][0])
            for withpic_json in withpic_jsons:
                htmlback = htmlback + pagelayout.div_thumb.format(size=withpic_json['size'], original=withpic_json['original'], thumbnail=withpic_json['thumbnail'])

        jsonback['html'] = htmlback

    return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


@asyncio.coroutine
def userquery(request):

    session = yield from get_session(request)

    if 'uid' not in session:
        userid = "0000000000"
        # return web.HTTPUnauthorized()
    else:
        userid = session['uid']

    querytype = request.match_info["type"]

    query_parameter=request.rel_url.query

    offset = 0

    if "page" in query_parameter:
        if re.search(r'^\d+$',query_parameter["page"])!=None:
            page = int(query_parameter["page"])
            offset = (page - 1) * 20
            if page == 0:
                return web.HTTPBadRequest(reason="page start from 1")
        else:
            return web.HTTPBadRequest(reason="parameter illegal")

    if "id" in query_parameter:
        if re.search(r'^\d{10}$',query_parameter["id"])!=None:
            uid = query_parameter["id"]
        else:
            return web.HTTPBadRequest(reason="parameter illegal")
    else:
        return web.HTTPBadRequest(reason="required parameter missing")

    jsonback = {}

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()

        if querytype == "follows":
            sql_execute = 'SELECT follow.fid,user.nickname,user.introduction FROM follow,user WHERE follow.uid = "%s" AND follow.fid = user.uid ORDER BY followtime DESC LIMIT %s,21'%(uid,offset)
        elif querytype == "fans":
            sql_execute = 'SELECT follow.uid,user.nickname,user.introduction FROM follow,user WHERE follow.fid = "%s" AND follow.uid = user.uid ORDER BY followtime DESC LIMIT %s,21'%(uid,offset)

        result = yield from cur.execute(sql_execute)
        if result == 0:
            yield from cur.close()
            conn.close()
            jsonback["html"] = ""
            jsonback["goon"] = 0
            return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

        infoset = yield from cur.fetchall()

        if len(infoset) < 21:
            repeattime = len(infoset)
            jsonback["goon"] = 0
        else:
            repeattime = 20
            jsonback["goon"] = 1

        query_set = {}
        for i in range(0,repeattime):
            query_set[infoset[i][0]] = {"followu":0,"ufollow":0}

        fan_where_part = ""
        follow_where_part = ""
        for query_uid in query_set:
            fan_where_part = fan_where_part + 'fanset.uid = "' + query_uid + '" OR '
            follow_where_part = follow_where_part + 'followset.fid = "' + query_uid + '" OR '
        fan_where_part = fan_where_part[0:-3]
        follow_where_part = follow_where_part[0:-3]

        exist = yield from cur.execute('SELECT fanset.uid FROM (SELECT follow.uid FROM follow WHERE follow.fid = "%s") fanset WHERE %s;'%(userid,fan_where_part))
        if exist != 0:
            fanset = yield from cur.fetchall()
            for line in fanset:
                query_set[line[0]]["followu"] = 1


        exist = yield from cur.execute('SELECT followset.fid FROM (SELECT follow.fid FROM follow WHERE follow.uid = "%s") followset WHERE %s;'%(userid,follow_where_part))
        if exist != 0:
            followset = yield from cur.fetchall()
            for line in followset:
                query_set[line[0]]["ufollow"] = 1

        yield from cur.close()
        conn.close()

        userflow = ""

        for i in range(0,repeattime):

            if query_set[infoset[i][0]]["ufollow"]==0 and query_set[infoset[i][0]]["followu"]==0:
                icontype = "follow"
                followu = "false"

            elif query_set[infoset[i][0]]["ufollow"]==0 and query_set[infoset[i][0]]["followu"]==1:
                icontype = "follow"
                followu = "true"

            elif query_set[infoset[i][0]]["ufollow"]==1 and query_set[infoset[i][0]]["followu"]==0:
                icontype = "following"
                followu = "false"

            elif query_set[infoset[i][0]]["ufollow"]==1 and query_set[infoset[i][0]]["followu"]==1:
                icontype = "following"
                followu = "true"

            if infoset[i][0]==userid:
                icontype = "self"
                followu = "false"

            userflow = userflow + pagelayout.oneuser.format(uid=infoset[i][0],nickname=infoset[i][1],introduction=infoset[i][2],icontype=icontype,followu=followu)

        jsonback["html"] = userflow
        return web.Response(text=json.dumps(jsonback,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
  
    fernet_key = fernet.Fernet.generate_key()
    logging.info(fernet_key)
    secret_key = base64.urlsafe_b64decode(fernet_key)

    setup(app, EncryptedCookieStorage(secret_key,max_age=1296000))# 15days

    app.router.add_route('GET', '/', indexpage)
    app.router.add_route('POST', '/signup', signup)
    app.router.add_route('POST', '/signin', signin)
    app.router.add_route('GET', '/signout', signout)
    app.router.add_route('GET', '/u/{uid:[\d]{10}}/verify/{hashmessage:[\d|a-f]{40}}', verify)

    app.router.add_route('GET', '/u/{uid:[\d]{10}}', userpage)
    app.router.add_route('GET', '/u/{nickname}', usersearch)
    app.router.add_route('GET', '/u/{uid:[\d]{10}}/edit', editpage)

    app.router.add_route('GET', '/status/{pid:[\d]{16}}', detailpage)
    app.router.add_route('POST', '/api/info/set', infoset)

    app.router.add_route('GET', '/api/{classify:comments}/show', pagingquery)
    app.router.add_route('GET', '/api/{classify:reposts}/show', pagingquery)
    app.router.add_route('GET', '/api/{classify:praises}/show', pagingquery)

    app.router.add_route('POST', '/api/praises/{operation:create}', praiseoperation)
    app.router.add_route('POST', '/api/praises/{operation:destroy}', praiseoperation)

    app.router.add_route('POST', '/api/follows/{operation:add}', followoperation)
    app.router.add_route('POST', '/api/follows/{operation:remove}', followoperation)

    app.router.add_route('POST', '/api/images/upload', uploadimage)

    app.router.add_route('POST', '/api/posts/create', createpost)
    app.router.add_route('POST', '/api/posts/destroy', destroypost)
    app.router.add_route('POST', '/api/comments/create', createcomment)

    app.router.add_route('GET', '/feed/{type:index}', feedquery)
    app.router.add_route('GET', '/feed/{type:personal}', feedquery)

    app.router.add_route('GET', '/p/{type:follows}', userquery)
    app.router.add_route('GET', '/p/{type:fans}', userquery)
    app.router.add_route('GET', '/p/album', albumquery)

    app.router.add_route('GET', '/u/{uid:[\d]{10}}/{type:follow}', listpage)
    app.router.add_route('GET', '/u/{uid:[\d]{10}}/{type:fan}', listpage)
    app.router.add_route('GET', '/u/{uid:[\d]{10}}/photo', albumpage)

    srv = yield from loop.create_server(app.make_handler(access_log=None), '0.0.0.0', 5400)
    logging.info('Server started at port 5400...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool())
loop.run_until_complete(init(loop))
loop.run_forever()