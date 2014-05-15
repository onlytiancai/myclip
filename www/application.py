# -*- coding: utf-8 -*-
import web

import utils
import clip_app 


urls = ["/", clip_app.Index,
        "/new/(\d+)", clip_app.New,
        "/show/(\d+)", clip_app.Show,
        "/edit/(\d+)", clip_app.Edit,
        "/delete/(\d+)", clip_app.Delete,
        "/showerror", clip_app.ShowError,
        "/historylist/(\d+)", clip_app.HistoryList,
        "/historyshow/(\d+)/(\d+)", clip_app.HistoryShow,
        "/cates", clip_app.CatesHandler,
        "/cate/(\d+)", clip_app.CateHandler,
        "/create_cate", clip_app.CreateCateHandler,
        "/create_cate/(\d+)", clip_app.CreateCateHandler,
        ]


app = web.application(urls, globals())
app.notfound = utils.notfound
app.internalerror = utils.internalerror
app.add_processor(web.loadhook(utils.header_html))
app.add_processor(web.loadhook(utils.filter_input_loadhook))
wsgiapp = app.wsgifunc()

if __name__ == '__main__':
    app.run()
