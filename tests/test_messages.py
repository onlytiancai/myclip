# -*- coding: utf-8 -*-
import sys; sys.path.append('www/')
import messages 

def test_default():
    messages.db.delete('messages', where='to_userid=2')
    msgid = messages.send_message(1, 2, 'test message')

    msg = messages.get_message(msgid)
    assert msg.content == 'test message'

    msgs = messages.get_messages(2)
    assert len(list(msgs)) == 1

    messages.read_message(msgid)
    msg = messages.get_message(msgid)
    assert msg.unread == 0
