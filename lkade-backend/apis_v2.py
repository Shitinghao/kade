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


DB = 'local'
if DB == 'local':
	# client = MongoClient('10.141.208.26', 27017)
	# client.admin.authenticate('bqb', '6QEUI8dhnq', mechanism='SCRAM-SHA-1')
	client = MongoClient()

config = {
	'entity_name_field': 'name',
}


db = client.bqb

app = bottle.app()

@app.hook('after_request')
def enable_cors(): response.headers['Access-Control-Allow-Origin'] = '*'

msg_badapikey = '{"status":"fail", "reason": "bad apikey"}'
msg_toofreq = '{"status":"fail", "reason": "too many requests"}'
msg_callus = '{"status":"fail", "reason": "您目前的APIkey无权限访问高级内容，请联系我们升级"}'


def GetEntitybyID(sid):
	return db.entity.find_one({'_id': ObjectId(sid)})

def GetEntityName(ent):
	if ent is None: return ''
	return ent[config['entity_name_field']]

def TestSpecialChars(sr):
	if re.search(r'[<>\'"\s]', sr):
		return True
	else:
		return False

@app.route('/api/triples', method=['GET', 'POST'])
def triples():
	ret = {'status': 'error', 'ret': []}
	name = request.params.entity
	entity = db.entity.find_one({'name': name})
	if entity is None:
		ret['status'] = 'entity not found: {}'.format(name)
	else:
		ret['status'] = 'ok'
		# 以查询节点为s的关系
		for triple in db.triple_rel.find({'sid': str(entity['_id'])}):
			o = GetEntitybyID(triple['oid'])
			if o is None:
				print('entity not found: {}'.format(triple['oid']))
				continue
			ret['ret'].append({
				'id': str(triple['_id']),
				's': GetEntityName(entity),
				'p': triple['p'],
				'oid': str(o['_id']),
				'oname': GetEntityName(o)
			})
		# 以查询节点为o的关系
		# for triple in db.triple_rel.find({'oid': str(entity['_id'])}):
		# 	s = GetEntitybyID(triple['sid'])
		# 	if s is None:
		# 		print('entity not found: {}'.format(triple['sid']))
		# 		continue
		# 	ret['ret'].append({
		# 		'id': str(triple['_id']),
		# 		's': GetEntityName(s),
		# 		'p': triple['p'],
		# 		'oid': str(entity['_id']),
		# 		'oname': GetEntityName(entity)
		# 	})
		# 以查询节点为s的属性
		for triple in db.triple_attr.find({'sid': str(entity['_id'])}):
			ret['ret'].append({
				'id': str(triple['_id']),
				's': GetEntityName(entity),
				'p': triple['p'],
				'oid': '',
				'oname': triple['o']
			})
	return json.dumps(ret, ensure_ascii = False)

@app.route('/api/ment2ent', method = ['GET', 'POST'])
def ment2ent():
	ret = {'status': 'error', 'ret': []}
	query = request.params.q
	no_other_m = request.params.no_other_m

	temp = []
	entity = db.entity.find_one({'name': query})
	if entity is not None:
		temp.append({
			'm': query,
			'eid': str(entity['_id']),
			'isent': True
		})
		if not no_other_m:
			temp.extend(list(db.ment2ent.find({'eid': str(entity['_id'])})))

	temp.extend(list(db.ment2ent.find({'m': query})))

	ret['ret'] = [{
		'id': str(t.get('_id', '')),
		'mention': t['m'],
		'eid': t['eid'],
		'ename': GetEntityName(GetEntitybyID(t['eid'])),
		'isent': t.get('isent', False)
	} for t in temp]
	return json.dumps(ret, ensure_ascii = False)


def precheck_new_entity(name):
	if name == '': return '名称不能为空'
	if TestSpecialChars(name): return '名称不能包含特殊符号或空白符'
	ditem = {config['entity_name_field']: name}
	exists = db.entity.find_one(ditem)
	if exists: return '实体已经存在'

@app.route('/api/new_entity', method = ['GET', 'POST'])
def newentity():
	name = request.params.name
	precheck = request.params.precheck
	msg = precheck_new_entity(name)
	ret = {'status': 'error' if msg else 'ok', 'msg': msg}
	if precheck: return json.dumps(ret, ensure_ascii=False)
	if not msg:
		ditem = {config['entity_name_field']: name}
		db.entity.insert_one(ditem)
	return json.dumps(ret, ensure_ascii = False)


