import json
import bottle
import re
from bson import ObjectId
from datetime import datetime
from bottle import request, response

from .utils import connect_db, entity2dict, triple2dict, mention2dict, o_is_entity, parse_href, make_href

app = bottle.app()
version = '1'
config_file = './config_host_cndbpedia.json'
db = connect_db(config_file)


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@app.route('/api/cndbpedia/test', method=['GET', 'POST'])
def test():
    ret = {
        'status': 'fail',
        'data': {},
        'error': 'connection failed'
    }

    temp = request.params.decode(encoding='utf-8')
    for k in temp:
        ret['data'][k] = temp[k]
    ret['status'] = 'success'
    ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/query_entity', method=['GET', 'POST'])
def query_entity():
    ret = {
        'status': 'fail',
        'nodes': [],
        'links': [],
        'error': 'connection failed'
    }

    _id = request.params.idx
    entity = db.entities.find_one({'_id': _id})
    if entity is None:
        ret['status'] = 'fail'
        ret['error'] = 'entity not found: {}'.format(_id)
    else:
        ret['status'] = 'success'
        ret['error'] = ''

        d = {}
        d[entity['_id']] = len(d)
        ret['nodes'].append(entity2dict(entity))
        for triple in db.triples.find({'s': entity['_id']}):
            if o_is_entity(triple['o']):
                o_id, _ = parse_href(triple['o'])
                o = db.entities.find_one({'_id': o_id})
                if o is None:
                    ret['status'] = 'fail'
                    ret['error'] = 'entity not found: {}'.format(o_id)
                else:
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
        for triple in db.triples.find({'s': node['idx']}):
            if not o_is_entity(triple['o']):
                ret['nodes'][index]['attr'].append(triple2dict(triple))

    return json.dumps(ret, ensure_ascii=False)


# @app.route('/api/cndbpedia/infobox/query_entity', method=['GET', 'POST'])
# def query_entity():
#     ret = {
#         'status': 'fail',
#         'res': [],
#         'error': 'connection failed'
#     }
#
#     _id = request.params.idx
#     entity = db.entities.find_one({'_id': _id})
#     if entity is None:
#         ret['status'] = 'fail'
#         ret['error'] = 'entity not found: {}'.format(_id)
#     else:
#         ret['status'] = 'success'
#         ret['res'].append(entity2dict(entity))
#         ret['error'] = ''
#
#     return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/add_entity', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/add_entity', method=['GET', 'POST'])
def add_entity():
    ret = {
        'status': 'fail',
        'idx': '',
        'error': 'connection failed'
    }

    _id = request.params.idx
    if db.entities.find_one({'_id': _id}) is not None:
        ret['status'] = 'fail'
        ret['error'] = 'entity exists: {}'.format(_id)
    else:
        r = db.entities.insert_one({'_id': _id, 'timestamp': datetime.now()})
        if not r.acknowledged:
            ret['status'] = 'fail'
            ret['error'] = 'insert failed'
        else:
            ret['status'] = 'success'
            ret['idx'] = r.inserted_id
            ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/update_entity', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/update_entity', method=['GET', 'POST'])
def update_entity():
    ret = {
        'status': 'fail',
        'error': 'connection failed'
    }

    _id = request.params.idx
    new_id = request.params.new_id
    if db.entities.find_one({'_id': _id}) is None:
        ret['status'] = 'fail'
        ret['error'] = 'entity not found: {}'.format(_id)
    elif db.entities.find_one({'_id': new_id}) is not None:
        ret['status'] = 'fail'
        ret['error'] = 'entity exists: {}'.format(new_id)
    else:
        p = re.compile(r'<a href="{}">.*?</a>'.format(_id))
        r1 = db.entities.delete_one({'_id': _id})
        r2 = db.entities.insert_one({'_id': new_id, 'timestamp': datetime.now()})
        r3 = db.triples.update_many({'s': _id}, {'$set': {'s': new_id, 'timestamp': datetime.now()}})
        r4 = db.triples.update_many({'o': {'$regex': p}}, {'$set': {'o': make_href(new_id, new_id), 'timestamp': datetime.now()}})
        r5 = db.ment2ent.update_many({'e': _id}, {'$set': {'e': new_id, 'timestamp': datetime.now()}})
        if not (r1.acknowledged and r2.acknowledged):
            ret['status'] = 'fail'
            ret['error'] = 'update failed'  # TODO: high level error
        elif not (r3.acknowledged and r4.acknowledged and r5.acknowledged):
            ret['status'] = 'fail'
            ret['error'] = 'update failed'
        else:
            ret['status'] = 'success'
            ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/delete_entity', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/delete_entity', method=['GET', 'POST'])
