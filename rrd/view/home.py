# -*- coding:utf-8 -*-

from rrd import app
from rrd import config
from flask import render_template, request, g
from rrd.model.host_group import HostGroup

from rrd.utils.logger import logging
log = logging.getLogger(__file__)


@app.route('/hostgroup', methods=["GET", ])
def home_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '0')
    me = g.user.name if mine == '1' else None
    vs, total = HostGroup.query(page, limit, query, me)
    log.debug(vs)
    return render_template(
        'group/index.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
            'is_root': g.user.name in config.MAINTAINERS,
        }
    )
