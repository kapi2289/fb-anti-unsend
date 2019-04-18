# Facebook Messenger anti-unsend

## Description
Are you getting angry when someone unsends the message and you can't see it? This project is for you! When someone will unsend the message, you'll get it immediately in your conversation with yourself.

## Installation
Clone the repo
```console
$ git clone https://github.com/kapi2289/fb-anti-unsend.git
$ cd fb-anti-unsend
```

Create the `.env` file and edit it with your favourite text editor
```console
$ cp .env.example .env
$ nano .env
```

Install dependencies
```console
$ pip install --user pipenv
$ pipenv install
```

And now you can run it!
```console
$ pipenv run python start.py
```

## Tips
This project is using `fbchat` library. You can get your session, turn it to JSON and save it to the `session.json` file
```python
import fbchat
import json
client = fbchat.Client("you@example.com", "password")
session = client.getSession()

with open("session.json", 'w') as f:
	f.write(json.dumps(session))
```

And then you need to set the `FB_USE_SESSION` option to `true` in your `.env` file
