# -*- coding:utf-8 -*-

import datetime
import time
from flask import g, session, request, redirect

from rrd import app, config
from rrd.view.utils import get_usertoken_from_session, get_current_user_profile

@app.template_filter('fmt_time')
def fmt_time_filter(value, pattern="%Y-%m-%d %H:%M"):
    if not value:
        return ''
    return datetime.datetime.fromtimestamp(value).strftime(pattern)


@app.template_filter('time_duration')
def time_duration(v):
    d = time.time() - time.mktime(v.timetuple())

    if d <= 60:
        return "just now"
    if d <= 120:
        return "1 minute ago"
    if d <= 3600:
        return "%d minutes ago" % (d/60)
    if d <= 7200:
        return "1 hour ago"
    if d <= 3600*24:
        return "%d hours ago" % (d/3600)
    if d <= 3600*24*2:
        return "1 day ago"

    return "%d days ago" % (d/3600/24)


@app.teardown_request
def app_teardown(exception):
    from rrd.store import db, alarm_db
    db.commit()
    alarm_db.commit()


@app.before_request
def app_before():
    g.user_token = get_usertoken_from_session(session)
    g.user = get_current_user_profile(g.user_token)
    g.locale = request.accept_languages.best_match(config.LANGUAGES.keys())

    path = request.path
    if not g.user and not path.startswith("/auth/login") and \
            not path.startswith("/static/") and \
            not path.startswith("/links/") and \
            not path.startswith("/auth/register"):
        return redirect("/auth/login")

    if path.startswith("/screen"):
        g.nav_menu = "nav_screen"
    elif path.startswith("/hostgroup") or path.startswith("/group"):
        g.nav_menu = "p_hostgroup"
    elif path.startswith("/template"):
        g.nav_menu = "p_template"
    elif path.startswith("/expression"):
        g.nav_menu = "p_expression"
    elif path.startswith("/nodata"):
        g.nav_menu = "p_nodata"
    elif path.startswith("/alarm-dash"):
        g.nav_menu = "p_alarm-dash"
    elif path.startswith("/metric"):
        g.nav_menu = "p_metric"
    elif path == "/":
        g.nav_menu = "p_dashboard"
    else:
        g.nav_menu = ""
