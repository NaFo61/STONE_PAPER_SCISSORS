import datetime
import sqlalchemy
from sqlalchemy import orm

from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash



class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    login = sqlalchemy.Column(sqlalchemy.String)
    avatar = sqlalchemy.Column(sqlalchemy.String)  # путь до аватарки
    stats1 = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Победа
    stats2 = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Ничья
    stats3 = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Поражение
    stats4 = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Всего игр
    stats5 = sqlalchemy.Column(sqlalchemy.String, default='0')  # Победа / Поражения
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    def update_stats1(self):
        self.stats1 += 1
        self.update_stats4()

    def update_stats2(self):
        self.stats2 += 1
        self.update_stats4()

    def update_stats3(self):
        self.stats3 += 1
        self.update_stats4()

    def update_stats4(self):
        self.stats4 += 1

    def update_stats5(self):
        try:
            wins = self.stats1
            loses = self.stats3
            kd = wins / loses
            kd = str(round(kd, 2))
            self.stats5 = kd
        except Exception as e:
            print(e)


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<User> {self.id} {self.login}!!!"
