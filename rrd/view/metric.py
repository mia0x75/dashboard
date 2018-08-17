# -*- coding:utf-8 -*-

from rrd import app
from flask import render_template, request, g, jsonify
from rrd.model.metric import Metric
from rrd.utils.logger import logging
log = logging.getLogger(__file__)

@app.route('/metric', methods=["GET", ])
def metric_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 50))
    query = request.args.get('q', '').strip()
    vs, total = Metric.query(page, limit, query)
    return render_template(
        'metric/index.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page
        }
    )

@app.route('/metric/delete/<metric_id>')
def metric_delete_get(metric_id):
    metric_id = int(metric_id)
    t = Metric.get(metric_id)
    if not t:
        return jsonify(msg='no such metric')
    Metric.delete_one(metric_id)
    return jsonify(msg='')

