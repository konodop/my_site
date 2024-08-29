# -*- coding: cp1251 -*-
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    # ������ ��� �����������
    email = EmailField('�����', validators=[DataRequired()])
    password = PasswordField('������', validators=[DataRequired()])
    password_again = PasswordField('��������� ������', validators=[DataRequired()])
    name = StringField('��� ������������', validators=[DataRequired()])
    about = TextAreaField("������� � ����")
    submit = SubmitField('����������������')


class LoginForm(FlaskForm):
    # ������ ��� ����� � �������
    email = EmailField('�����', validators=[DataRequired()])
    password = PasswordField('������', validators=[DataRequired()])
    submit = SubmitField('�����')