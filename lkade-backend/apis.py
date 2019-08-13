import sys
if 'prod' in sys.argv:
	from gevent import monkey; monkey.patch_all()

import shutil, re, json, random, requests
import os, time, traceback
import urllib.parse
import bottle, platform
from bottle import route, template, request, response, static_file
from pymongo import MongoClient
from datetime import datetime
import logging
import logging.handlers
from bson.objectid import ObjectId


DB = 'local'
if DB == 'local':
	client = MongoClient('10.141.208.26', 27017)
	client.admin.authenticate('gdmdbuser', '6QEUI8dhnq', mechanism='SCRAM-SHA-1')

config = {
	'entity_name_field': '_id',
}

db = client.get_database('cndbpedia')
user_table = db.get_collection('user')
entity_table = db.get_collection('entities')
triple_table = db.get_collection('triples')
ment2ent_table = db.get_collection('ment2ent')

app = bottle.app()

from utils import *

#logfile = 'apis.log'
#if DB == 'local': logfile = '/home/kw/db_data/log/apis.log'
#filehandler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight', encoding='utf-8')
#filehandler.suffix = "%Y%m%d.log"
#logging.basicConfig(handlers=[filehandler], 
#					format='%(asctime)s\t%(message)s',
#					datefmt='%Y-%m-%d %H:%M:%S',
#					level=logging.INFO)

def RemoveHref(x): 
	return re.sub('<a[^>]*>', '', x).replace('</a>', '')

def GetEntitybyID(sid):
	return entity_table.find_one( {'_id': sid} )

def GetEntityName(ent):
	if ent is None: return ''
	return ent[config['entity_name_field']]

def TestSpecialChars(sr): 
	if re.search(r'[<>\'"\s]', sr):
		return True
	else:
		return False

def SplitHref(zz):
	zz = zz.replace('</a>', '')
	if '<a>' in zz: eid = ename = zz.split('<a>')[-1]
	else:
		vv = re.search('<a href="(.+?)">(.+?)$', zz)
		eid, ename = vv.group(1), vv.group(2)
	return eid, ename

def SplitDBO(x):
	if x['o'].endswith('</a>') and x['o'].startswith('<a'): oid, oname = SplitHref(x['o'])
	else: oid, oname = '', RemoveHref(x['o'])
	return oid, oname

@app.route('/api/triples', method=['GET', 'POST'])
def triples():
	if not check_authority(): return not_authority_ret
	entity = request.params.entity
	keephref = request.params.keephref
	ret = []; ok = True
	if len(entity) > 200: ok = False
	procO = RemoveHref if keephref == '' else (lambda x:x)
	entity = entity.replace('"', '').replace('"', '')
	xx = triple_table.find({'s': entity}).limit(1000)
	for x in xx:
		oid, oname = SplitDBO(x)
		item = {'id':str(x['_id']), 
		  's':x['s'], 'sname':x['s'], 'p':x['p'],
		  'oid':oid, 'oname':oname}
		ret.append(item)
	ret = {'status':'ok','ret': ret}
	return json.dumps(ret, ensure_ascii = False)

@app.route('/api/ment2ent', method = ['GET', 'POST'])
def ment2ent():
	if not check_authority(): return not_authority_ret
	mention = request.params.q
	no_other_m = request.params.no_other_m
	ok = True
	if len(mention) > 200: ok = False

	rets = []
	entx = GetEntitybyID(mention)
	if entx is not None: 
		ent = mention
		rets.append({'m':mention, 'e':ent, 'isent': True})
		if not no_other_m:
			rets.extend(ment2ent_table.find({'e': ent}))

	xx = ment2ent_table.find({'e': {'$ne': mention}, 'm': mention}).limit(1000)
	rets.extend(list(xx))
	ret = [{'id':str(x.get('_id', '')), 'mention': x['m'], \
		 'eid': x['e'], 'ename': GetEntityName(GetEntitybyID(x['e'])),
		 'isent': x.get('isent', False)} for x in rets]
	ret = {'status':'ok','ret': ret}
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


def precheck_new_triple(sid, p, oid, oname, old_tid):
	if sid == '' or GetEntitybyID(sid) is None: return '实体不存在'
	if p == '': return '属性不能为空'
	if TestSpecialChars(p): return '属性不能包含特殊符号或空白符'
	query = {'s': sid, 'p': p}
	exists = list(triple_table.find(query))
	if old_tid != '':
		exists = [x for x in exists if x['_id'] != ObjectId(old_tid)]
	for xx in exists:
		ooid, ooname = SplitDBO(xx)
		if ooname == oname: return '存在重复关系'
		if oid != '' and ooid == oid: return '存在重复关系'
	if oname != '':
		if TestSpecialChars(oname): return '值不能包含特殊符号或空白符'
	if oid != '':
		oo = GetEntitybyID(oid)
		if oo is None: return 'Object实体不存在'
		if oname != '' and GetEntityName(oo) != oname: return "实体名称不匹配"
	if oname == '' and oid == '':
		return '值不能为空'

@app.route('/api/new_triple', method = ['GET', 'POST'])
def new_triple():
	if not check_authority(write=True): return not_authority_ret
	sid = request.params.sid
	p = request.params.p
	oid = request.params.oid
	oname = request.params.oname
	old_tid = request.params.old_tid
	precheck = request.params.precheck
	msg = precheck_new_triple(sid, p, oid, oname, old_tid)
	ret = {'status': 'error' if msg else 'ok', 'msg': msg}
	if precheck: return json.dumps(ret, ensure_ascii=False)
	if not msg:
		ostr = oname
		if oid != '': ostr = '<a href="%s">%s</a>' % (oid, oname)
		ditem = {'s': sid, 'p': p, 'o': ostr}
		rr = triple_table.insert_one(ditem)
		ret['eid'] = str(rr.inserted_id)
	return json.dumps(ret, ensure_ascii=False)


