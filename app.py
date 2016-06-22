import os
import redis
import collections
from flask import Flask, request, render_template, redirect, jsonify, url_for, abort
from json import loads, dumps
from datetime import datetime

app = Flask(__name__)
REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r_server = redis.StrictRedis.from_url(REDIS_URL)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    all_badgers = loads(r_server.get('all_badgers'))
    all_badgers_sorted = collections.OrderedDict(sorted(all_badgers.items()))
    kwargs = {'all_badgers': all_badgers_sorted}
    return render_template('index.html', **kwargs)


@app.route('/<username>/add/', methods=['POST'])
def add(username):
    word_count = request.form['count']
    dt = datetime.now()
    # post_date = dt.isoformat("T").split('T')[0]
    post_date = dt.isoformat("T")

    all_badgers = loads(r_server.get('all_badgers'))
    all_badgers.setdefault(username, {})
    all_badgers[username][post_date] = word_count

    # save to db
    r_server.set('all_badgers', dumps(all_badgers))

    this_badger = all_badgers[username]
    this_badger_sorted = collections.OrderedDict(sorted(this_badger.items(), reverse=True))
    kwargs = {'username': username, 'badger': this_badger_sorted}
    return render_template('user.html', **kwargs)


if __name__ == '__main__':
    app.debug = True
    app.run()
