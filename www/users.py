# -*- coding: utf-8 -*-
import web
import random
from hashlib import md5

import settings

db = web.database(**settings.DB_CONN)


def create_user(username, password, usertype=0):
    username = username.lower()
    if exists_user(username):
        raise web.conflict()

    salt = str(random.randint(1, 1024 * 1024))
    password = password + salt
    password = md5(password).hexdigest().upper()
    db.insert('users', username=username, password=password, salt=salt,
              usertype=usertype, created_time=web.SQLLiteral("NOW()"),
              nickname=username, openid='')
     

def change_password(username, password):
    user = get_user_by_username(username)
    password = password + str(user.salt)
    password = md5(password).hexdigest().upper()
    db.update('users', where='username=$username', vars={'username': username},
              password=password)


def verify_password(username, password):
    user = get_user_by_username(username)
    password = password + str(user.salt)
    password = md5(password).hexdigest().upper()
    return password == user.password


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
# nosetests users.py -s --with-cov --cover-package=users

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
