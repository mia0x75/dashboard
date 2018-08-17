# -*- coding:utf-8 -*-

from rrd import app
from flask import jsonify, render_template, request, g
from flask.ext.babel import gettext
from rrd.model.host_group import HostGroup
from rrd.model.variable import Variable
import sys

@app.route('/group/<group_id>/variables')
def variable_list_get(group_id):
    group_id = int(group_id)
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)
    variables = Variable.select_vs(where='grp_id = %s', params=[group_id])
    return render_template('variable/list.html', group=group, variables=variables)

@app.route('/group/<group_id>/variable/creator', methods=['GET'])
def variable_creator_get(group_id):
    group_id = int(group_id)
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)
    return render_template('variable/creator.html', **locals())

@app.route('/group/<group_id>/variable/creator', methods=['POST'])
def variable_creator_post(group_id):
    group_id = int(group_id)
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)
    name = request.form['name'].strip()
    content = request.form['content'].strip()
    note = request.form['note'].strip()
    if Variable.exists('grp_id=%s and name=%s', [group_id, name]):
        return jsonify(msg='%s/%s is already existent' % (group['name'], name))
    last_id = Variable.insert({
        'grp_id': group_id,
        'name': name,
        'content': content,
        'note': note,
        'create_user': g.user.name,
    })
    if last_id > 0:
        return jsonify(msg='')
    else:
        return jsonify(msg='occur error')

@app.route('/variable/edit/<variable_id>', methods=['GET'])
def variable_edit_get(variable_id):
    variable_id = int(variable_id)
    variable = Variable.get(variable_id)
    op = gettext('edit')
    return render_template('variable/edit.html', **locals())

@app.route('/variable/edit/<variable_id>', methods=['POST'])
def variable_edit_post(variable_id):
    variable_id = int(variable_id)
    name = request.form['name'].strip()
    content = request.form['content'].strip()
    note = request.form['note'].strip()
    grp_id = request.form['grp_id'].strip()
    if variable_id:
        # edit
        if Variable.exists('name=%s and content=%s and note=%s and grp_id=%s', [name, content, note, variable_id]):
            return jsonify(msg='%s/%s/%s has already existent' % (name, content, note))
        Variable.update_dict({
            'name': name,
            'content': content,
            'note': note,
        }, 'id=%s', [variable_id])
    else:
        # clone
        if Variable.exists('name=%s and grp_id=%s', [name, grp_id]):
            return jsonify(msg='%s/%s has already existent' % (grp_id, name))
        last_id = Variable.insert({
            'name': name,
            'content': content,
            'note': note,
            'create_user': g.user.name,
            'grp_id': grp_id,
        })
        if last_id <= 0:
            return jsonify(msg='occur error')
    return jsonify(msg='')

@app.route('/variable/clone/<variable_id>', methods=['GET'])
def variable_clone_get(variable_id):
    variable_id = int(variable_id)
    variable = Variable.get(variable_id)
    # for clone
    variable_id = 0
    op = gettext('clone')
    return render_template('variable/edit.html', **locals())

@app.route('/variable/delete/<variable_id>', methods=['GET'])
def variable_delete_get(variable_id):
    variable_id = int(variable_id)
    Variable.delete_one(variable_id)
    return jsonify(msg='')

