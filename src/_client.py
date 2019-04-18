# -*- coding: utf-8 -*-

import time

import fbchat
from fbchat.models import *

from ._settings import *


class Client(fbchat.Client):

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.messages = list()
        self.setDefaultThread(self.uid, ThreadType.USER)

    def onMessage(self, message_object, thread_id, **kwargs):
        self.messages.append(message_object)
        for message in self.messages:
            ts = (time.time() - 10 * 60) * 1000
            if message.timestamp < ts:
                self.messages = list(filter(lambda x: x is not message, self.messages))

    def onMessageUnsent(self, mid, author_id, **kwargs):
        if IGNORE_SELF and author_id == self.uid:
            return
        for message in self.messages:
            if message.uid == mid:
                files = []
                for a in message.attachments:
                    if isinstance(a, ImageAttachment):
                        url = a.large_preview_url
                    elif isinstance(a, VideoAttachment):
                        url = a.preview_url
                    elif isinstance(a, AudioAttachment):
                        url = a.url
                    elif isinstance(a, FileAttachment):
                        url = a.url
                    else:
                        continue
                    files.append(url)
                author = self.fetchUserInfo(message.author)[message.author]
                self.send(Message("{} unsent the message:".format(author.name),
                                  mentions=[Mention(author.uid, length=len(author.name))]))
                if files:
                    self.sendMessage("Attachments: \n{}".format("\n----------\n".join(files)))
                if message.text or message.sticker:
                    self.send(message)
                self.messages = list(filter(lambda x: x is not message, self.messages))
                break
