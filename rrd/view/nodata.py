# -*- coding:utf-8 -*-

from rrd import app
from flask import request, g, render_template, jsonify
from rrd.model.nodata import Nodata
from rrd.utils.params import required_chk


@app.route('/nodata')
def nodatas_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 5))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '0')
    me = g.user.name if mine == '1' else None
    vs, total = Nodata.query(page, limit, query, me)
    return render_template(
        'nodata/list.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
        }
    )

@app.route('/nodata/add')
def nodata_add_get():
    o = Nodata.get(int(request.args.get('id', '0').strip()))
    return render_template('nodata/add.html', data={'nodata': o})


@app.route('/nodata/update', methods=['POST'])
def nodata_update_post():
    nodata_id = request.form['nodata_id'].strip()
    name = request.form['name'].strip()
    obj = request.form['obj'].strip()
    obj_type = request.form['obj_type'].strip()
    metric = request.form['metric'].strip()
    tags = request.form['tags'].strip()
    dstype = request.form['dstype'].strip()
    step = request.form['step'].strip()
    mock = request.form['mock'].strip()

    msg = required_chk({
        'name': name,
        'endpoint': obj,
        'endpoint_type': obj_type,
        'metric': metric,
        'type': dstype,
        'step': step,
        'mock_value': mock,
    })

    if msg:
        return jsonify(msg=msg)

    return jsonify(msg=Nodata.save_or_update(
        nodata_id,
        name,
        obj,
        obj_type,
        metric,
        tags,
        dstype,
        step,
        mock,
        g.user.name,
    ))

@app.route('/nodata/delete/<nodata_id>')
def nodata_delete_get(nodata_id):
    nodata_id = int(nodata_id)
    Nodata.delete_one(nodata_id)
    return jsonify(msg='')
