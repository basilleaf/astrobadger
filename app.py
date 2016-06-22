import os
import redis
import collections
import dateutil.parser
from flask import Flask, request, render_template, redirect, jsonify, url_for, abort
from json import loads, dumps
from datetime import datetime, timedelta

app = Flask(__name__)
REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r_server = redis.StrictRedis.from_url(REDIS_URL)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/admin/')
def admin():
    """ lists all users """
    all_badgers = loads(r_server.get('all_badgers'))
    all_badgers_sorted = collections.OrderedDict(sorted(all_badgers.items(), reverse=True))
    kwargs = {'badgers': all_badgers_sorted }
    return render_template('index.html', **kwargs)


@app.route('/<username>/')
def user(username):
    """ displays a single user """
    all_badgers = loads(r_server.get('all_badgers'))
    this_badger = all_badgers[username]
    this_badger_sorted = collections.OrderedDict(sorted(this_badger.items(), reverse=True))
    days = days_in_a_row(this_badger)
    kwargs = {'badgers': { username: this_badger_sorted }, 'days': days }
    return render_template('index.html', **kwargs)


@app.route('/<username>/add/', methods=['POST'])
def add(username):
    """ add a new word count for a user """
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

    return redirect(url_for('user', username=username))
    # return render_template('user.html', **kwargs)

def days_in_a_row(dich):
    # this_badger is like: { date: number, date: number }
    # given a dictionary of days,

    dt = datetime.now()
    post_date = dt.isoformat("T")

    # find midnight tonight
    midnight_tonight = (dt + timedelta(days=1)).replace(microsecond=0,second=0,minute=0, hour=0)

    # make a list output
    ddays = []
    for key in dich:
        deltat = midnight_tonight - dateutil.parser.parse(key)
        dd = deltat.days
        ddays.append(dd)

    t = sorted(ddays)

    totaldelta = []
    for t1,t2 in zip(t[0:-1], t[1:]):
        totaldelta.append(t2-t1)

    # if t[0] is not 0, then a day has been missed
    if(t[0] > 0):
        return 0

    # now look for the first occurence of >1 in the totaldelta series
    nrun = 0
    while (t[nrun] < 2):
        nrun = nrun + 1

    ntot = nrun + 1
    return ntot



if __name__ == '__main__':
    app.debug = True
    app.run()
