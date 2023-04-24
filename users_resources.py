from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    db_session.global_init('db/mars_explorer.db')
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_session.global_init('db/database.db')
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'email', 'login', 'stats1', 'stats2', 'stats3', 'stats4', 'stats5')
        )})

class UsersListResource(Resource):
    def get(self):
        db_session.global_init('db/database.db')
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [user.to_dict(
            only=('id', 'email', 'login', 'stats1', 'stats2', 'stats3', 'stats4', 'stats5')) for user in users]})

