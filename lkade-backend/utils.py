import json, hashlib, re
from bottle import route, template, request, response, static_file
from beaker.middleware import SessionMiddleware
from bson.objectid import ObjectId

def check_authority(write=False):
	#return True
	sess = request.environ.get('beaker.session')
	islogin = sess.get('issLogin', False)
	canwrite = sess.get('canWrite', False)
	if not islogin: return False
	if write and not canwrite: return False
	return True
not_authority_ret = json.dumps({'status':'fail', 'msg':'没有权限'}, ensure_ascii=False)

session_opts = {
	'session.type':'file',
    'session.cookei_expires':300,
    'session.data_dir':'./sessions',
    'sessioni.auto':True
}

def DefineCommonFuncs(app, user_table):
	@app.hook('after_request')
	def enable_cors(): response.headers['Access-Control-Allow-Origin'] = '*'

	@app.route('/', method='GET')
	@app.error(404)
	def index(error=''):
		return static_file('index.html', root='./vdist')
	
	@app.route('/static/<filepath:path>')
	def static(filepath):
	    return static_file(filepath, root="./vdist/static")
	
	@app.route('/login_check', method=['POST', 'OPTIONS'])
	def login_check():
		sess = request.environ.get('beaker.session')
		ret = {'status': 'fail'}
		response.headers['Access-Control-Allow-Headers'] = "Content-Type,XFILENAME,XFILECATEGORY,XFILESIZE,x-requested-with,Authorization"
		user = request.params.user
		passwd = request.params.passwd
		theuser = user_table.find_one({'username': user})
		if theuser is not None:
			saltpass = (theuser.get('password', '')+'salt123').encode()
			if passwd == hashlib.md5(saltpass).hexdigest():
				ret['status'] = 'ok'
				ret['uname'] = user
				sess['issLogin'] = True
				sess['canWrite'] = theuser.get('isguest') is None
				sess.save()
		return json.dumps(ret, ensure_ascii=False)
	
	@app.route('/login_exit', method=['POST', 'OPTIONS'])
	def login_exit():
		sess = request.environ.get('beaker.session')
		sess['issLogin'] = False
		sess.save()
		ret = {'status': 'ok'}
		return json.dumps(ret, ensure_ascii=False)

	
	sapp = SessionMiddleware(app, session_opts)
	return sapp


def DefineSchemaFuncs(app, schema_table):
	'''
	SCHEMA相关
	'''
	@app.route('/api/schemas', method=['GET', 'POST'])
	def schemas():
		if not check_authority(): return not_authority_ret
		if schema_table is None: return {'status': 'error', 'msg': '库中没有Schema功能'}
		ret = {'status': 'ok', 'ret': []}
		for x in schema_table.find({}):
			item = {
					'id': str(x['_id']),
					'op_type': x['op_type'],
					'cond_p': x['cond_p'],
					'limit_o': x['limit_o'],
					'limit_o_type': x['limit_o_type']
				}
			ret['ret'].append(item) 
		return ret

	@app.route('/api/remove_schema', method = ['GET', 'POST'])
	def remove_schema():
		if not check_authority(write=True): return not_authority_ret
		tid = request.params.id
		if schema_table is None: return {'status': 'error', 'msg': '没有Schema'}
		del_result = schema_table.delete_one({'_id': ObjectId(tid)})
		status = 'ok' if del_result.acknowledged else 'error'
		return {'status':status, 'ret': ''}

	def precheck_new_schema(cond_p, op_type, limit_o_type, limit_o):
		if schema_table is None: return '库中没有Schema功能'
		if cond_p == '': return '属性名/关系名cond_p不能为空'
		if op_type not in ['and', 'or']: return 'op_type必须为and或者or'
		if limit_o_type not in ['eval', 'regex', 'equal']: return 'limit_o_type必须为eval，regex，equal之一'
		if len(limit_o) == 0: return 'limit_o不能为空'
		if limit_o_type == 'eval' and len(limit_o) > 10: return '出于安全考虑，当limit_o_type为eval时limit_o有长度限制'

	@app.route('/api/new_schema', method = ['GET', 'POST'])
	def new_schema():
		if not check_authority(write=True): return not_authority_ret
		cond_p = request.params.cond_p
		op_type = request.params.op_type
		limit_o_type = request.params.limit_o_type
		limit_o = request.params.limit_o
		precheck = request.params.precheck
		msg = precheck_new_schema(cond_p, op_type, limit_o_type, limit_o)
		ret = {'status': 'error' if msg else 'ok', 'msg': msg}
		if precheck: return json.dumps(ret, ensure_ascii=False)
		if not msg:
			ditem = {'cond_p': cond_p, 'op_type': op_type, 
			   'limit_o_type':limit_o_type, 'limit_o': limit_o}
			schema_table.insert_one(ditem)
		return json.dumps(ret, ensure_ascii=False)


def check_schema_rules(rules, value):
	def check_single_rule(rule, value):
		if rule['limit_o_type'] == 'regex':
			rr = '^%s$' % rule['limit_o']
			return re.match(rr, value) is not None
		elif rule['limit_o_type'] == 'equal':
			return value == rule['limit_o']
		elif rule['limit_o_type'] == 'eval':
			x = value
			try: 
				x = float(x)
				return eval(rule['limit_o']) is True
			except:
				try: return eval(rule['limit_o']) is True
				except: return False
		return False
	for rule in [x for x in rules if x['op_type'] == 'or']:
		if check_single_rule(rule, value): return 'ok'
	for rule in [x for x in rules if x['op_type'] == 'and']:
		if not check_single_rule(rule, value): return rule['limit_o_type'] + ': ' + rule['limit_o']
	return 'ok'