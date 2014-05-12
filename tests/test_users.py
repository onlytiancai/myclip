# -*- coding: utf-8 -*-
import sys; sys.path.append('www/')
import web
import users


def test_default():
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
