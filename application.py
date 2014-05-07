# -*- coding: utf-8 -*-
import os
import web
from datetime import datetime
from collections import defaultdict

tpl_dir = os.path.join(os.path.dirname(__file__), 'templates')
render = web.template.render(tpl_dir, base='layout')
db = web.database(dbn='mysql', host='localhost', user='root', passwd='password', db='myclip')

form = web.form.Form(web.form.Textbox("title", web.form.notnull, description=u"标题"),
                     web.form.Textarea("content", web.form.notnull, description="内容"),
                     web.form.Button("submit", type="submit", description="保存"),
                     )

def show_error(message, backurl='/'):
    return web.seeother('/showerror?message=%s&backurl=%s' % (message, backurl))

class Index(object):
    def GET(self):
        clips = db.select('clips', order="changed_time desc", where="pid = 0")
        return render.index(clips)


class New(object):
    def GET(self):
        return render.new()

    def POST(self):
        f = form()
        if f.validates():
            db.insert('clips', title=f.d.title, content=f.d.content,
                      created_time=datetime.now(), changed_time=datetime.now())
            return web.seeother('/')
        else:
            return show_error(u'标题和内容不能为空')


class Show(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())
        if clip:
            return render.show(clip[0])
        else:
            return web.notfound()

class Edit(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())
        if clip:
            return render.edit(clip[0])
        else:
            return web.notfound()

    def POST(self, id):
        f = form()
        if f.validates():
            clip = db.select('clips', where='id=$id', vars=dict(id=id))
            if clip:
                row = clip[0] # INFO:
                db.insert('clips', pid=id, title=row.title, content=row.content,
                          created_time=datetime.now(), changed_time=datetime.now())
                db.update('clips', where="id=$id", vars=dict(id=id),
                          changed_time=datetime.now(), title=f.d.title, content=f.d.content)
                return web.seeother('/show/%s' % id)
            else:
                return web.notfound()
        else:
            return show_error(u'标题和内容不能为空', '/edit/%s' % id)


class Delete(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())
        if clip:
            return render.delete(clip[0])
        else:
            return web.notfound()

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
        if clip:
            rows = db.select('clips', where="pid=$pid", vars=dict(pid=id), 
                              order="changed_time desc", limit=pagesize, offset=offset)
            group_clips = defaultdict(list)
            for row in rows:
                group_clips[row.changed_time.strftime('%Y-%m-%d')].append(row)
            return render.historylist(clip[0], group_clips, page)
        else:
            return web.notfound()

class HistoryShow(object):
    def GET(self, pid, id):
        pclip = db.select('clips', where='id=$pid', vars=dict(pid=pid))
        clip = db.select('clips', where='id=$id', vars=dict(id=id))
        return render.historyshow(pclip[0], clip[0])



urls = ["/", Index,
        "/new", New,
        "/show/(\d+)", Show,
        "/edit/(\d+)", Edit, 
        "/delete/(\d+)", Delete, 
        "/showerror", ShowError, 
        "/historylist/(\d+)", HistoryList,
        "/historyshow/(\d+)/(\d+)", HistoryShow,
        ]

app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

if __name__ == '__main__':
    app.run()
