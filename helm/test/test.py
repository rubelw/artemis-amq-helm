#!/usr/bin/env python3

import stomp
import time

class MyListener(stomp.ConnectionListener):
    def __init__(self):
        self.msg_received =0
    def on_error(self, message):
        print('received an error "%s"' % message)
    def on_message(self,message):
        print('received a message "%s"' % message)

username='artemis'
password='artemis'
host='<EXTERNAL IP>'
port=61616
conn = stomp.Connection([(host,port)])
conn.set_listener('',MyListener())
print('connecting')
conn.connect(username,password, wait=True)
print('connecting')
conn.subscribe(destination="/queue/test", id=1, ack="auto")
time.sleep(2)
conn.send(body="this is a test", destination="/queue/test", content_type="text/blah", receipt="123")
time.sleep(1)
conn.disconnect()
