# -*- coding:utf-8 -*-

from .bean import Bean


class Metric(Bean):
    _tbl = 'metric'
    _id = 'id'
    _cols = 'id, name, update_at'

    def __init__(self, _id, name, update_at):
        self.id = _id
        self.name = name
        self.update_at = update_at

    @classmethod
    def query(cls, page, limit, query):
        where = ''
        params = []

        if query:
            where += ' and ' if where else ''
            where += 'name like %s'
            params.append('%' + query + '%')

        vs = cls.select_vs(where=where, params=params, page=page, limit=limit, order='id')
        total = cls.total(where, params)
        return vs, total
