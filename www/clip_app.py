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
        clips = db.select('clips', order="changed_time desc", where="pid = 0")
        return render.index(clips)


class New(object):
    def GET(self):
        return render.new()

    def POST(self):
        i = web.input()
        new_id = db.insert('clips', title=i.title, content=i.content,
                           created_time=datetime.now(), changed_time=datetime.now())
        db.insert('clips', pid=new_id, title=i.title, content=i.content,
                  created_time=datetime.now(), changed_time=datetime.now())
        return web.seeother('/')


class Show(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())
        return render.show(clip[0])


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
