# -*- coding:utf-8 -*-

from .bean import Bean


class PluginDir(Bean):
    _tbl = 'plugin_dir'
    _id = 'id'
    _cols = 'id, grp_id, dir, create_user'

    def __init__(self, _id, grp_id, plugin_dir, create_user):
        self.id = _id
        self.grp_id = grp_id
        self.dir = plugin_dir
        self.create_user = create_user

