# -*- coding:utf-8 -*-

import hashlib
import json
import dateutil.parser
import time
import requests

from rrd.config import API_ADDR
from rrd import corelib


def graph_info(endpoint_counter):
    if not endpoint_counter:
        return

    h = {"Content-type": "application/json"}
    r = corelib.auth_requests("POST", "%s/graph/history" %
                              API_ADDR, headers=h, data=json.dumps(params))
    if r.status_code != 200:
        raise

    return r.json()


def graph_query(endpoint_counters, cf, start, end):
    params = {
        "start_time": start,
        "end_time": end,
        "consol_fun": cf,
        "counters": endpoint_counters,
    }
    #r = requests.post("%s/graph/history" %QUERY_ADDR, data=json.dumps(params))
    h = {"Content-type": "application/json"}
    r = corelib.auth_requests("POST", "%s/graph/history" %
                              API_ADDR, headers=h, data=json.dumps(params))
    if r.status_code != 200:
        raise Exception("{} : {}".format(r.status_code, r.text))

    return r.json()


def digest_key(endpoint, key):
    s = "%s/%s" % (endpoint.encode("utf8"), key.encode("utf8"))
    return hashlib.md5(s).hexdigest()[:16]


def graph_history(endpoints, counters, cf, start, end):
    # TODO:step
    params = {
        "start_time": start,
        "end_time": end,
        "consol_fun": cf,
        "hostnames": endpoints,
        "counters": counters,
    }
    h = {"Content-type": "application/json"}
    r = corelib.auth_requests("POST", "%s/graph/history" %
                              API_ADDR, headers=h, data=json.dumps(params))
    if r.status_code != 200:
        raise Exception("%s : %s" % (r.status_code, r.text))

    return r.json()


def merge_list(a, b):
    sum = []
    a_len = len(a)
    b_len = len(b)
    l1 = min(a_len, b_len)
    l2 = max(a_len, b_len)

    if a_len < b_len:
        a, b = b, a

    for i in range(0, l1):
        if a[i] is None and b[i] is None:
            sum.append(None)
        elif a[i] is None:
            sum.append(b[i])
        elif b[i] is None:
            sum.append(a[i])
        else:
            sum.append(a[i] + b[i])

    for i in range(l1, l2):
        sum.append(a[i])

    return sum


def CF(cf, values):
    if cf == 'AVERAGE':
        return float(sum(values))/len(values)
    elif cf == 'MAX':
        return max(values)
    elif cf == 'MIN':
        return min(values)
    elif cf == 'LAST':
        return values[-1]
