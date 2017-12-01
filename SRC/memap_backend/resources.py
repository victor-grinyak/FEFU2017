from flask_restful import reqparse, abort
import flask_restful
import utils
import settings
import time
from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(time.time() - start)
        return res

    return wrapper


class Resource(flask_restful.Resource):
    method_decorators = [log]


class Diff(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        parser.add_argument('last_modified', type=int, required=True)
        args = parser.parse_args()
        user_id = utils.get_user_id(args['token'])
        if not user_id:
            abort(403, ok=False, error='invalid token')
        diff = utils.get_diff(user_id, args['last_modified'])
        return {'ok': True, 'updates': diff}


class Auth(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        check_res = utils.check_password(args['login'], args['password'])
        if check_res:
            token_res = utils.gen_token(args['login'])
            return token_res
        else:
            abort(401, ok=False, error='invalid login/password')


class Reg(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        reg_res = utils.reg_user(args['login'], args['password'])
        return reg_res


class Logout(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str, required=True)
        parser.add_argument('token', type=str, required=True)
        args = parser.parse_args()
        logout_res = utils.del_token(args['login'], args['token'])
        return logout_res


class NoteList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        args = parser.parse_args()
        user_id = utils.get_user_id(args['token'])
        if not user_id:
            abort(403, ok=False, error='invalid token')
        notes, archived_notes = utils.get_all_notes(user_id)
        return {'ok': True, 'notes': notes, 'archived_notes': archived_notes}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        parser.add_argument('header', type=str, required=True)
        parser.add_argument('date', type=int, required=True)
        parser.add_argument('longitude', type=float, required=True)
        parser.add_argument('lattitude', type=float, required=True)
        parser.add_argument('location_str', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('is_archived', type=bool, required=True)
        args = parser.parse_args()
        user_id = utils.get_user_id(args['token'])
        if not user_id:
            abort(403, ok=False, error='invalid token')
        post_res = utils.post_note(user_id, args)
        if post_res:
            return {'ok': True, 'note': post_res}
        abort(500, ok=False, error='unexpected error')


class Note(Resource):
    def get(self, note_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        args = parser.parse_args()
        user_id = utils.get_user_id(args['token'])
        if not user_id:
            abort(403, ok=False, error='invalid token')
        note = utils.get_note(user_id, note_id)
        if not note:
            abort(404, ok=False, error='note not found')
        return note

    def put(self, note_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        parser.add_argument('header', type=str, required=True)
        parser.add_argument('date', type=int, required=True)
        parser.add_argument('longitude', type=float, required=True)
        parser.add_argument('lattitude', type=float, required=True)
        parser.add_argument('location_str', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()
        user_id = utils.get_user_id(args['token'])
        if not user_id:
            abort(403, ok=False, error='invalid token')
        put_res = utils.put_note(user_id, note_id, args)
        if put_res:
            return {'ok': True, 'note': put_res}
        else:
            return abort(500, ok=False, error='note not found')

    def delete(self, note_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        args = parser.parse_args()
        user_id = utils.get_user_id(args['token'])
        if not user_id:
            abort(403, ok=False, error='invalid token')
        res_del = utils.del_note(user_id, note_id, settings.mark_as_deleted)
        if res_del:
            return {'ok': True}
        else:
            abort(404, ok=False, error='note not found')
