# -*- coding: utf-8 -*-

import fbchat
import time
from options import *


class Client(fbchat.Client):

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **ķwargs)
        self.messages = list()

    def onMessage(self, message_object, thread_id, **kwargs):
        self.messages.append(message_object)
        for i in range(len(self.messages)):
             ts = (time.time() - 10 * 60) * 1000
             if self.messages[i].timestamp < ts:
                 del(self.messages[i])


if __name__ == "__main__":
    client = Client(FB_EMAIL, FB_PASSWORD, session_cookies=FB_SESSION)
    client.listen()

