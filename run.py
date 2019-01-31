# -*- coding: utf-8 -*-

from client import Client
from options import *


if __name__ == "__main__":
    client = Client(FB_EMAIL, FB_PASSWORD, session_cookies=FB_SESSION)
    client.listen(ALWAYS_ACTIVE)


