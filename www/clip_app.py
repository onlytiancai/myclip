# -*- coding: utf-8 -*-
import web
from datetime import datetime
from collections import defaultdict

import settings
import utils

db = web.database(**settings.DB_CONN)
render = utils.render.clip


class Index(object):
    def GET(self):
        cates = get_cates()
        return render.index(cates)


class New(object):
    def GET(self, cateid=0):
        return render.new()

    def POST(self, cateid=0):
        i = web.input()
        new_id = db.insert('clips', title=i.title, content=i.content,cateid=cateid,
                           created_time=datetime.now(), changed_time=datetime.now())
        db.insert('clips', pid=new_id, title=i.title, content=i.content,cateid=cateid,
                  created_time=datetime.now(), changed_time=datetime.now())
        return web.seeother('/cate/%s' % cateid)


class Show(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())[0]
        cate = get_cate(clip.cateid)
        return render.show(cate, clip)


class Edit(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())
        return render.edit(clip[0])

    def POST(self, id):
        i = web.input(title=u'无概要信息')
        db.update('clips', where="id=$id", vars=dict(id=id),
                  changed_time=datetime.now(), content=i.content)

        db.insert('clips', pid=id, title=i.title, content=i.content,
                  created_time=datetime.now(), changed_time=datetime.now())
        return web.seeother('/show/%s' % id)


class Delete(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())
        return render.delete(clip[0])

    def POST(self, id):
        db.delete('clips', where="id=$id or pid=$id", vars=dict(id=id))
        return web.seeother('/')


class ShowError(object):
    def GET(self):
        return render.showerror(web.input())


class HistoryList(object):
    def GET(self, id):
        input = web.input(page=1)
        page = int(input.page)
        if page < 1:
            page = 1
        pagesize = 100
        offset = (page - 1) * pagesize
        clip = db.select('clips', where='id=$id', vars=locals())
        rows = db.select('clips', where="pid=$pid", vars=dict(pid=id),
                         order="changed_time desc", limit=pagesize, offset=offset)
        group_clips = defaultdict(list)
        for row in rows:
            group_clips[row.changed_time.strftime('%Y-%m-%d')].append(row)
        return render.historylist(clip[0], group_clips, page)


class HistoryShow(object):
    def GET(self, pid, id):
        pclip = db.select('clips', where='id=$pid', vars=dict(pid=pid))
        clip = db.select('clips', where='id=$id', vars=dict(id=id))
        return render.historyshow(pclip[0], clip[0])


def get_cates():
    cates = [] 
    rows = db.select('clip_cate', where='pid=0')
    for row in rows:
        cate = web.storage(row)
        cate.subcates = db.select('clip_cate', where='pid=$pid',
                                  vars=dict(pid=cate.id))
        cates.append(cate)
    return cates


def get_cate(id):
    if int(id) == 0:
        return web.storage(id=0, name=u'其它')
    cate = db.select('clip_cate', where='id=$id', vars=dict(id=id))
    return cate[0]


def get_clips(cateid=0):
    rows = db.select('clips', where='cateid=$cateid and pid=0',
                     vars=dict(cateid=cateid))
    return rows


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
        db.insert('clip_cate', pid=pid, name=i.catename, created_time=datetime.now())
        return web.seeother('/cates')
