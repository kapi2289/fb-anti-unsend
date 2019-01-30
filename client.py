# -*- coding: utf-8 -*-

import fbchat
import time
from options import *
from fbchat.models import *


class Client(fbchat.Client):

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.messages = list()

    def onMessage(self, message_object, thread_id, **kwargs):
        self.messages.append(message_object)
        print("Received {}".format(message_object))
        for message in self.messages:
             ts = (time.time() - 10 * 60) * 1000
             if message.timestamp < ts:
                 print("Deleted {}".format(message))
                 self.messages = list(filter(x: x is not message, self.messages))

    def onMessageUnsent(self, mid, author_id, **kwargs):
        print("Detected unsent {}".format(mid))
        if IGNORE_SELF and author_id == self.uid:
            return
        for message in self.messages:
            if message.uid == mid:
                print("Found {}".format(message))
                files = []
                for a in message.attachments:
                    if isinstance(a, ImageAttachment):
                        mime = "image/gif" if a.is_animated else "image/png"
                    elif isinstance(a, VideoAttachment):
                        mime = "video/mpeg"
                    elif isinstance(a, AudioAttachment):
                        mime = "audio/mp3"
                    elif isinstance(a, FileAttachment):
                        mime = None
                    else:
                        continue
                    files.append((a.uid, mime))
                author = self.fetchUserInfo(message.author)[message.author]
                self.sendMessage("{} unsent the message:".format(author.name), thread_id=self.uid, thread_type=ThreadType.USER)
                if files:
                    self._sendFiles(files, message, thread_id=self.uid, thread_type=ThreadType.USER)
                else:
                    self.send(message, thread_id=self.uid, thread_type=ThreadType.USER)
                self.messages = list(filter(x: x is not  message, self.messages))
                break


if __name__ == "__main__":
    client = Client(FB_EMAIL, FB_PASSWORD, session_cookies=FB_SESSION)
    client.listen()

