# -*- coding: utf-8 -*-

import re
import time

import fbchat
import requests
from fbchat.models import *

from ._settings import *


class Client(fbchat.Client):

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.messages = list()
        self.setDefaultThread(self.uid, ThreadType.USER)

    def onMessage(self, mid, message_object, thread_id, **kwargs):
        message_object.uid = mid
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
                unsendable_files = []
                for a in message.attachments:
                    if isinstance(a, ImageAttachment):
                        if a.is_animated:
                            files.append(a.animated_preview_url)
                        else:
                            url = a.large_preview_url or a.preview_url or a.thumbnail_url
                            if url:
                                files.append(url)
                    elif isinstance(a, VideoAttachment):
                        files.append(a.preview_url)
                    elif isinstance(a, AudioAttachment):
                        unsendable_files.append(a.url)
                    elif isinstance(a, FileAttachment):
                        r = requests.get(a.url)
                        if r.status_code == 200:
                            url = re.search("document\.location\.replace\(\"(.*)\"\);", r.text).group(1)
                            url = url.replace('\\/', '/')
                            files.append(url)

                author = self.fetchUserInfo(message.author)[message.author]
                message.reply_to_id = None
                self.send(Message("{} unsent the message:".format(author.name),
                                  mentions=[Mention(author.uid, length=len(author.name))]))
                if message.text or message.sticker:
                    self.send(message)
                if unsendable_files:
                    self.sendMessage("Attachments: \n{}".format("\n----------\n".join(unsendable_files)))
                if files:
                    self.sendRemoteFiles(files)
                self.messages = list(filter(lambda x: x is not message, self.messages))
                break
