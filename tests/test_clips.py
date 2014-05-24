#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import sys; sys.path.append('www/')
from nose.tools import assert_equal
import web
from mock import Mock
import logging
from datetime import datetime

import clips

logging.basicConfig(level=logging.NOTSET)
app = clips.app


def test_get_cates():
    top_cates = [web.storage(id=1, name='1'), web.storage(id=2, name='2')]
    clips.get_top_cates = Mock(return_value=top_cates)

    sub_cates = [web.storage(id=11, name='11'), web.storage(id=22, name='22')]
    clips.get_subcates = Mock(return_value=sub_cates)

    cates = clips.get_cates()

    assert len(cates) == 2
    assert len(cates[0].subcates) == 2
    assert_equal(cates[0].subcates[0].id, 11)


def test_get_cate():
    cate = clips.get_cate(0)
    assert_equal(cate.name, u'其它')


def test_IndexHandler():
    req = app.request('/')
    assert_equal(req.status, '200 OK')


def test_NewHandler():
    clips.create_clip = Mock(return_value=1)

    req = app.request('/new/1')
    assert_equal(req.status, '200 OK')

    data = web.storage(title='test title', content='test content')
    req = app.request('/new/1', method='POST', data=data)
    assert_equal(req.status, '303 See Other')
    assert_equal(req.headers['Location'], 'http://0.0.0.0:8080/cate/1')


def test_EditHandler():
    clips.get_clip = Mock(return_value=web.storage(id=1, title='1', content='11'))

    req = app.request('/edit/1')
    clips.get_clip.assert_called_once_with('1')
    assert_equal(req.status, '200 OK')

    clips.modify_clip = Mock()

    data = web.storage(title='test title', content='test content')
    req = app.request('/edit/1', method='POST', data=data)

    clips.modify_clip.assert_called_once_with('test title', 'test content')
    assert_equal(req.status, '303 See Other')
    assert_equal(req.headers['Location'], 'http://0.0.0.0:8080/show/1')


def test_DeleteHandler():
    clips.get_clip = Mock(return_value=web.storage(id=1, title='1', content='11'))

    req = app.request('/delete/1')
    clips.get_clip.assert_called_once_with('1')
    assert_equal(req.status, '200 OK')

    clips.delete_clip = Mock()

    req = app.request('/delete/1', method='POST')
    clips.delete_clip.assert_called_once_with('1')


def test_HistoryListHandler():
    data = [web.storage(id=1, title='1', content='11',
            changed_time=datetime(2014, 05, 05),
            created_time=datetime(2014, 05, 05)),

            web.storage(id=1, title='1', content='11',
            changed_time=datetime(2014, 06, 05),
            created_time=datetime(2014, 05, 05)),
            ]

    clips.get_clip_history = Mock(return_value=data)

    historys = clips.get_clip_history(1, 1)
    historys = clips.group_history(historys)
    assert '2014-05-05' in historys
    assert '2014-06-05' in historys

    clips.get_clip = Mock(return_value=web.storage(id=1, title='1', content='11'))

    req = app.request('/historylist/1')

    assert_equal(req.status, '200 OK')


def test_HistoryShowHandler():
    clips.get_clip = Mock(return_value=web.storage(id=1, title='1', content='11',
                          created_time=datetime.now()))
    req = app.request('/historyshow/1/2')
    assert_equal(req.status, '200 OK')
    clips.get_clip.assert_any_call('1')
    clips.get_clip.assert_any_call('2')


def test_CatesHandler():
    clips.get_cates = Mock(return_value=[])
    req = app.request('/cates')
    assert_equal(req.status, '200 OK')


def test_CateHandler():
    clips.get_cate = Mock(return_value=web.storage(name='1', id=1))
    clips.get_clips = Mock(return_value=[])
    req = app.request('/cate/1')
    assert_equal(req.status, '200 OK')


def test_CreateCateHandler():
    req = app.request('/create_cate')
    assert_equal(req.status, '200 OK')

    clips.create_cate = Mock(return_value=1)
    data = web.storage(catename='11')
    req = app.request('/create_cate/1', method='POST', data=data)
    assert_equal(req.status, '303 See Other')
    assert_equal(req.headers['Location'], 'http://0.0.0.0:8080/cates')
