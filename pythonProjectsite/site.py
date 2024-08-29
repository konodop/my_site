# -*- coding: cp1251 -*-
# ����������� ��������� � ��������� ����������
import json
from forms.user import RegisterForm, LoginForm
from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.news import News

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


# �������� �������� ��������� � http://127.0.0.1:8080/

@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    # ��������� ���������� � ��������� �� info.json
    with open("templates/info.json", "rt", encoding="cp1251") as f:
        waterfalls = json.loads(f.read())
    if request.method == 'GET':
        return render_template('main.html', waterfalls=waterfalls, comms='', title='������� �������� ���������',
                               news=news)
    elif request.method == 'POST':
        s = request.form['about']
        user = db_sess.query(User).filter(User.id == 1).first()
        # ���� �� ����� � �������, ��������� �� �����������
        if user is not None:
            # ��������� � ����������� �����������
            user.news.append(News(content=s))
            db_sess.commit()
            return render_template('main.html', waterfalls=waterfalls, comms=s, title='������� �������� ���������',
                                   news=news)
        else:
            return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        # ��������� ������
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='�����������',
                                   form=form,
                                   message="������ �� ���������")
        db_sess = db_session.create_session()
        # ��������� ��������� �� �����
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='�����������',
                                   form=form,
                                   message="����� ������������ ��� ����")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        # ��������� ������������
        db_sess.add(user)
        # ��������� ���� ������
        db_sess.commit()
        # ���������� �� �������� � ������������
        return redirect('/login')
    return render_template('register.html', title='�����������', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(email=form.email.data).first()
        # ��������� �� �������� � ����� � ������
        if user is not None and user.check_password(form.password.data):
            # ���������� �� �������� ��������
            return redirect('/')
        else:
            return render_template('login.html', message='����� ���� ������ ������� �������', form=form)
    return render_template('login.html', title='�����������', form=form)


if __name__ == '__main__':
    main()
