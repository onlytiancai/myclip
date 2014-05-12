# -*- coding: utf-8 -*-
import os
import web

tpl_dir = os.path.join(os.path.dirname(__file__), 'templates')
render = web.template.render(tpl_dir, base='layout')


def header_html():
    web.header('Content-Type', 'text/html; charset=UTF-8')


def notfound():
    web.ctx.status = '404 Not Found'
    return web.notfound(str(render._404()))


def internalerror():
    web.ctx.status = '500 Internal Server Error'
    return web.internalerror(str(render._500()))


def filter_input_loadhook():
    i = web.input()
    # 请求太大，直接返回http 400
    for k in i:
        if len(i[k]) > 102400:
            raise web.badrequest('request to large.')


def show_error(message, backurl='/'):
    return web.seeother('/showerror?message=%s&backurl=%s' % (message, backurl))


def get_clientip():
    return web.ctx.env.get('HTTP_X_REAL_IP', web.ctx.ip)


def password_strength(password):
    '''校验密码强度，必须包含大小写字母和数字
    >>> password_strength('fooBar09')
    True
    >>> password_strength('fooBar')
    False
    >>> password_strength('123456')
    False
    >>> password_strength('123456aB')
    True
    >>> password_strength('')
    False
    '''
    if len(password) < 6:
        return False
    from string import ascii_lowercase, ascii_uppercase, digits
    s_lc = set(ascii_lowercase)
    s_uc = set(ascii_uppercase)
    s_d = set(digits)
    return all(set(password) & x for x in (s_lc, s_uc, s_d))
