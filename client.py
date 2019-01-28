# -*- coding: utf-8 -*-

import fbchat


class Client(fbchat.Client):
    pass


if __name__ == "__main__":
    client = Client("", "")
    client.listen()

