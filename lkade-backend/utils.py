import json
import re
from queue import Queue
from datetime import datetime
from pymongo import MongoClient


def connect_db(config_file):
    with open(config_file, 'r', encoding='utf-8') as fin:
        config = json.load(fin)

    host = config.get('host', '127.0.0.1')
    port = config.get('port', 27017)
    db_name = config.get('db_name', '')
    db_user = config.get('db_user', '')
    db_passwd = config.get('db_passwd', '')
    auth_mech = config.get('auth_mech', 'SCRAM-SHA-1')

    client = MongoClient(host=host, port=port)
    if db_user != '':
        client.admin.authenticate(db_user, db_passwd, mechanism=auth_mech)
    db = client.get_database(db_name)

    return db


def entity2dict(entity):
    return {'idx': entity['_id'], 'timestamp': entity['timestamp'].timestamp(), 'attr': []}


def triple2dict(triple):
    return {'idx': str(triple['_id']), 's': triple['s'], 'p': triple['p'], 'o': triple['o'], 'timestamp': triple['timestamp'].timestamp()}


def mention2dict(mention):
    return {'idx': str(mention['_id']), 'm': mention['m'], 'e': mention['e'], 'timestamp': mention['timestamp'].timestamp()}


def o_is_entity(o):
    return re.match(r'<a href="(.*?)">(.*?)</a>', o) is not None


def parse_href(o):
    r = re.match(r'<a href="(.*?)">(.*?)</a>', o)
    o_id, o_name = r.group(1), r.group(2)

    return o_id, o_name


def make_href(o_id, o_name):
    return '<a href="{}">{}</a>'.format(o_id, o_name)


def parse_a(o):
    return re.sub(r'<a>|</a>', '', o)


def make_a(o):
    return '<a>{}</a>'.format(o)


def download_db(src_db, dst_db):
    for collection in src_db.list_collection_names():
        src_col = src_db.get_collection(collection)
        dst_col = dst_db.get_collection(collection)
        for line in src_col.find({}):
            if dst_col.find_one(line) is None:
                dst_col.insert_one(line)


def download_small_data(src_db, dst_db):
    for line in src_db.ment2attribute.find({}):
        if dst_db.ment2attribute.find_one(line) is None:
            dst_db.ment2attribute.insert_one(line)

    wait_list = Queue()
    for t in ['歌手', '中国大学', '中国高校']:
        for line in src_db.triples.find({'o': t}):
            ent = line['s']
            if src_db.entities.find_one({'_id': ent}):
                wait_list.put(ent)
    print(datetime.now())
    print(wait_list.qsize())

    cnt = 0
    while not wait_list.empty():
        ent = wait_list.get()
        if dst_db.entities.find_one({'_id': ent}) is not None:
            continue

        cnt += 1
        if cnt % 1000 == 0:
            print(datetime.now())
            print('processing: ', cnt)

        for line in src_db.entities.find({'_id': ent}):
            if dst_db.entities.find_one(line) is None:
                dst_db.entities.insert_one(line)
        for line in src_db.triples.find({'s': ent}):
            if o_is_entity(line['o']):
                o, _ = parse_href(line['o'])
                if src_db.entities.find_one({'_id': o}) is None:
                    continue
                wait_list.put(o)
            if dst_db.triples.find_one(line) is None:
                dst_db.triples.insert_one(line)
        for line in src_db.ment2ent.find({'e': ent}):
            if dst_db.ment2ent.find_one(line) is None:
                dst_db.ment2ent.insert_one(line)


def convert_db(src_db, dst_db):
    wait_list = Queue()
    done_list = set()

    for t in ['歌手', '中国大学', '中国高校']:
        for line in src_db.triples.find({'o': t}):
            name = line['s']
            if src_db.entities.find_one({'_id': name}):
                wait_list.put(name)
    for line in src_db.triples.find({'o': {'$regex': 'href'}}).limit(10000):
        if not o_is_entity(line['o']):
            continue
        s = line['s']
        if src_db.entities.find_one({'_id': s}):
            wait_list.put(s)
        o, _ = parse_href(line[['o']])
        if src_db.entities.find_one({'_id': o}):
            wait_list.put(o)
    print(datetime.now())
    print(wait_list.qsize())

    cnt = 0
    while not wait_list.empty():
        name = wait_list.get()
        if name in done_list:
            continue
        done_list.add(name)

        cnt += 1
        if cnt % 1000 == 0:
            print(datetime.now())
            print('processing: ', cnt)

        if dst_db.entity.find_one({'name': name}) is None:
            dst_db.entity.insert_one({'name': name, 'timestamp': datetime.now()})
        sid = str(dst_db.entity.find_one({'name': name})['_id'])
        for line in src_db.ment2ent.find({'e': name}):
            m = line['m']
            if dst_db.ment2ent.find_one({'m': m, 'eid': sid}) is None:
                dst_db.ment2ent.insert_one({'m': m, 'eid': sid, 'timestamp': datetime.now()})
        for line in src_db.triples.find({'s': name}):
            p = line['p']
            if o_is_entity(line['o']):
                o, _ = parse_href(line['o'])
                if src_db.entities.find_one({'_id': o}) is None:
                    continue
                if o not in done_list:
                    wait_list.put(o)
                if dst_db.entity.find_one({'name': o}) is None:
                    dst_db.entity.insert_one({'name': o, 'timestamp': datetime.now()})
                oid = str(dst_db.entity.find_one({'name': o})['_id'])
                for temp in src_db.ment2ent.find({'e': o}):
                    m = temp['m']
                    if dst_db.ment2ent.find_one({'m': m, 'eid': oid}) is None:
                        dst_db.ment2ent.insert_one({'m': m, 'eid': oid, 'timestamp': datetime.now()})
                if dst_db.triple_rel.find_one({'sid': sid, 'p': p, 'oid': oid}) is None:
                    dst_db.triple_rel.insert_one({'sid': sid, 'p': p, 'oid': oid, 'timestamp': datetime.now()})
            else:
                o = parse_a(line['o'])
                if dst_db.triple_attr.find_one({'sid': sid, 'p': p, 'o': o}) is None:
                    dst_db.triple_attr.insert_one({'sid': sid, 'p': p, 'o': o, 'timestamp': datetime.now()})

    for line in src_db.ment2attribute.find({}):
        m = line['m']
        a = line['a']
        if dst_db.ment2attr.find_one({'m': m, 'a': a}) is None:
            dst_db.ment2attr.insert_one({'m': m, 'a': a, 'timestamp': datetime.now()})
