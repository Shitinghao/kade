import json, hashlib
from bottle import route, template, request, response, static_file
from beaker.middleware import SessionMiddleware

def check_authority(write=False):
	return True
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
