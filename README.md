About
=====

![madeatdotastro](https://img.shields.io/badge/Made%20at-%23dotastro-brightgreen.svg)


AstroBadger - getting in the habit of writing 200 academic words per
day, every day.

This was inspired by [750 words](http://750words.com), a website that
encourages you to write 750 words every day and collect badges for
longer and longer runs of days in a row that you keep going.

750 words is too much for writing academic papers, though, so we though
200 words would be simpler.

During the pitch at dotastro8, Becky misheard 'badges' as 'badgers' and
so you are awarded badgers for the number of days you write.

Requirements
============

The client is a Chrome extension.

You can load it by accessing chrome://extensions then enabling Developer
Mode and then Loading the directory chrome_4/ in the astrobadger/
directory.

Usage
=====

Highlight the text you want to word count with your mouse, and click on
the badger to register your word count for the day. You will get a popup
window congratulating you along with a number of badgers representing
the number of days in a row you have written.


Testing the server on a local machine
=====================================

Making a conda environment with Flask dependencies:

    conda create --name badger4 python=2 click Flask sqlalchemy gunicorn itsdangerous Jinja2 MarkupSafe psycopg2 redis SQLAlchemy Werkzeug redis-py dateutil

Then start in this new environment:

    source activate badger4

Start up the main Flask server:

    cd astrobadger/
    python app.py

Start up the database server:

    redis-server

# also need to rebuild the database for this...

in badger4 environment?

copy and paste this in your python to get the redis database ready...

import os
import redis
import collections
import dateutil.parser
from flask import Flask, request, render_template, redirect, jsonify,
url_for, abort
from json import loads, dumps
from datetime import datetime, timedelta

app = Flask(__name__)
REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r_server = redis.StrictRedis.from_url(REDIS_URL)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

## this should initialise your database

```
all_badgers = {}
r_server.set('all_badgers', dumps(all_badgers))
```

## check that it exists with:

```
all_badgers = loads(r_server.get('all_badgers'))
```

Credits/License
===============

Badgers from Weebl and the [badger badger badger badger](https://www.badgerbadgerbadger.com/) animation. There
may be the occasional snake.

Thanks to Jonathan Fey for explaining the Chrome mechanics.

Hack by Lisa and Matt.

