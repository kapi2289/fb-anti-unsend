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
        for i in range(len(self.messages)):
             ts = (time.time() - 10 * 60) * 1000
             if self.messages[i].timestamp < ts:
                 print("Deleted {}".format(self.messages[i]))
                 del(self.messages[i])

    def onMessageUnsent(self, mid, author_id, **kwargs):
        print("Detected unsent {}".format(mid))
        if IGNORE_SELF and author_id == self.uid:
            return
        for i in range(len(self.messages)):
            if self.messages[i].uid == mid:
                print("Found {}".format(self.messages[i]))
                files = []
                for a in self.messages[i].attachments:
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
                if files:
                    self._sendFiles(files, self.messages[i], thread_id=self.uid, thread_type=ThreadType.USER)
                else:
                    self.send(self.messages[i], thread_id=self.uid, thread_type=ThreadType.USER)
                del(self.messages[i])
                break


if __name__ == "__main__":
    client = Client(FB_EMAIL, FB_PASSWORD, session_cookies=FB_SESSION)
    client.listen()

