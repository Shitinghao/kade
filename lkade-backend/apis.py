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
	client = MongoClient('10.141.208.26', 27017)
	client.admin.authenticate('gdmdbuser', '6QEUI8dhnq', mechanism='SCRAM-SHA-1')

config = {
		'entity_name_field': '_id',
	}


dbcd = client.cndbpedia

app = bottle.app()

@app.hook('after_request')
def enable_cors(): response.headers['Access-Control-Allow-Origin'] = '*'

#logfile = 'apis.log'
#if DB == 'local': logfile = '/home/kw/db_data/log/apis.log'
#filehandler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight', encoding='utf-8')
#filehandler.suffix = "%Y%m%d.log"
#logging.basicConfig(handlers=[filehandler], 
#					format='%(asctime)s\t%(message)s',
#                    datefmt='%Y-%m-%d %H:%M:%S',
#					level=logging.INFO)

msg_badapikey = '{"status":"fail", "reason": "bad apikey"}'
msg_toofreq = '{"status":"fail", "reason": "too many requests"}'
msg_callus = '{"status":"fail", "reason": "您目前的APIkey无权限访问高级内容，请联系我们升级"}'


def T(xx):
    if xx is None: return xx
    xx['_id'] = str(xx['_id'])
    for k, v in xx.items():
        if isinstance(v, datetime): xx[k] = v.timestamp()
    return xx


def DoPreCheck(params=[]): return 'ok', ''

def RemoveHref(x): 
	return re.sub('<a[^>]*>', '', x).replace('</a>', '')

def GetEntitybyID(sid):
	return dbcd.entities.find_one( {'_id': sid} )

def SplitHref(zz):
	zz = zz.replace('</a>', '')
	if '<a>' in zz: eid = ename = zz.split('<a>')[-1]
	else:
		vv = re.search('<a href="(.+?)">(.+?)$', zz)
		eid, ename = vv.group(1), vv.group(2)
	return eid, ename

@app.route('/api/triples', method=['GET', 'POST'])
def triples():
	entity = request.params.entity
	keephref = request.params.keephref
	ret = []; ok = True
	if len(entity) > 200: ok = False
	procO = RemoveHref if keephref == '' else (lambda x:x)
	entity = entity.replace('"', '').replace('"', '')
	xx = dbcd.triples.find({'s': entity}).limit(1000)
	for x in xx:
		if x['o'].endswith('</a>') and x['o'].startswith('<a'): oid, oname = SplitHref(x['o'])
		else: oid, oname = '', RemoveHref(x['o'])
		item = {'id':str(x['_id']), 's':x['s'], 'p':x['p'], 'oid':oid, 'oname':oname}
		ret.append(item)
	ret = {'status':'ok','ret': ret}
	return json.dumps(ret, ensure_ascii = False)

@app.route('/api/ment2ent', method = ['GET', 'POST'])
def ment2ent():
	mention = request.params.q
	ok = True
	if len(mention) > 200: ok = False
	xx = dbcd.ment2ent.find({'m': mention}).limit(1000)
	ent = list(xx)
	if GetEntitybyID(mention) is not None: ent.append({'m':mention, 'e':mention})
	ret = [{'id':str(x.get('_id', '')), 'mention': x['m'], 'eid': x['e'], 'ename': GetEntitybyID(x['e'])[config['entity_name_field']]} for x in ent]
	ret = {'status':'ok','ret': ret}
	return json.dumps(ret, ensure_ascii = False)

@app.route('/api/newentity', method = ['GET', 'POST'])
def newentity():
	name = request.params.name
	ok = True
	ditem = {config['entity_name_field']: name}
	ditem = dbcd.entities.insert_one(ditem)
	ret = {'status':'ok','ret': ditem}
	return json.dumps(ret, ensure_ascii = False)

@app.route('/api/newtriple', method = ['GET', 'POST'])
def newtriple():
	sid = request.params.sid
	p = request.params.p
	oid = request.params.oid
	oname = request.params.oname
	assert '<' not in oid and '>' not in oname
	ostr = oid
	if oname != '': ostr = '<a href="%s">%s</a>' % (oid, oname)
	ditem = {'s': sid, 'p': p, 'o': ostr}
	ins_result = dbcd.triples.insert_one(ditem)
	ret = {'status':'ok','ret': 'succ'}
	return json.dumps(ret, ensure_ascii = False)

@app.route('/api/removetriple', method = ['GET', 'POST'])
def removetriple():
	tid = request.params.id
	ok = True
	del_result = dbcd.triples.delete_one({'_id': ObjectId(tid)})
	ret = {'status':'ok','ret': 'ok'}
	return json.dumps(ret, ensure_ascii = False)

@app.route('/', method='GET')
def index():
	return static_file('index.html', root='views')

#from gevent import monkey; monkey.patch_all()
#bottle.run(app, host='0.0.0.0', port=26551, server='gevent')

bottle.run(app, host='0.0.0.0', port=26551, debug=True, reloader=True)
