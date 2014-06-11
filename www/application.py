# -*- coding: utf-8 -*-
import web

import utils
import clips
import users
import workreports


render = utils.render


class IndexHandler(object):
    def GET(self):
        return render.index()


urls = ["/", IndexHandler,
        "/clips", clips.app,
        "/users", users.app,
        "/workreport", workreports.app,
        ]


app = web.application(urls, globals())
app.notfound = utils.notfound
app.internalerror = utils.internalerror
app.add_processor(web.loadhook(utils.header_html))
app.add_processor(web.loadhook(utils.filter_input_loadhook))
wsgiapp = app.wsgifunc()

if __name__ == '__main__':
    app.run()
