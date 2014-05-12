# -*- coding: utf-8 -*-
import web

import settings

db = web.database(**settings.DB_CONN)


def send_message(_from, to, message, msgtype=0):
    now = web.SQLLiteral("NOW()")
    return db.insert('messages', from_userid=_from, to_userid=to, created_time=now,
                     content=message, msgtype=msgtype, unread=1)


def get_messages(to, page=1):
    page = int(page)
    if page < 1:
        page = 1
    pagesize = 20
    offset = (page - 1) * pagesize

    rows = db.select('messages', where="to_userid=$to", vars={'to': to},
                     order='created_time desc', limit=pagesize, offset=offset)
    return rows


def get_message(msgid):
    rows = db.select('messages', where='id=$id', vars={'id': msgid})
    return rows[0] if rows else None


def read_message(msgid):
    db.update('messages', where='id=$id', vars={'id': msgid}, unread=0)