def precheck_new_ment2ent(eid, mention):
	if mention == '': return '别名不能为空'
	if TestSpecialChars(mention): return '别名不能包含特殊符号或空白符'
	ent = GetEntitybyID(eid)
	if ent is None: return '实体不存在'
	print(GetEntityName(ent), mention)
	if GetEntityName(ent) == mention: return '别名不能和实体名相同'
	ditem = {'m': mention, 'e': eid}
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
		ditem = {'m': mention, 'e': eid}
		ment2ent_table.insert_one(ditem)
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_triple', method = ['GET', 'POST'])
def remove_triple():
	if not check_authority(write=True): return not_authority_ret
	tid = request.params.id
	ok = True
	del_result = triple_table.delete_one({'_id': ObjectId(tid)})
	status = 'ok' if del_result.acknowledged else 'error'
	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_ment2ent', method = ['GET', 'POST'])
def remove_ment2ent():
	if not check_authority(write=True): return not_authority_ret
	tid = request.params.id
	ok = True
	del_result = ment2ent_table.delete_one({'_id': ObjectId(tid)})
	status = 'ok' if del_result.acknowledged else 'error'
	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii = False)

def RemoveEntity(ent):
	ment2ent_table.delete_many({'e': ent})
	triple_table.delete_many({'s': ent})
	return entity_table.delete_one({'_id': ent})

def EntityRelatedInfos(ent):
	tris = []
	for x in ment2ent_table.find({'e': ent}):
		tris.append({'s':x['e'], 'p': '别名', 'o':x['m']})
	for x in triple_table.find({'s': ent}):
		tris.append({'s':x['s'], 'p': x['p'], 'o':x['o']})
	return tris

@app.route('/api/info_remove_entity', method = ['GET', 'POST'])
def info_remove_entity():
	eid = request.params.id
	ret = {'status':'ok','ret': EntityRelatedInfos(eid)}
	return json.dumps(ret, ensure_ascii=False)

@app.route('/api/remove_entity', method = ['GET', 'POST'])
def remove_entity():
	if not check_authority(write=True): return not_authority_ret
	eid = request.params.id
	ok = True
	del_result = RemoveEntity(eid)
	status = 'ok' if del_result.acknowledged else 'error'
	ret = {'status':status, 'ret': 'ok'}
	return json.dumps(ret, ensure_ascii=False)



def entity2dict(entity):
	#'timestamp': entity['timestamp'].timestamp(), 
	return {'idx': entity['_id'], 'attr': []}

def o_is_entity(o):
	return re.match(r'<a(.*?)</a>', o) is not None

def triple2dict(triple):
	ret = {'idx': str(triple['_id']), 's': triple['s'], 'p': triple['p'], 'o': triple['o']}
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
	_id = request.params.idx
	no_expand = request.params.no_expand
	entity = entity_table.find_one({'_id': _id})
	if entity is None:
		ret['status'] = 'fail'
		ret['error'] = 'entity not found: {}'.format(_id)
	else:
		ret['status'] = 'success'
		ret['error'] = ''

		d = {}
		d[entity['_id']] = len(d)
		ret['nodes'].append(entity2dict(entity))
		if not no_expand:
			for triple in triple_table.find({'s': entity['_id']}):
				if o_is_entity(triple['o']):
					o_id, _ = SplitHref(triple['o'])
					o = GetEntitybyID(o_id)
					if o is not None:
						if o['_id'] not in d:
							d[o['_id']] = len(d)
							ret['nodes'].append(entity2dict(o))
						ret['links'].append({
							'source': d[entity['_id']],
							'target': d[o['_id']],
							'triple': triple2dict(triple)
						})

	for index in range(len(ret['nodes'])):
		node = ret['nodes'][index]
		for triple in triple_table.find({'s': node['idx']}):
			if not o_is_entity(triple['o']):
				ret['nodes'][index]['attr'].append(triple2dict(triple))

	return json.dumps(ret, ensure_ascii=False)


def make_href(o_id, o_name):
	return '<a href="{}">{}</a>'.format(o_id, o_name)

@app.route('/api/graph/update_triple_p', method=['GET', 'POST'])
def update_triple_p():
	if not check_authority(): return not_authority_ret
	ret = {
		'status': 'fail',
		'msg': 'connection failed'
	}
	_id = request.params.idx
	new_p = request.params.new_p
	triple = triple_table.find_one({'_id': ObjectId(_id)})
	if triple is None:
		ret['status'] = 'fail'
		ret['msg'] = '关系不存在：{}'.format(_id)
	else:
		s = triple['s']
		o = triple['o']
		if triple_table.find_one({'s': s, 'p': new_p, 'o': o}) is not None:
			ret['status'] = 'fail'
			ret['error'] = '关系重复: {}-{}-{}'.format(s, new_p, o)
		else:
			r = triple_table.update_one({'_id': ObjectId(_id)}, {'$set': {'p': new_p, 'timestamp': datetime.now()}})
			if not r.acknowledged:
				ret['status'] = 'fail'
				ret['msg'] = 'update failed'
			else:
				ret['status'] = 'success'
				ret['msg'] = '修改关系成功'
	return json.dumps(ret, ensure_ascii=False)

sapp = DefineCommonFuncs(app, user_table)

if 'prod' in sys.argv:
	bottle.run(sapp, host='0.0.0.0', port=26551, server='gevent')
else: 
	bottle.run(sapp, host='0.0.0.0', port=26551, debug=True, reloader=True)