def delete_entity():
    ret = {
        'status': 'fail',
        'error': 'connection failed'
    }

    _id = request.params.idx
    p = re.compile(r'<a href="{}">.*?</a>'.format(_id))
    r1 = db.entities.delete_one({'_id': _id})
    r2 = db.triples.delete_many({'s': _id})
    r3 = db.triples.delete_many({'o': {'$regex': p}})
    r4 = db.ment2ent.delete_many({'e': _id})
    if not (r1.acknowledged and r2.acknowledged and r3.acknowledged and r4.acknowledged):
        ret['status'] = 'fail'
        ret['error'] = 'delete failed'
    else:
        ret['status'] = 'success'
        ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/add_relation', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/add_relation', method=['GET', 'POST'])
def add_relation():
    ret = {
        'status': 'fail',
        'idx': '',
        'error': 'connection failed'
    }

    s = request.params.s
    p = request.params.p
    o_id = request.params.o_id
    o_name = request.params.o_name
    o = make_href(o_id, o_name)
    if db.entities.find_one({'_id': s}) is None:
        ret['status'] = 'fail'
        ret['error'] = 'entity not found: {}'.format(s)
    elif db.entities.find_one({'_id': o_id}) is None:
        ret['status'] = 'fail'
        ret['error'] = 'entity not found: {}'.format(o_id)
    elif db.triples.find_one({'s': s, 'p': p, 'o': o}) is not None:
        ret['status'] = 'fail'
        ret['error'] = 'triple exists: {}-{}-{}'.format(s, p, o)
    else:
        r = db.triples.insert_one({'s': s, 'p': p, 'o': o, 'timestamp': datetime.now()})
        if not r.acknowledged:
            ret['status'] = 'fail'
            ret['error'] = 'insert failed'
        else:
            ret['status'] = 'success'
            ret['idx'] = str(r.inserted_id)
            ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/update_relation', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/update_relation', method=['GET', 'POST'])
def update_relation():
    ret = {
        'status': 'fail',
        'error': 'connection failed'
    }

    _id = request.params.idx
    new_p = request.params.new_p
    triple = db.triples.find_one({'_id': ObjectId(_id)})
    if triple is None:
        ret['status'] = 'fail'
        ret['error'] = 'triple not exists: {}'.format(_id)
    else:
        s = triple['s']
        o = triple['o']
        if db.triples.find_one({'s': s, 'p': new_p, 'o': o}) is not None:
            ret['status'] = 'fail'
            ret['error'] = 'triple exists: {}-{}-{}'.format(s, new_p, o)
        else:
            r = db.triples.update_one({'_id': ObjectId(_id)}, {'$set': {'p': new_p, 'timestamp': datetime.now()}})
            if not r.acknowledged:
                ret['status'] = 'fail'
                ret['error'] = 'update failed'
            else:
                ret['status'] = 'success'
                ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/delete_relation', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/delete_relation', method=['GET', 'POST'])
def delete_relation():
    ret = {
        'status': 'fail',
        'error': 'connection failed'
    }

    _id = request.params.idx
    r = db.triples.delete_one({'_id': ObjectId(_id)})
    if not r.acknowledged:
        ret['status'] = 'fail'
        ret['error'] = 'delete failed'
    else:
        ret['status'] = 'success'
        ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/add_attribute', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/add_attribute', method=['GET', 'POST'])
def add_attribute():
    ret = {
        'status': 'fail',
        'error': 'connection failed'
    }

    s = request.params.s
    p = request.params.p
    o = request.params.o
    if db.entities.find_one({'_id': s}) is None:
        ret['status'] = 'fail'
        ret['error'] = 'entity not found: {}'.format(s)
    elif db.triples.find_one({'s': s, 'p': p, 'o': o}) is not None:
        ret['status'] = 'fail'
        ret['error'] = 'triple exists: {}-{}-{}'.format(s, p, o)
    else:
        r = db.triples.insert_one({'s': s, 'p': p, 'o': o, 'timestamp': datetime.now()})
        if not r.acknowledged:
            ret['status'] = 'fail'
            ret['error'] = 'insert failed'
        else:
            ret['status'] = 'success'
            ret['idx'] = str(r.inserted_id)
            ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/update_attribute', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/update_attribute', method=['GET', 'POST'])
def update_attribute():
    ret = {
        'status': 'fail',
        'error': 'connection failed'
    }

    _id = request.params.idx
    new_p = request.params.new_p
    new_o = request.params.new_o
    triple = db.triples.find_one({'_id': ObjectId(_id)})
    if triple is None:
        ret['status'] = 'fail'
        ret['error'] = 'triple not found: {}'.format(_id)
    else:
        s = triple['s']
        if db.triples.find_one({'s': s, 'p': new_p, 'o': new_o}) is not None:
            ret['status'] = 'fail'
            ret['error'] = 'triple exists: {}-{}-{}'.format(s, new_p, new_o)
        else:
            r = db.triples.update_one({'_id': ObjectId(_id)}, {'$set': {'p': new_p, 'o': new_o, 'timestamp': datetime.now()}})
            if not r.acknowledged:
                ret['status'] = 'fail'
                ret['error'] = 'update failed'
            else:
                ret['status'] = 'success'
                ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


