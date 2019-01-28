# -*- coding: utf-8 -*-

import fbchat


class Client(fbchat.Client):

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **ķwargs)
        self.messages = list()

    def onMessage(self, message_object, thread_id, **kwargs):
        self.messages.append(message_object)


if __name__ == "__main__":
    client = Client("", "")
    client.listen()

