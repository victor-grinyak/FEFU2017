import binascii
import datetime
import os

import bcrypt
from pymongo import DESCENDING

import db


def hash_password(password):
    salt = bcrypt.gensalt()
    b_password = bytes(password, 'utf8')
    hashed_password = bcrypt.hashpw(b_password, salt)
    return hashed_password


def check_password(login, password):
    user = db.users_collection.find_one({'login': login})
    if not user:
        return False
    return bcrypt.checkpw(bytes(password, 'utf8'), user['password'])


def gen_token(login):
    token = binascii.b2a_hex(os.urandom(8))
    token = str(token, 'utf-8')
    while db.users_collection.find_one({'tokens': token}):
        token = binascii.b2a_hex(os.urandom(8))
        token = str(token, 'utf-8')
    res = db.users_collection.update_one({'login': login}, {'$push': {'tokens': token}})
    if res.raw_result['nModified'] == 1:
        return {'ok': True, 'token': token}
    return {'ok': False, 'error': 'unexpected error'}


def reg_user(login, password):
    if db.users_collection.find_one({'login': login}):
        return {'ok': False, 'error': 'login exist'}
    try:
        new_user_id = list(db.users_collection.find({}, {'id': 1}).sort('id', DESCENDING))[0]['id'] + 1
    except:
        new_user_id = 1
    res = db.users_collection.insert_one({'id': new_user_id, 'login': login, 'password': hash_password(password)})
    token_res = gen_token(login)
    return token_res


def del_token(login, token):
    res = db.users_collection.update_one({'login': login}, {'$pull': {'tokens': token}})
    if res.raw_result['nModified'] == 1:
        return {'ok': True}
    else:
        return {'ok': False, 'error': 'login/token not found'}


def get_user_id(token):
    res = db.users_collection.find_one({'tokens': token}, {'id': 1})
    if not res:
        return None
    return res['id']


def proccess_note_resp(note):
    if None:
        return None
    note.pop('_id', None)
    note.pop('owner_id', None)
    note.pop('token', None)
    note.pop('is_deleted', None)
    if 'last_modified' in note:
        note['last_modified'] = note['last_modified'].isoformat()
    return note


def get_note(user_id, note_id):
    note = db.notes_collection.find_one({'owner_id': user_id, 'id': note_id})
    return proccess_note_resp(note)


def post_note(user_id, note):
    note = proccess_note_resp(note)
    try:
        new_note_id = db.users_collection.find_one({'id': user_id}, {'note_count': 1})['note_count'] + 1
    except:
        new_note_id = 1
    note['id'] = new_note_id
    note['owner_id'] = user_id
    note['last_modified'] = datetime.datetime.utcnow()
    note['is_deleted'] = False
    note['is_archived'] = False
    res = db.notes_collection.insert_one(note)
    if res:
        db.users_collection.update({'id': user_id}, {'$inc': {'note_count': 1}})
    return proccess_note_resp(db.notes_collection.find_one({'owner_id': user_id, 'id': new_note_id}))


def get_all_notes(user_id):
    notes = list(db.notes_collection.find({'owner_id': user_id, 'is_deleted': False, 'is_archived': False}))
    archived_notes = list(db.notes_collection.find({'owner_id': user_id, 'is_deleted': False, 'is_archived': True}))
    notes = list(map(proccess_note_resp, notes))
    archived_notes = list(map(proccess_note_resp, archived_notes))
    return notes, archived_notes


def del_note(user_id, note_id, mark_as_deleted):
    if mark_as_deleted:
        res = db.notes_collection.update_one({'owner_id': user_id, 'id': note_id, 'is_deleted': False}, {'$set': {'is_deleted': True}})
    else:
        res = db.notes_collection.delete_one({'owner_id': user_id, 'id': note_id})
    if res.raw_result['n'] != 1:
        return False
    return True


def put_note(user_id, note_id, args):
    args['last_modified'] = datetime.datetime.utcnow()
    res = db.notes_collection.update({'owner_id': user_id, 'id': note_id}, {'$set': args})
    if res['n'] != 1:
        return None
    return proccess_note_resp(db.notes_collection.find_one({'owner_id': user_id, 'id': note_id}))


def get_diff(user_id, l_modified):
    last_client_modified = datetime.datetime.fromtimestamp(int(l_modified))
    res = list(db.notes_collection.find({'owner_id': user_id, 'last_modified': {'$gt': last_client_modified}}))
    print()
    return list(map(proccess_note_resp, res))
