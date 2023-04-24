""""""
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

import random
import sys
import logging
import os

from data import db_session
from data.users import User
from api import get_result
from users_resources import UsersListResource, UsersResource
from exceptions import *
from functions import *

app = Flask(__name__)
api = Api(app)

api.add_resource(UsersListResource, '/api/users')
api.add_resource(UsersResource, '/api/users/<int:user_id>')

app.config['SECRET_KEY'] = 'NaFo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
UPLOAD_FOLDER = "Z:/PycharmProjects/flask/Project_2/static/avatars"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
login_manager = LoginManager(app=app)

login_manager.login_view = '/'
login_manager.session_protection = 'strong'
login_manager.init_app(app)

db_session.global_init('db/database.db')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['POST', "GET"])
def mainpage():
    if request.method == 'POST':  # Если отправка данных
        try:
            if "main_header_button_play" in request.form:
                return redirect(url_for('login'))  # Переход
        except Exception as e:
            print(CriticalErrorException('>>> Critical Error'))
    return render_template("main.html")


@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == 'POST':  # Если отправка данных
        try:
            if "RegistrationButton" in request.form:
                return redirect(url_for('registration'))
            if "LoginSubmit" in request.form:
                """Есть ли такой пользователь, и если есть то return redirect(url_for('game'))"""
                db_sess = db_session.create_session()
                email = request.form.get('Email')
                password = request.form.get('Password')
                user = db_sess.query(User).filter(User.email == email).first()
                if user:
                    if user.check_password(password):
                        login_user(user)
                        return redirect(url_for('game'))
                    else:
                        print('Не правильный пароль')
                else:
                    print('Такого пользователя нет')
        except Exception as e:
            print(CriticalErrorException('>>> Critical Error'))
    return render_template("log.html")


@app.route('/registration', methods=['POST', "GET"])
def registration():
    if request.method == 'POST':  # Если отправка данных
        try:
            if "RegistrationButton" in request.form:
                db_sess = db_session.create_session()
                email = request.form.get('Email')
                login = request.form.get('Login')
                password = request.form.get('Password')

                user = db_sess.query(User).filter(User.email == email).first()
                if len(email) <= 5 or len(login) <= 3 or len(password) < 8:
                    raise ProblemWithSomeParameterException('>>> Invalid Parameters')
                else:
                    if user:
                        raise UserAlreadyExistsException('>>> User already exists')
                    else:
                        user = User()
                        user.email = email
                        user.login = login
                        user.set_password(password)

                        db_sess.add(user)
                        db_sess.commit()
                        login_user(user)
                        return redirect(url_for('game'))
            if "ReturnButton" in request.form:
                return redirect(url_for('login'))
        except Exception as e:
            print(CriticalErrorException('>>> Critical Error'))

        return render_template('registration.html')
    return render_template("registration.html")


@app.route('/game', methods=['POST', "GET"])
def game():
    Paper = "../static/img/Paper.png"
    Rock = "../static/img/Rock.png"
    Scissors = "../static/img/Scissors.png"
    lst = [Paper, Rock, Scissors]
    if request.method == 'POST':  # Если отправка данных
        try:
            if "game_button_item_rock" in request.form:
                Item = random.choice(lst)

                user_r = get_item(Rock)
                bot_r = get_item(Item)
                result = find_result(user_r, bot_r)
                # print(f"user_r: {user_r} | bot_r: {bot_r} | result: {result}")

                update_db(db_session, current_user, User, result)

                return render_template("game.html", user_item=Rock, bot_item=Item,
                                       result_of_game=result)
            if "game_button_item_paper" in request.form:
                Item = random.choice(lst)

                user_r = get_item(Paper)
                bot_r = get_item(Item)
                result = find_result(user_r, bot_r)
                # print(f"user_r: {user_r} | bot_r: {bot_r} | result: {result}")

                update_db(db_session, current_user, User, result)
                return render_template("game.html", user_item=Paper, bot_item=Item,
                                       result_of_game=result)
            if "game_button_item_scissors" in request.form:
                Item = random.choice(lst)

                user_r = get_item(Scissors)
                bot_r = get_item(Item)
                result = find_result(user_r, bot_r)
                # print(f"user_r: {user_r} | bot_r: {bot_r} | result: {result}")

                update_db(db_session, current_user, User, result)
                return render_template("game.html", user_item=Scissors, bot_item=Item,
                                       result_of_game=result)
            elif "game_button_profile" in request.form:
                return redirect(url_for('profile'))
        except Exception as e:
            print(CriticalErrorException('>>> Critical Error'))
        return render_template('game.html', user_item=Rock, bot_item=Rock)
    return render_template('game.html', user_item=Rock, bot_item=Rock)


@app.route('/profile', methods=['POST', "GET"])
@login_required
def profile():
    db_sess = db_session.create_session()
    email = current_user.email
    user = db_sess.query(User).filter(User.email == email).first()

    stats1 = user.stats1
    stats2 = user.stats2
    stats3 = user.stats3
    stats4 = user.stats4
    stats5 = user.stats5

    fact = get_result(stats1)

    try:
        if "profile_button_return" in request.form:
            return redirect(url_for('game'))
        elif "profile_button_logout" in request.form:
            return redirect(url_for('logout'))
    except Exception as e:
        print(CriticalErrorException('>>> Critical Error'))
        # return render_template('profile.html', user_login=current_user.login, stats1=stats1,
        #                        stats2=stats2, stats3=stats3, stats4=stats4, stats5=stats5, fact=fact)
    return render_template('profile.html', user_login=current_user.login, stats1=stats1,
                           stats2=stats2, stats3=stats3, stats4=stats4, stats5=stats5, fact=fact)

@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == "POST":
        try:
            print("Upload")
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.login == current_user.login).first()
            if user.avatar:
                # print(1)
                file = request.files['file']
                f = file.read()
                db_sess.commit()
                with open(os.path.join(UPLOAD_FOLDER, f"{current_user.login}.png"), "wb") as pic:
                    pic.write(f)
            else:
                file = request.files['file']
                user.avatar = f"{current_user.login}.png"
                db_sess.add(user)
                db_sess.commit()
                with open(os.path.join(UPLOAD_FOLDER, f"{current_user.login}.png"), "wb") as pic:
                    pic.write(file.read())
        except:
            pass
    return redirect(url_for('profile'))


@app.route('/logout')
@login_required
def logout():
    # Проверка Авторизации
    if current_user.is_authenticated:
        # Деавторизация Пользователя
        logout_user()
        # Перенаправление на Главную Страницу
        return redirect(url_for('mainpage'))
    else:
        # Перенаправление на Главную Страницу
        return redirect(url_for('mainpage'))


if __name__ == '__main__':
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.run(port=5000, host='127.0.0.1')
