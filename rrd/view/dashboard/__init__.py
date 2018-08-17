# -*- coding:utf-8 -*-

import time
from flask import request, g, session, abort, render_template

from rrd import app
from rrd.consts import GRAPH_TYPE_HOST


@app.before_request
def dashboard_before():
    if request.method == "GET":
        now = int(time.time())

        # 是否显示顶部图表导航
        g.nav_header = request.args.get("nav_header") or "on"
        g.cols = request.args.get("cols") or "2"
        try:
            g.cols = int(g.cols)
        except:
            g.cols = 2
        if g.cols <= 0:
            g.cols = 2
        if g.cols >= 6:
            g.cols = 6

        g.legend = request.args.get("legend") or "off"
        g.graph_type = request.args.get("graph_type") or GRAPH_TYPE_HOST
        g.sum = request.args.get("sum") or "off"  # 是否求和
        g.sumonly = request.args.get("sumonly") or "off"  # 是否只显示求和

        # MAX, MIN, AVGRAGE, LAST
        g.cf = (request.args.get("cf") or "AVERAGE").upper()

        g.start = int(request.args.get("start") or -3600)
        if g.start < 0:
            g.start = now + g.start

        g.end = int(request.args.get("end") or 0)
        if g.end <= 0:
            g.end = now + g.end
        g.end = g.end - 60

        g.id = request.args.get("id") or ""

        g.limit = int(request.args.get("limit") or 0)
        g.page = int(request.args.get("page") or 0)
        g.comp_date = int(request.args.get("comp_date") or 0)
