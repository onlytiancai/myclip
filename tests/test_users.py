# -*- coding: utf-8 -*-
import sys; sys.path.append('www/')
import web
from nose.tools import assert_equal
from mock import Mock


import users
import utils

app = users.app


def skeeptest_default():
    users.db.delete('users', where="username='test_user'")
    users.create_user('test_user', '123456')

    conflict = False
    try:
        users.create_user('test_user', '123456')
    except web.conflict:
        conflict = True
    assert conflict


    assert users.verify_password('test_user', '123456')
    assert not users.verify_password('test_user', '654321')


    assert users.verify_password('test_user', '123456')
    users.change_password('test_user', '654321')
    assert users.verify_password('test_user', '654321')


def test_RegisterHandler():
    req = app.request('/register')
    assert_equal(req.status, '200 OK')

    users.create_user = Mock()
    utils.get_clientip= Mock(return_value='1.1.1.1')
    utils.password_strength = Mock(return_value=True)

    data = web.storage(login_email='a@a.com',
                       login_password='123456',
                       login_password2='123456')
    req = app.request('/register', method='POST', data=data)

    assert_equal(req.status, '303 See Other')
    assert_equal(req.headers['Location'], 'http://0.0.0.0:8080/register_successful')
    utils.password_strength.assert_called_once_with('123456')
    users.create_user.assert_called_once_with('a@a.com', '123456', '1.1.1.1')

    data.login_password2 = '654321'
    req = app.request('/register', method='POST', data=data)
    assert_equal(req.status, '303 See Other')
    assert req.headers['Location'].find('showerror')


def test_LoginHandler():
    req = app.request('/login')
    assert_equal(req.status, '200 OK')

    users.verify_password = Mock(return_value=True)
    utils.get_clientip= Mock(return_value='1.1.1.1')

    data = web.storage(login_email='a@a.com', login_password='123456')
    req = app.request('/login', method='POST', data=data)

    assert_equal(req.status, '303 See Other')
    assert_equal(req.headers['Location'], 'http://0.0.0.0:8080/')
    users.verify_password.assert_called_once_with('a@a.com', '123456', '1.1.1.1')

    users.verify_password = Mock(return_value=True)
    req = app.request('/login', method='POST', data=data)
    assert_equal(req.status, '303 See Other')
    assert req.headers['Location'].find('showerror')