def precheck_new_triple(sid, p, oid, oname):
	print(sid, p, oid, oname)
	if GetEntitybyID(sid) is None: return '实体不存在'
	if p == '': return '属性不能为空'
	if TestSpecialChars(p): return '属性不能包含特殊符号或空白符'
	if oname == '': return '值不能为空'
	if TestSpecialChars(oname): return '值不能包含特殊符号或空白符'
	# oid非空表示关系，否则表示属性
	if oid != '':
		if db.triple_rel.find_one({'sid': sid, 'p': p, 'oid': oid}) is not None:
			return '存在重复关系'
		o = GetEntitybyID(oid)
		if o is None:
			return 'Object实体不存在'
		if oname != GetEntityName(o):
			return '实体名称不匹配'
	elif db.triple_attr.find_one({'sid': sid, 'p': p, 'o': oname}) is not None:
			return '存在重复属性'

@app.route('/api/new_triple', method = ['GET', 'POST'])
def new_triple():
	sid = request.params.sid
	p = request.params.p
	oid = request.params.oid
	oname = request.params.oname
	precheck = request.params.precheck
	msg = precheck_new_triple(sid, p, oid, oname)
	ret = {'status': 'error' if msg else 'ok', 'msg': msg}
	if precheck: return json.dumps(ret, ensure_ascii=False)
	if not msg:
		# oid非空表示关系，否则表示属性
		if oid != '':
			db.triple_rel.insert_one({'sid': sid, 'p': p, 'oid': oid})
		else:
			db.triple_attr.insert_one({'sid': sid, 'p': p, 'o': oname})
	return json.dumps(ret, ensure_ascii=False)


def precheck_new_ment2ent(eid, mention):
	if mention == '': return '别名不能为空'
	if TestSpecialChars(mention): return '别名不能包含特殊符号或空白符'
	if GetEntitybyID(eid) is None: return '实体不存在'
	ditem = {'m': mention, 'eid': eid}
	if db.ment2ent.find_one(ditem) is not None: return '库中已存在此关系'

@app.route('/api/new_ment2ent', method = ['GET', 'POST'])
def new_ment2ent():
	eid = request.params.eid
	mention = request.params.mention
	precheck = request.params.precheck
	msg = precheck_new_ment2ent(eid, mention)
	ret = {'status': 'error' if msg else 'ok', 'msg': msg}
	if precheck: return json.dumps(ret, ensure_ascii=False)
	if not msg:
		ditem = {'m': mention, 'eid': eid}
		db.ment2ent.insert_one(ditem)
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_triple', method = ['GET', 'POST'])
def remove_triple():
	tid = request.params.id
	r1 = db.triple_rel.delete_one({'_id': ObjectId(tid)})
	r2 = db.triple_attr.delete_one({'_id': ObjectId(tid)})
	status = 'ok' if (r1.acknowledged and r2.acknowledged) else 'error'

	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_ment2ent', method = ['GET', 'POST'])
def remove_ment2ent():
	tid = request.params.id
	del_result = db.ment2ent.delete_one({'_id': ObjectId(tid)})
	status = 'ok' if del_result.acknowledged else 'error'
	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii = False)

def RemoveEntity(eid):
	db.ment2ent.delete_many({'eid': eid})
	db.triple_rel.delete_many({'sid': eid})
	db.triple_rel.delete_many({'oid': eid})
	db.triple_attr.delete_many({'sid': eid})
	return db.entity.delete_one({'_id': ObjectId(eid)})

def EntityRelatedInfos(idx):
	tris = []
	for x in db.ment2ent.find({'eid': idx}):
		tris.append({'s': GetEntityName(GetEntitybyID(x['eid'])), 'p': '别名', 'o': x['m']})
	for x in db.triple_rel.find({'sid': idx}):
		tris.append({'s': GetEntityName(GetEntitybyID(x['sid'])), 'p': x['p'], 'o': GetEntityName(GetEntitybyID(x['oid']))})
	for x in db.triple_rel.find({'oid': idx}):
		tris.append({'s': GetEntityName(GetEntitybyID(x['sid'])), 'p': x['p'], 'o': GetEntityName(GetEntitybyID(x['oid']))})
	for x in db.triple_attr.find({'sid': idx}):
		tris.append({'s': GetEntityName(GetEntitybyID(x['sid'])), 'p': x['p'], 'o': x['o']})
	return tris

@app.route('/api/info_remove_entity', method = ['GET', 'POST'])
def info_remove_entity():
	eid = request.params.id
	ret = {'status':'ok','ret': EntityRelatedInfos(eid)}
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_entity', method = ['GET', 'POST'])
def remove_entity():
	eid = request.params.id
	del_result = RemoveEntity(eid)
	status = 'ok' if del_result.acknowledged else 'error'
	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii=False)


@app.route('/', method='GET')
def index():
	return static_file('index.html', root='views')

#from gevent import monkey; monkey.patch_all()
#bottle.run(app, host='0.0.0.0', port=26551, server='gevent')

bottle.run(app, host='0.0.0.0', port=26551, debug=True, reloader=True)
