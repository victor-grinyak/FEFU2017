import json

from bson import json_util
from flask import Flask, jsonify, Response, request
from flask_restful import Api
from functools import wraps
import db
import settings
from resources import Auth, Reg, Logout, NoteList, Note, Diff

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
api = Api(app)


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


def check_auth(username, password):
    return username == 'admin' and password == '12sec'


def authenticate():
    return Response(
        'Auth Required', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/db/notes')
@requires_auth
def return_all_users():
    notes = list(db.notes_collection.find({}))
    return jsonify(json.loads(json_util.dumps(notes)))


@app.route('/db/users')
@requires_auth
def return_all_notes():
    users = list(db.users_collection.find({}))
    return jsonify(json.loads(json_util.dumps(users)))


api.add_resource(Diff, '/api/notes/updates')
api.add_resource(Auth, '/api/auth')
api.add_resource(Reg, '/api/reg')
api.add_resource(Logout, '/api/logout')
api.add_resource(NoteList, '/api/notes')
api.add_resource(Note, '/api/notes/<int:note_id>')

if __name__ == '__main__':
    app.run(port=settings.port)
