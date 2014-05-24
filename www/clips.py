# -*- coding: utf-8 -*-
import web
from datetime import datetime
from collections import defaultdict

import settings
import utils

db = web.database(**settings.DB_CONN)
render = utils.render.clip

# === modle


def get_top_cates():
    return db.select('clip_cate', where='pid=0')


def get_subcates(pid):
    return db.select('clip_cate', where='pid=$pid', vars=dict(pid=pid))


def get_cates():
    cates = []
    rows = get_top_cates()
    for row in rows:
        cate = web.storage(row)
        cate.subcates = get_subcates(row.id)
        cates.append(cate)
    return cates


def get_cate(id):
    if int(id) == 0:
        return web.storage(id=0, name=u'其它')
    cate = db.select('clip_cate', where='id=$id', vars=dict(id=id))
    return cate[0]


def create_cate(pid, name):
    db.insert('clip_cate', pid=pid, name=name, created_time=datetime.now())


def get_clips(cateid=0):
    rows = db.select('clips', where='cateid=$cateid and pid=0',
                     vars=dict(cateid=cateid))
    return rows


def create_clip(title, content, cateid):
    new_id = db.insert('clips', title=title, content=content, cateid=cateid,
                       created_time=datetime.now(), changed_time=datetime.now())
    db.insert('clips', pid=new_id, title=title, content=content, cateid=cateid,
              created_time=datetime.now(), changed_time=datetime.now())
    return new_id


def modify_clip(title, content):
    db.update('clips', where="id=$id", vars=dict(id=id),
              changed_time=datetime.now(), content=content)

    db.insert('clips', pid=id, title=title, content=content,
              created_time=datetime.now(), changed_time=datetime.now())


def get_clip(id):
    clip = db.select('clips', where='id=$id', vars=locals())
    return clip[0]


def delete_clip(id):
    db.delete('clips', where="id=$id or pid=$id", vars=dict(id=id))


def get_clip_history(id, page, pagesize=100):
    page = int(page)
    if page < 1:
        page = 1
    offset = (page - 1) * pagesize
    rows = db.select('clips', where="pid=$pid", vars=dict(pid=id),
                     order="changed_time desc", limit=pagesize, offset=offset)
    return rows


def group_history(rows):
    group_clips = defaultdict(list)
    for row in rows:
        group_clips[row.changed_time.strftime('%Y-%m-%d')].append(row)
    return group_clips


# === web Handler
class IndexHandler(object):
    def GET(self):
        cates = get_cates()
        return render.index(cates)


class NewHandler(object):
    def GET(self, cateid=0):
        return render.new()

    def POST(self, cateid=0):
        i = web.input()
        create_clip(i.title, i.content, cateid)
        return web.seeother('/cate/%s' % cateid)


class ShowHandler(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())[0]
        cate = get_cate(clip.cateid)
        return render.show(cate, clip)


class EditHandler(object):
    def GET(self, id):
        clip = get_clip(id)
        return render.edit(clip)

    def POST(self, id):
        i = web.input(title=u'无概要信息')
        modify_clip(i.title, i.content)
        return web.seeother('/show/%s' % id)


class DeleteHandler(object):
    def GET(self, id):
        clip = get_clip(id)
        return render.delete(clip)

    def POST(self, id):
        delete_clip(id)
        return web.seeother('/')


class ShowErrorHandler(object):
    def GET(self):
        return render.showerror(web.input())


class HistoryListHandler(object):
    def GET(self, id):
        i = web.input(page=1)
        clip = get_clip(id)
        historys = get_clip_history(id, i.page)
        historys = group_history(historys)
        return render.historylist(clip, historys, i.page)


class HistoryShowHandler(object):
    def GET(self, pid, id):
        pclip = get_clip(pid) 
        clip = get_clip(id) 
        return render.historyshow(pclip, clip)


class CatesHandler(object):
    def GET(self):
        cates = get_cates()
        return render.cates(cates)


class CateHandler(object):
    def GET(self, cateid):
        cate = get_cate(cateid)
        return render.cate(cate, get_clips(cateid))
        

class CreateCateHandler(object):
    def GET(self, pid=0):
        return render.create_cate()

    def POST(self, pid=0):
        i = web.input()
        create_cate(i.catename, pid)
        return web.seeother('/cates')

urls = ["/", IndexHandler,
        "/new/(\d+)", NewHandler,
        "/show/(\d+)", ShowHandler,
        "/edit/(\d+)", EditHandler,
        "/delete/(\d+)", DeleteHandler,
        "/showerror", ShowErrorHandler,
        "/historylist/(\d+)", HistoryListHandler,
        "/historyshow/(\d+)/(\d+)", HistoryShowHandler,
        "/cates", CatesHandler,
        "/cate/(\d+)", CateHandler,
        "/create_cate", CreateCateHandler,
        "/create_cate/(\d+)", CreateCateHandler,
        ]


app = web.application(urls, globals())
