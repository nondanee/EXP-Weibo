import asyncio
import aiomysql
import time
import datetime
import random
import base64
import os
import ssl
import re
import hashlib
import pymysql
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import logging
logging.basicConfig(level=logging.INFO,format='%(message)s')

@asyncio.coroutine
def create_pool():
    global pool
    pool = yield from aiomysql.create_pool(host='localhost', port=3306,
                                           user='root', password='',
                                           db='weibo', loop=loop,
                                           charset='utf8')


@asyncio.coroutine
def index(request):
    session = yield from get_session(request)
    uid = session['uid'] if 'uid' in session else None
    logintime = session['logintime'] if 'logintime' in session else None
    text = 'uid: {},logintime: {}'.format(uid,logintime)
    return web.Response(text=text)


@asyncio.coroutine
def signin(request):
    data = yield from request.post()
    session = yield from get_session(request)

    if 'uid' in session and 'logintime' in session:
        return web.Response(text="already login")

    if len(data)>2:
        return web.HTTPBadRequest()
    email = data['email'] if 'email' in data else None
    password = data['password'] if 'password' in data else None
    if email==None or password==None:
        return web.HTTPBadRequest()

    password = re.sub("\'","\\'",password)
    password = re.sub('\"','\\"',password)
    assword = re.sub('\\;',';',password)
    user_check='''SELECT uid FROM user WHERE email ="%s" and password ="%s";'''%(email,password)
    #print(user_check)

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        exist = yield from cur.execute(user_check)
        if exist == 0:
            yield from cur.close()
            conn.close()
            return web.HTTPForbidden()

        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()
    
    session["uid"] = out[0][0]
    session["logintime"] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    return web.Response(text="login success")

@asyncio.coroutine
def signup(request):
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
    uid = str(random.randint(0000000000,9999999999)).zfill(10)
    
    verify = uid + "+" + email + "+" + regdate
    verify_sha1 = hashlib.sha1(verify.encode('utf-8')).hexdigest()


    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        try:
            yield from cur.execute('INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s)',(uid,email,password,nickname,regdate,0))
        except pymysql.err.IntegrityError as e:
            print(e)
            if re.search(r"key 'PRIMARY'",e.args[1])!=None:
                yield from cur.close()
                conn.close()
                return web.HTTPNotImplemented()
            elif re.search(r"key 'email'",e.args[1])!=None:
                print(e)
                yield from cur.close()
                conn.close()
                return web.Response(text="email address already registered")
            elif re.search(r"key 'nickname'",e.args[1])!=None:
                print(e)
                yield from cur.close()
                conn.close()
                return web.Response(text="nickname has been used")
        else:
            yield from conn.commit()
            yield from cur.close()
            conn.close()

    os.system("python sendverifyemail.py "+email+" "+nickname+" "+uid+" "+verify_sha1+"&")

    return web.Response(text="ok")


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

    return web.Response(text="verify success")


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
  
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    app.router.add_route('GET', '/', index)
    app.router.add_route('POST', '/signin', signin)
    app.router.add_route('POST', '/signup', signup)
    app.router.add_route('GET', '/u/{uid:[\d]{10}}/verify/{hashmessage:[\d|a-f]{40}}', verify)
    srv = yield from loop.create_server(app.make_handler(access_log=None), '0.0.0.0', 8000)
    print('Server started at port 8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool())
loop.run_until_complete(init(loop))
loop.run_forever()
