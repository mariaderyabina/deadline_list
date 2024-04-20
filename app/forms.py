from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class CreateTaskForm(FlaskForm):
    task = StringField('Новая задача', validators=[DataRequired()])
    date = DateField('Дедлайн', validators=[DataRequired()])
    submit = SubmitField('Добавить задачу')

class StatusDoneForm(FlaskForm):
    submit = SubmitField('Сделано')

class StatusNotDoneForm(FlaskForm):
    submit = SubmitField('Не сделано')
    
class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Удалить')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user:
            raise ValidationError('Пожалуйста, выберите другое имя пользователя')
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user:
            raise ValidationError('Пожалуйста, выберите другой email адрес')
        