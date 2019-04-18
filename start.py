# -*- coding: utf-8 -*-

from src._client import Client
from src._settings import FB_EMAIL, FB_PASSWORD, FB_SESSION, ALWAYS_ACTIVE


if __name__ == "__main__":
    client = Client(FB_EMAIL, FB_PASSWORD, session_cookies=FB_SESSION)
    client.listen(ALWAYS_ACTIVE)
