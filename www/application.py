# -*- coding: utf-8 -*-
import web

import utils
import clips 


urls = ["/", clips.IndexHandler,
        "/new/(\d+)", clips.NewHandler,
        "/show/(\d+)", clips.ShowHandler,
        "/edit/(\d+)", clips.EditHandler,
        "/delete/(\d+)", clips.DeleteHandler,
        "/showerror", clips.ShowErrorHandler,
        "/historylist/(\d+)", clips.HistoryListHandler,
        "/historyshow/(\d+)/(\d+)", clips.HistoryShowHandler,
        "/cates", clips.CatesHandler,
        "/cate/(\d+)", clips.CateHandler,
        "/create_cate", clips.CreateCateHandler,
        "/create_cate/(\d+)", clips.CreateCateHandler,
        ]


app = web.application(urls, globals())
app.notfound = utils.notfound
app.internalerror = utils.internalerror
app.add_processor(web.loadhook(utils.header_html))
app.add_processor(web.loadhook(utils.filter_input_loadhook))
wsgiapp = app.wsgifunc()

if __name__ == '__main__':
    app.run()
