# -*- coding:utf-8 -*-

from .bean import Bean

class Tag(Bean):
    _tbl = 'tags'
    _id = 'id'
    _cols = 'id, name'
    def __init__(self, _id, name):
        self.id = _id
        self.name = name
