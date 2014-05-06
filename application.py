# -*- coding: utf-8 -*-
import os
import web
from datetime import datetime

tpl_dir = os.path.join(os.path.dirname(__file__), 'templates')
render = web.template.render(tpl_dir, base='layout')
db = web.database(dbn='mysql', host='localhost', user='root', passwd='password', db='myclip')

form = web.form.Form(web.form.Textbox("title", web.form.notnull, description=u"标题"),
                     web.form.Textarea("content", web.form.notnull, description="内容"),
                     web.form.Button("submit", type="submit", description="保存"),
                     )


class Index(object):
    def GET(self):
        clips = db.select('clips', order="changed_time desc")
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
            db.update('clips', where="id=$id", vars=dict(id=id),
                      changed_time=datetime.now(), title=f.d.title, content=f.d.content)
        return web.seeother('/show/%s' % id)


class Delete(object):
    def GET(self, id):
        clip = db.select('clips', where='id=$id', vars=locals())
        if clip:
            return render.delete(clip[0])
        else:
            return web.notfound()

    def POST(self, id):
        db.delete('clips', where="id=$id", vars=locals())
        return web.seeother('/')



urls = ["/", Index,
        "/new", New,
        "/show/(\d+)", Show,
        "/edit/(\d+)", Edit, 
        "/delete/(\d+)", Delete, 
        ]

app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

if __name__ == '__main__':
    app.run()
