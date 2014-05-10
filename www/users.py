# -*- coding: utf-8 -*-
import web
import random
from hashlib import md5

import settings

db = web.database(**settings.DB_CONN)


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

# ======================test cases =================
# nosetests users.py -s --with-cov


def test_create_user():
    db.delete('users', where="username='test_user'")
    create_user('test_user', '123456')


def test_create_user_conflict():
    db.delete('users', where="username='test_user'")
    create_user('test_user', '123456')
    conflict = False
    try:
        create_user('test_user', '123456')
    except web.conflict:
        conflict = True
    assert conflict


def test_verify_password():
    db.delete('users', where="username='test_user'")
    create_user('test_user', '123456')
    assert verify_password('test_user', '123456')
    assert not verify_password('test_user', '654321')


def test_change_password():
    db.delete('users', where="username='test_user'")
    create_user('test_user', '123456')
    assert verify_password('test_user', '123456')
    change_password('test_user', '654321')
    assert verify_password('test_user', '654321')
