# -*- coding: utf-8 -*-
import web
import random
from hashlib import md5

import settings
import utils

db = web.database(**settings.DB_CONN)
render = utils.render.users


def _gen_salt():
    return str(random.randint(1, 1024 * 1024))


def _gen_password(password, salt=None):
    password = password + str(salt)
    return md5(password).hexdigest().upper()


def create_user(username, password, clientip='0.0.0.0', usertype=0):
    username = username.lower()
    if exists_user(username):
        raise web.conflict()
    salt = _gen_salt()
    password = _gen_password(password, salt)
    now = web.SQLLiteral("NOW()")

    db.insert('users', username=username, password=password, salt=salt,
              usertype=usertype, nickname=username, openid='',
              register_time=now, register_ip=clientip,
              lastlogin_time=now, lastlogin_ip=clientip)
     

def change_password(username, password):
    salt = _gen_salt()
    password = _gen_password(password, salt)
    db.update('users', where='username=$username', vars={'username': username},
              password=password, salt=salt)


def verify_password(username, password, clientip='0.0.0.0'):
    user = get_user_by_username(username)
    password = _gen_password(password, user.salt)
    if password == user.password:
        now = web.SQLLiteral("NOW()")
        db.update('users', where='username=$username', vars={'username': username},
                  lastlogin_time=now, lastlogin_ip=clientip)
        return True
    else:
        return False


def get_user_by_username(username):
    rows = db.select('users', where="username=$username",
                     vars={'username': username})
    if not rows:
        raise web.notfound()
    return rows[0]


def exists_user(username):
    rows = db.select('users', where="username=$username",
                     vars={'username': username})
    return bool(rows)


class IndexHandler(object):
    pass


class LoginHandler(object):
    pass


class RegisterHandler(object):
    def GET(self):
        return render.register()

    def POST(self):
        i = web.input()
        clientip = utils.get_clientip()

        if not utils.password_strength(i.login_password):
            return utils.show_error(u'密码强度太弱')


        create_user(i.login_email, i.login_password, clientip)
        return web.seeother('/register_successful')


urls = ["/", IndexHandler,
        "/login", LoginHandler,
        "/register", RegisterHandler,
        ]


app = web.application(urls, globals())
