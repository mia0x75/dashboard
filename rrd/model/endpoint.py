# -*- coding:utf-8 -*-

import json

from rrd.config import API_ADDR
from rrd import corelib


class Endpoint(object):
    def __init__(self, id, endpoint, ts):
        self.id = str(id)
        self.endpoint = endpoint
        self.ts = ts

    def __repr__(self):
        return "<Endpoint id=%s, endpoint=%s>" % (self.id, self.id)
    __str__ = __repr__

    @classmethod
    def search(cls, qs, start=0, limit=100, deadline=0):
        args = [deadline, ]
        for q in qs:
            args.append("%" + q + "%")
        args += [start, limit]

        sql = '''select id, endpoint, ts from endpoint where ts > %s '''
        for q in qs:
            sql += ''' and endpoint like %s'''
        sql += ''' limit %s,%s'''
        # TODO: 改成api调用，增加falcon-api功能
        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def search_in_ids(cls, qs, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)

        args = ids + [deadline, ]
        for q in qs:
            args.append("%" + q + "%")

        sql = '''select id, endpoint, ts from endpoint where id in (''' + \
            placeholder + ''') and ts > %s '''
        for q in qs:
            sql += ''' and endpoint like %s'''
        # TODO: 改成api调用，增加falcon-api功能
        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets_by_endpoint(cls, endpoints, deadline=0):
        if not endpoints:
            return []

        h = {"Content-type": "application/json"}
        qs = "deadline=%d" % deadline
        for x in endpoints:
            qs += "&endpoints=%s" % x
        r = corelib.auth_requests(
            "GET", API_ADDR + "/graph/endpointobj?%s" % qs, headers=h)
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json() or []
        return [cls(*[x["id"], x["endpoint"], x["ts"]]) for x in j]

    @classmethod
    def gets(cls, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)
        args = ids + [deadline, ]
        # TODO: 改成api调用，增加falcon-api功能
        cursor = db_conn.execute(
            '''select id, endpoint, ts from endpoint where id in (''' + placeholder + ''') and ts > %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]


class EndpointCounterA(object):
    def __init__(self, endpoint_id, counter, step, type_):
        self.endpoint_id = str(endpoint_id)
        self.counter = counter
        self.step = step
        self.type_ = type_

    def __repr__(self):
        return "<EndpointCounter endpoint_id=%s, counter=%s>" % (self.endpoint_id, self.counter)
    __str__ = __repr__

    @classmethod
    def search_in_endpoint_ids(cls, qs, endpoint_ids, limit=100):
        if not endpoint_ids:
            return []

        eid_str = ",".join(endpoint_ids)
        r = corelib.auth_requests(
            "GET", API_ADDR + "/graph/endpoint_counter?eid=%s&metricQuery=%s&limit=%d" % (eid_str, " ".join(qs), limit))
        if r.status_code != 200:
            raise Exception(r.text)
        j = r.json() or []

        return [cls(*[x["endpoint_id"], x["counter"], x["step"], x["type"]]) for x in j]