@app.route('/api/cndbpedia/graph/delete_attribute', method=['GET', 'POST'])
# @app.route('/api/cndbpedia/infobox/delete_attribute', method=['GET', 'POST'])
def delete_attribute():
    ret = {
        'status': 'fail',
        'error': 'connection failed'
    }

    _id = request.params.idx
    r = db.triples.delete_one({'_id': ObjectId(_id)})
    if not r.acknowledged:
        ret['status'] = 'fail'
        ret['error'] = 'delete failed'
    else:
        ret['status'] = 'success'
        ret['error'] = ''

    return json.dumps(ret, ensure_ascii=False)


# @app.route('/api/cndbpedia/infobox/query_mention', method=['GET', 'POST'])
# def query_mention():
#     ret = {
#         'status': 'fail',
#         'mentions': [],
#         'error': 'connection failed'
#     }
#
#     query = request.params.query
#     for mention in db.ment2ent.find({'m': query}):
#         ret['mentions'].append(mention2dict(mention))
#     for mention in db.ment2ent.find({'e': query}):
#         ret['mentions'].append(mention2dict(mention))
#     if len(ret['mentions']) == 0:
#         ret['status'] = 'fail'
#         ret['error'] = 'mention not found: {}'.format(query)
#     else:
#         ret['status'] = 'success'
#         ret['error'] = ''
#
#     return json.dumps(ret, ensure_ascii=False)


# @app.route('/api/cndbpedia/infobox/add_mention', method=['GET', 'POST'])
# def add_mention():
#     ret = {
#         'status': 'fail',
#         'idx': '',
#         'error': 'connection failed'
#     }
#
#     m = request.params.m
#     e = request.params.e
#     if db.entities.find_one({'_id': e}) is None:
#         ret['status'] = 'fail'
#         ret['error'] = 'entity not found: {}'.format(e)
#     elif db.ment2ent.find_one({'m': m, 'e': e}) is not None:
#         ret['status'] = 'fail'
#         ret['error'] = 'mention exists: {}-{}'.format(m, e)
#     else:
#         r = db.ment2ent.insert_one({'m': m, 'e': e, 'timestamp': datetime.now()})
#         if not r.acknowledged:
#             ret['status'] = 'fail'
#             ret['error'] = 'insert failed'
#         else:
#             ret['status'] = 'success'
#             ret['error'] = ''
#
#     return json.dumps(ret, ensure_ascii=False)


# @app.route('/api/cndbpedia/infobox/update_mention', method=['GET', 'POST'])
# def update_mention():
#     ret = {
#         'status': 'fail',
#         'error': 'connection failed'
#     }
#
#     _id = request.params.idx
#     new_m = request.params.new_m
#     new_e = request.params.new_e
#     if db.ment2ent.find_one({'_id': ObjectId(_id)}) is None:
#         ret['status'] = 'fail'
#         ret['error'] = 'mention not found: {}'.format(_id)
#     elif db.entities.find_one({'_id': new_e}) is None:
#         ret['status'] = 'fail'
#         ret['error'] = 'entity not found: {}'.format(new_e)
#     elif db.ment2ent.find_one({'m': new_m, 'e': new_e}) is not None:
#         ret['status'] = 'fail'
#         ret['error'] = 'mention exists: {}-{}'.format(new_m, new_e)
#     else:
#         r = db.ment2ent.update_one({'_id': ObjectId(_id)}, {'$set': {'m': new_m, 'e': new_e, 'timestamp': datetime.now()}})
#         if not r.acknowledged:
#             ret['status'] = 'fail'
#             ret['error'] = 'update failed'
#         else:
#             ret['status'] = 'success'
#             ret['error'] = ''
#
#     return json.dumps(ret, ensure_ascii=False)


# @app.route('/api/cndbpedia/infobox/delete_mention', method=['GET', 'POST'])
# def delete_mention():
#     ret = {
#         'status': 'fail',
#         'error': 'connection failed'
#     }
#
#     _id = request.params.idx
#     r = db.ment2ent.delete_one({'_id': ObjectId(_id)})
#     if not r.acknowledged:
#         ret['status'] = 'fail'
#         ret['error'] = 'delete failed'
#     else:
#         ret['status'] = 'success'
#         ret['error'] = ''
#
#     return json.dumps(ret, ensure_ascii=False)


def main():
    bottle.run(app, host='0.0.0.0', port=22222, server='tornado')


if __name__ == '__main__':
    main()
