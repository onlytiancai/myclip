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
        if len(i[k]) > 10240:
            raise web.badrequest('request to large.')

def show_error(message, backurl='/'):
    return web.seeother('/showerror?message=%s&backurl=%s' % (message, backurl))
