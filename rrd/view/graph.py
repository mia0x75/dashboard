# -*- coding:utf-8 -*-

import json
import sys

from flask import jsonify, render_template, request, g, make_response, abort
from flask.ext.babel import gettext
from rrd.model.host_group import HostGroup
from rrd.model.host import Host
from rrd import app, config
from rrd import corelib


@app.route('/group/<group_id>/graph')
def graph_list_get(group_id):
    group_id = int(group_id)
    ret = {
        "ok": False,
        "msg": "",
        "endpoints": [],
        "counters": []
    }
    return render_template("graph/counter.html", data=ret)
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        ret['msg'] = 'no such group %s' % group_id
        return render_template("graph/counter.html", data=ret)
    vs, _ = Host.query(1, 10000000, '', '0', group_id)
    names = [v.hostname for v in vs]
    h = {"Content-type": "application/json"}
    r = corelib.auth_requests(
        "GET", config.API_ADDR + "/graph/endpoints?endpoints=%s" % ','.join(names), headers=h)
    if r.status_code != 200:
        abort(400, r.text)
        ret['msg'] = r.text
        return render_template("graph/counter.html", data=ret)
    endpoint_ids = json.loads(r.text)
    # return json.dumps(endpoint_ids)
    if len(endpoint_ids) == 0:
        ret['msg'] = 'No any endpoint selected'
        return render_template("graph/counter.html", data=ret)
    r = corelib.auth_requests("GET", config.API_ADDR + "/graph/endpoint_counter?eid=%s" % ",".join(
        '%s' % e['id'] for e in endpoint_ids), headers=h)
    if r.status_code != 200:
        ret['msg'] = r.text
        return render_template("graph/counter.html", data=ret)
    j = r.json()
    counters_map = {}
    for x in j:
        counters_map[x['counter']] = [x['counter'], x['type'], x['step']]
    sorted_counters = sorted(counters_map.keys())
    sorted_values = [counters_map[x] for x in sorted_counters]
    ret['ok'] = True
    ret['endpoints'] = endpoint_ids
    ret['counters'] = sorted_values
    return render_template("graph/counter.html", data=ret)
