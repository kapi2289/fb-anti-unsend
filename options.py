# -*- coding: utf-8 -*-

import json
import os
from dotenv import load_dotenv

load_dotenv()

def is_true(a):
    return str(a).lower() in ("true","yes","1")

FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")
FB_USE_SESSION = is_true(os.getenv("FB_USE_SESSION"))
FB_SESSION_FILE = "session.json" or os.getenv("FB_SESSION_FILE")

with open(FB_SESSION_FILE) as f:
    FB_SESSION = json.loads(f.read())

IGNORE_SELF = is_true(os.getenv("IGNORE_SELF"))

