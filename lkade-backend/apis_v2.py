import shutil, re, json, random, requests
import sys, os, time
import urllib.parse
import bottle, platform
import traceback
from bottle import route, template, request, response, static_file
from pymongo import MongoClient
from datetime import datetime
import logging
import logging.handlers
from bson.objectid import ObjectId
import ljqpy


DB = 'local'
if DB == 'local':
	client = MongoClient('10.141.208.26', 27017)
	client.admin.authenticate('gdmdbuser', '6QEUI8dhnq', mechanism='SCRAM-SHA-1')

config = {
	'entity_name_field': 'name',
}

db = client.get_database('bqb')
user_table = db.get_collection('user')
entity_table = db.get_collection('entity')
relation_table = db.get_collection('triple_rel')
attribute_table = db.get_collection('triple_attr')
ment2ent_table = db.get_collection('ment2ent')


app = bottle.app()

from utils import *


def GetEntitybyID(sid):
	try: sid = ObjectId(sid)
	except: return None
	return entity_table.find_one({'_id': ObjectId(sid)})

def GetEntityName(ent):
	if ent is None: return ''
	return ent[config['entity_name_field']]

def TestSpecialChars(sr):
	if re.search(r'[<>\'"\s]', sr):
		return True
	else:
		return False

def SplitId(name):
	ename = ''
	eid = ljqpy.RM("<id:([0-9a-f]+)>", name)
	if eid == "": return name, name
	ename = re.sub("<id:([0-9a-f]+)>$", '', name)
	return ename, eid

@app.route('/api/triples', method=['GET', 'POST'])
def triples():
	if not check_authority(): return not_authority_ret
	ret = {'status': 'error', 'ret': []}
	name = request.params.entity
	no_expand_o = request.params.no_expand_o

	name, eid = SplitId(name)

	if eid != name: entity = GetEntitybyID(eid)
	else: entity = entity_table.find_one({'name': name})
	if entity is None:
		ret['status'] = 'ok'
	else:
		ret['status'] = 'ok'
		eid = str(entity['_id'])
		ename = GetEntityName(entity)

		# 以查询节点为s的关系
		for triple in relation_table.find({'sid': eid}):
			o = GetEntitybyID(triple['oid'])
			if o is None:
				print('entity not found: {}'.format(triple['oid']))
				continue
			ret['ret'].append({
				'id': str(triple['_id']),
				's': eid,
				'sname': ename,
				'p': triple['p'],
				'oid': str(o['_id']),
				'oname': GetEntityName(o)
			})
		if not no_expand_o:
			# 以查询节点为o的关系
			for triple in relation_table.find({'oid': eid}):
				s = GetEntitybyID(triple['sid'])
				if s is None:
					print('entity not found: {}'.format(triple['sid']))
					continue
				ret['ret'].append({
					'id': str(triple['_id']),
					's': str(s['_id']),
					'sname': GetEntityName(s),
					'p': triple['p'],
					'oid': eid,
					'oname': ename
				})
		# 以查询节点为s的属性
		for triple in attribute_table.find({'sid': eid}):
			ret['ret'].append({
				'id': str(triple['_id']),
				's': eid,
				'sname': ename,
				'p': triple['p'],
				'oid': '',
				'oname': triple['o']
			})
	return json.dumps(ret, ensure_ascii = False)

@app.route('/api/ment2ent', method = ['GET', 'POST'])
def ment2ent():
	if not check_authority(): return not_authority_ret
	ret = {'status': 'error', 'ret': []}
	query = request.params.q
	no_other_m = request.params.no_other_m

	query, eid = SplitId(query)

	rets = []

	if eid != query: entity = GetEntitybyID(eid)
	else: entity = entity_table.find_one({'name': query})

	if entity is not None:
		rets.append({
			'm': query,
			'eid': str(entity['_id']),
			'isent': True
		})
		if not no_other_m:
			rets.extend(list(ment2ent_table.find({'eid': str(entity['_id'])})))

	rets.extend(list(ment2ent_table.find({'m': query})))

	ret['ret'] = [{
		'id': str(x.get('_id', '')),
		'mention': x['m'],
		'eid': x['eid'],
		'ename': GetEntityName(GetEntitybyID(x['eid'])),
		'isent': x.get('isent', False)
	} for x in rets]
	ret['status'] = 'ok'
	return json.dumps(ret, ensure_ascii = False)


def precheck_new_entity(name):
	if name == '': return '名称不能为空'
	if TestSpecialChars(name): return '名称不能包含特殊符号或空白符'
	ditem = {config['entity_name_field']: name}
	exists = entity_table.find_one(ditem)
	if exists: return '实体已经存在'

