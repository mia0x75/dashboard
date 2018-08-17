# -*- coding:utf-8 -*-

from flask import jsonify, render_template, request, g, abort
from rrd import app
from rrd.model.alarm import Event, EventCase
import json


@app.route("/alarm-dash/case")
def alarm_dash_case_get():
    event_cases = []
    limit = int(request.args.get("limit") or 10)
    page = int(request.args.get("p") or 1)
    endpoint_q = request.args.get("endpoint_q") or ""
    metric_q = request.args.get("metric_q") or ""
    status = request.args.get("status") or ""
    from_date = request.args.get("from_date") or ""
    to_date = request.args.get("to_date") or ""

    if status:
        limit = int(200)
    # limit should be under control
    if limit > 200:
        limit = int(200)

    cases, total = EventCase.query(
        page, limit, endpoint_q, metric_q, status, from_date, to_date)
    if status == 'PROBLEM':
        return render_template("alarm/case_problem.html", **locals())
    else:
        return render_template("alarm/case.html", **locals())


@app.route("/alarm-dash/case/event")
def alarm_dash_event_get():
    limit = int(request.args.get("limit") or 10)
    page = int(request.args.get("p") or 1)

    case_id = request.args.get("case_id")
    if not case_id:
        abort(400, "no case id")

    _cases = EventCase.select_vs(where='id=%s', params=[case_id], limit=1)
    if len(_cases) == 0:
        abort(400, "no such case where id=%s" % case_id)
    case = _cases[0]

    case_events, total = Event.query(
        event_caseId=case_id, page=page, limit=limit)
    return render_template("alarm/case_events.html", **locals())


@app.route("/alarm-dash/case/delete", methods=['POST'])
def alarm_dash_case_delete():
    ret = {
        "msg": "",
    }
    ids = request.form.get("ids") or ""
    ids = ids.split(",") or []
    if not ids:
        ret['msg'] = "no case ids"
        return json.dumps(ret)

    holders = []
    for x in ids:
        holders.append("%s")
    placeholder = ','.join(holders)

    where = 'id in (' + placeholder + ')'
    params = ids
    EventCase.delete(where=where, params=params)
    for x in ids:
        Event.delete(where='event_caseId=%s', params=[x])

    return json.dumps(ret)


@app.route("/alarm-dash/case/event/delete", methods=['POST'])
def alarm_dash_case_event_delete():
    ret = {
        "msg": "",
    }
    ids = request.form.get("ids") or ""
    ids = ids.split(",") or []
    if not ids:
        ret['msg'] = "no case ids"
        return json.dumps(ret)

    holders = ["%s" for x in ids]
    placeholder = ','.join(holders)

    where = 'id in (' + placeholder + ')'
    params = ids
    Event.delete(where=where, params=params)

    return json.dumps(ret)
