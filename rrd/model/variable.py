# -*- coding:utf-8 -*-

from .bean import Bean

class Variable(Bean):
    _tbl = 'variable'
    _id = 'id'
    _cols = 'id, grp_id, name, content, note, create_user'

    def __init__(self, _id, grp_id, name, content, note, create_user):
        self.id = _id
        self.grp_id = grp_id
        self.name = name
        self.content = content
        self.note = note
        self.create_user = create_user