@app.route('/api/new_entity', method = ['GET', 'POST'])
def newentity():
	if not check_authority(write=True): return not_authority_ret
	name = request.params.name
	precheck = request.params.precheck
	msg = precheck_new_entity(name)
	ret = {'status': 'error' if msg else 'ok', 'msg': msg}
	if precheck: return json.dumps(ret, ensure_ascii=False)
	if not msg:
		ditem = {config['entity_name_field']: name}
		rr = entity_table.insert_one(ditem)
		ret['eid'] = str(rr.inserted_id)
	return json.dumps(ret, ensure_ascii = False)


def precheck_new_triple(sid, p, oid, oname):
	sname, sid = SplitId(sid)
	if sid == '' or GetEntitybyID(sid) is None: return '实体不存在'
	if p == '': return '属性不能为空'
	if TestSpecialChars(p): return '属性不能包含特殊符号或空白符'
	if oname == '': return '值不能为空'
	# oid非空表示关系，否则表示属性
	if oid != '':
		oname, oid = SplitId(oid)
		if relation_table.find_one({'sid': sid, 'p': p, 'oid': oid}) is not None:
			return '存在重复关系'
		o = GetEntitybyID(oid)
		if o is None: return 'Object实体不存在'
		if oname != GetEntityName(o): return '实体名称不匹配'
	else:
		if TestSpecialChars(oname): return '值不能包含特殊符号或空白符'
		if attribute_table.find_one({'sid': sid, 'p': p, 'o': oname}) is not None:
			return '存在重复属性'

@app.route('/api/new_triple', method = ['GET', 'POST'])
def new_triple():
	if not check_authority(): return not_authority_ret
	sid = request.params.sid
	p = request.params.p
	oid = request.params.oid
	oname = request.params.oname
	precheck = request.params.precheck
	msg = precheck_new_triple(sid, p, oid, oname)
	ret = {'status': 'error' if msg else 'ok', 'msg': msg}
	if precheck: return json.dumps(ret, ensure_ascii=False)
	sname, sid = SplitId(sid)
	if not msg:
		# oid非空表示关系，否则表示属性
		if oid != '':
			oname, oid = SplitId(oid)
			rr = relation_table.insert_one({'sid': sid, 'p': p, 'oid': oid})
		else:
			rr = attribute_table.insert_one({'sid': sid, 'p': p, 'o': oname})
	ret['eid'] = str(rr.inserted_id)
	return json.dumps(ret, ensure_ascii=False)


def precheck_new_ment2ent(eid, mention):
	if mention == '': return '别名不能为空'
	if TestSpecialChars(mention): return '别名不能包含特殊符号或空白符'
	ent = GetEntitybyID(eid)
	if ent is None: return '实体不存在'
	if GetEntityName(ent) == mention: return '别名不能和实体名相同'
	ditem = {'m': mention, 'eid': eid}
	if ment2ent_table.find_one(ditem) is not None: return '库中已存在此关系'

@app.route('/api/new_ment2ent', method = ['GET', 'POST'])
def new_ment2ent():
	if not check_authority(write=True): return not_authority_ret
	eid = request.params.eid
	mention = request.params.mention
	precheck = request.params.precheck
	msg = precheck_new_ment2ent(eid, mention)
	ret = {'status': 'error' if msg else 'ok', 'msg': msg}
	if precheck: return json.dumps(ret, ensure_ascii=False)
	if not msg:
		ditem = {'m': mention, 'eid': eid}
		ment2ent_table.insert_one(ditem)
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_triple', method = ['GET', 'POST'])
def remove_triple():
	if not check_authority(write=True): return not_authority_ret
	tid = request.params.id
	oid = request.params.oid
	if oid != '': rr = relation_table.delete_one({'_id': ObjectId(tid)})
	else: rr = attribute_table.delete_one({'_id': ObjectId(tid)})
	status = 'ok' if rr.acknowledged else 'error'
	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_ment2ent', method = ['GET', 'POST'])
def remove_ment2ent():
	if not check_authority(write=True): return not_authority_ret
	tid = request.params.id
	del_result = ment2ent_table.delete_one({'_id': ObjectId(tid)})
	status = 'ok' if del_result.acknowledged else 'error'
	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii = False)

def RemoveEntity(eid):
	ment2ent_table.delete_many({'eid': eid})
	relation_table.delete_many({'sid': eid})
	relation_table.delete_many({'oid': eid})
	attribute_table.delete_many({'sid': eid})
	return entity_table.delete_one({'_id': ObjectId(eid)})

def EntityRelatedInfos(idx):
	tris = []
	for x in ment2ent_table.find({'eid': idx}):
		tris.append({'s': GetEntityName(GetEntitybyID(x['eid'])), 'p': '别名', 'o': x['m']})
	for x in relation_table.find({'sid': idx}):
		tris.append({'s': GetEntityName(GetEntitybyID(x['sid'])), 'p': x['p'], 'o': GetEntityName(GetEntitybyID(x['oid']))})
	for x in relation_table.find({'oid': idx}):
		tris.append({'s': GetEntityName(GetEntitybyID(x['sid'])), 'p': x['p'], 'o': GetEntityName(GetEntitybyID(x['oid']))})
	for x in attribute_table.find({'sid': idx}):
		tris.append({'s': GetEntityName(GetEntitybyID(x['sid'])), 'p': x['p'], 'o': x['o']})
	return tris

@app.route('/api/info_remove_entity', method = ['GET', 'POST'])
def info_remove_entity():
	eid = request.params.id
	ename, eid = SplitId(eid)
	ret = {'status':'ok','ret': EntityRelatedInfos(eid)}
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_entity', method = ['GET', 'POST'])
def remove_entity():
	if not check_authority(write=True): return not_authority_ret
	eid = request.params.id
	del_result = RemoveEntity(eid)
	status = 'ok' if del_result.acknowledged else 'error'
	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii=False)


def entity2dict(entity):
	#'timestamp': entity['timestamp'].timestamp(), 
	return {'idx': str(entity['_id']), 'attr': [], 
		 'name': GetEntityName(entity)}

def o_is_entity(o):
	return re.match(r'<a href="(.*?)">(.*?)</a>', o) is not None

def triple2dict(triple):
	ret = {'idx': str(triple['_id']), 
		's': triple['sid'], 'p': triple['p'], 'o': triple.get('o', triple.get('oid', ''))}
	return ret


@app.route('/api/graph/query_entity', method=['GET', 'POST'])
def query_entity():
	if not check_authority(): return not_authority_ret
	ret = {
		'status': 'fail',
		'nodes': [],
		'links': [],
		'error': 'connection failed'
	}
	
	no_expand = request.params.no_expand
	no_expand_o = request.params.no_expand_o
	eid = request.params.idx
	if eid == '': return json.dumps(ret, ensure_ascii=False)

	name, eid = SplitId(eid)

	entity = GetEntitybyID(eid)
	if entity is None:
		ret['status'] = 'fail'
		ret['error'] = 'entity not found'
	else:
		ret['status'] = 'success'
		ret['error'] = ''

		d = {}
		entid = str(entity['_id'])
		d[entid] = len(d)
		ret['nodes'].append(entity2dict(entity))
		if not no_expand:
			for triple in relation_table.find({'sid': entid}):
				oid = triple['oid']
				oent = GetEntitybyID(oid)
				if oent is None:
					ret['status'] = 'fail'
					ret['error'] = 'oentity not found'
				else:
					if oid not in d:
						d[oid] = len(d)
						ret['nodes'].append(entity2dict(oent))
					ret['links'].append({
						'source': d[entid],
						'target': d[oid],
						'triple': triple2dict(triple)
					})
				if not no_expand_o:
					for triple in relation_table.find({'oid': entid}):
						sid = triple['sid']
						sent = GetEntitybyID(sid)
						if sent is None:
							ret['status'] = 'fail'
							ret['error'] = 'sentity not found'
						else:
							if sid not in d:
								d[sid] = len(d)
								ret['nodes'].append(entity2dict(sent))
							ret['links'].append({
								'source': d[sid],
								'target': d[entid],
								'triple': triple2dict(triple)
							})

	for index in range(len(ret['nodes'])):
		node = ret['nodes'][index]
		for triple in attribute_table.find({'sid': node['idx']}):
			ret['nodes'][index]['attr'].append(triple2dict(triple))
	return json.dumps(ret, ensure_ascii=False)


@app.route('/api/graph/update_triple_p', method=['GET', 'POST'])
def update_triple_p():
    ret = {
        'status': 'fail',
        'msg': 'connection failed'
    }
    _id = request.params.idx
    new_p = request.params.new_p
    triple = relation_table.find_one({'_id': ObjectId(_id)})
    if triple is None:
        ret['status'] = 'fail'
        ret['msg'] = '关系不存在：{}'.format(_id)
    else:
        s = triple['sid']
        o = triple['oid']
        if relation_table.find_one({'sid': s, 'p': new_p, 'oid': o}) is not None:
            ret['status'] = 'fail'
            ret['error'] = '关系重复: {}-{}-{}'.format(s, new_p, o)
        else:
            r = relation_table.update_one({'_id': ObjectId(_id)}, {'$set': {'p': new_p, 'timestamp': datetime.now()}})
            if not r.acknowledged:
                ret['status'] = 'fail'
                ret['msg'] = 'update failed'
            else:
                ret['status'] = 'success'
                ret['msg'] = '修改关系成功'
    return json.dumps(ret, ensure_ascii=False)

sapp = DefineCommonFuncs(app, user_table)

#from gevent import monkey; monkey.patch_all()
#bottle.run(sapp, host='0.0.0.0', port=26551, server='gevent')

bottle.run(sapp, host='0.0.0.0', port=26551, debug=True, reloader=True)
